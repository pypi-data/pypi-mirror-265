import concurrent.futures
import io
import math
import pickle
import re
import time
from typing import Union, List

import numpy as np
import pandas as pd
import pymongo
import rados
from radosdb.config.config import parse_config
import radosdb
from radosdb.common.helper.redis_helper import get_redis_client
from radosdb.config.config import parse_config
from radosdb.model.time_conversion import DatetimeConversion
from radosdb.repo.mongo_data_meta_repo import MongoDataMetaRepo
from radosdb.repo.mongo_trade_day_repo import MongoTradeDayRepo
from radosdb.service.data_meta_service import DataMetaService
from radosdb.service.trade_day_service import TradeDayService
from rd import *
from tdata import *
import datetime

import warnings

warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)

__all__ = [
    "write",
    "read",
    "delete",
    "find_fields",
    "trade_day_repo",
    "data_meta_service",
    "trade_day_service"
]

radosdb_config = parse_config("radosdb", path=radosdb.config)
data_length = radosdb_config["data_length"]
ceph_config = radosdb_config["ceph"]
conf_path = ceph_config["conf_path"]
admin_path = ceph_config["admin_path"]
default_pool = ceph_config["pool"]
max_threads = radosdb_config["max_threads"]
max_size = ceph_config['max_object'] * 1024 ** 2
default_size = ceph_config['max_write_object'] * 1024 ** 2

max_size_gb = ceph_config["max_size_gb"]
total_index_df = ceph_config["total_index_df"]
redis_config = radosdb_config.get("redis")

lock_config = radosdb_config.get("lock", {})
data_lock_prefix = lock_config['data_lock_prefix']

redis_client = get_redis_client(redis_config)

mongo_config = radosdb_config["mongo"]
mongo_url = mongo_config["url"]
db_name = mongo_config["db_name"]
collection_name = mongo_config["collection_name"]
mongo_client = pymongo.MongoClient(mongo_url)
mongodb = mongo_client[db_name]

trade_day_repo = MongoTradeDayRepo(mongodb)
datetime_conversion = DatetimeConversion(trade_day_repo)
data_meta_service = DataMetaService(MongoDataMetaRepo(mongodb,collection_name))
trade_day_service = TradeDayService(trade_day_repo)

pattern = re.compile(r"\.\d+$")

date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
datetime_pattern = re.compile(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2}(:\d{2})?)?")

def write_to_object(name:str,
                    data:bytes,
                    offset:int):
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            completion = ioctx.aio_write(name, data,offset)
            completion.wait_for_complete()
            completion.wait_for_safe()
            return completion.get_return_value()

def update_object(name:str,
                  data:bytes,
                  offset:int):
    with redis_client.lock(f"{data_lock_prefix}{name}"):
        return write_to_object(name, data, offset)

def multithread_write(name_list:list[str],
                      data_list:list[np.array],
                      offset_list:list[int]):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(write_to_object, str(name), data.tobytes(), int(offset))
            for name, data,offset in zip(name_list, data_list, offset_list)
        ]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results

def transfer_datetime_to_tick(dt: Union[int, str, pd.Timestamp]) -> int:
    if isinstance(dt, int):
        return dt
    elif isinstance(dt, pd.Timestamp):
        return datetime_conversion.datetime2tick(dt)
    elif isinstance(dt, str):
        return datetime_conversion.datetime2tick(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"))

def read_index_df(name: str) -> pd.DataFrame | None:
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            with redis_client.lock(f"{data_lock_prefix}{name}"):
                try:
                    index_df = ioctx.read(name, max_size)
                    if len(index_df) == 0:
                        return None
                except rados.ObjectNotFound:
                    return None
                index_df = pickle.loads(index_df)

                return index_df

def write_df(name:str,
             data:pd.DataFrame,
             freq: int,
             start: int=None,
             end: int=None
             ) -> int:
    if data.index[-1] < data.index[0]:
        data = data[::-1]
    if isinstance(data.index, pd.DatetimeIndex):
        data.index = datetime_conversion.datetime2tick_by_range(data.index[0], data.index[-1], freq)

    data,start,end = loc_df(data, start, end)
    index_df = read_index_df(name)
    res = []

    if index_df is None:
        res.append(write_single_df(name, data))
    else:
        existing_index = np.concatenate([np.arange(row[0], row[1] + 1, freq) for row in index_df[["start", "end"]].values])
        real_index = np.arange(index_df.iat[0,1],index_df.iat[-1,2]+1,freq)
        last_object_size = index_df.iat[-1,4][0]*index_df.iat[-1,4][1]*8
        criteria = np.array_equal(existing_index,real_index) & (len(data) <= data_length) & ((start-real_index[-1])<=freq) & (start >= int(index_df.iat[-1,1])) & (last_object_size<=default_size)
        if criteria:
            return update_single_df(name, data, freq, index_df)

        need_to_rewrite_index = data.index[data.index.isin(existing_index)]  # 找到需要覆盖的index
        need_to_rewrite_df = index_df[(index_df.start >= start) & (index_df.end <= end)]

        first = index_df[(index_df.start < start) & (index_df.end >= start)]
        last = index_df[(index_df.start <= end) & (index_df.end > end)]

        if not first.empty:
            data_to_write = data.loc[start: first.iat[0,2]].reindex(columns=first.iat[0,3],copy=False)
            bytes_to_start = ((start-first.iat[0,1])/freq)*len(first.iat[0,3])*8
            res.append(write_to_object(first.iat[0,0], data_to_write.values.tobytes(), int(bytes_to_start)))

        if not last.empty:
            data_to_write = data.loc[last.iat[0,1]:end].reindex(columns=last.iat[0,3],copy=False)
            res.append(write_to_object(last.iat[0,0], data_to_write.values.tobytes(), 0))

        if not need_to_rewrite_df.empty:
            res.append(write_single_df(name,
                                       data,
                                       name_list=need_to_rewrite_df.file_name.tolist(),
                                       start_list=need_to_rewrite_df.start.tolist(),
                                       end_list=need_to_rewrite_df.end.tolist(),
                                       shape_list=need_to_rewrite_df.shape_list))

        data = data[~(data.index.isin(need_to_rewrite_index))]
        if not data.empty:
            res.append(write_single_df(name, data))

    if sum(res) == 0:
        return 0
    else:
        raise Exception(f"{name} {data.index[0]} to {data.index[-1]} write failed")

def update_index_df(name: str, index_df: pd.DataFrame) -> int:
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            with redis_client.lock(f"{data_lock_prefix}{name}"):
                try:
                    old_index_df: pd.DataFrame = pickle.loads(ioctx.read(name, max_size))
                    index_df = pd.concat([old_index_df, index_df], axis=0)
                    index_df = index_df.drop_duplicates(subset=['start'],keep='last',ignore_index=True).sort_values(by=["start"])
                    index_df.index = range(len(index_df))
                except rados.ObjectNotFound:
                    index_df = index_df

                index_df = pickle.dumps(index_df)
                completion = ioctx.aio_write_full(name, index_df)
                completion.wait_for_complete()
                completion.wait_for_safe()

                return completion.get_return_value()

def write_single_df(name:str,
                    data:pd.DataFrame,
                    name_list: list[str] = None,
                    start_list: list[int] = None,
                    end_list: list[int] = None,
                    shape_list: list[tuple[int,int]] = None):

    data_values = data.values

    col = data.columns

    if name_list is None:
        chunk = math.ceil(len(data_values.tobytes()) / default_size)
        data_list = np.array_split(data_values, chunk)
    else:
        shape_list = np.insert(np.cumsum(np.array(list(shape_list),copy=False)[:,0]),0,0)
        data_list = [data_values[shape_list[i]:shape_list[i+1]] for i in range(len(shape_list)-1)]

    index_array = np.array_split(data.index.values, chunk) if name_list is None else None
    start_list = [i[0] for i in index_array] if name_list is None else start_list
    end_list = [i[-1] for i in index_array] if name_list is None else end_list
    name_list = [f'{name}_{start}_{end}' for start, end in zip(start_list, end_list)] if name_list is None else name_list
    shape_list = [i.shape for i in data_list]
    offset_list = [0] * len(name_list)

    max_len = math.floor(max_size_gb*1024/(default_size/1024**2))
    split = math.ceil(len(name_list)/max_len)
    name_split = np.array_split(name_list,split)
    name_shape = np.insert(np.cumsum(np.array([len(i) for i in name_split],copy=False)),0,0)
    data_split = [data_list[name_shape[i]:name_shape[i+1]] for i in range(len(name_shape)-1)]

    res = []
    for name_l,data_l,offset_l in zip(name_split,data_split,np.array_split(offset_list,split)):
        res.append(sum(multithread_write(name_l, data_l, offset_l)))
    res = sum(res)

    index_df = pd.DataFrame({'file_name':name_list,
                                 'start': start_list,
                                 'end': end_list,
                                 'col_list': [list(col)]*len(name_list),
                                 'shape_list': shape_list},
                                  copy=False)
    if res == 0:
        res_index = update_index_df(name, index_df=index_df)
        if sum([res, res_index]) == 0:
            return 0
        else:
            raise Exception(f"write_index_df failed: {name}, {res_index}")
    else:
        raise Exception(f"write_single_df failed: {name}, range: {start_list[0]} to {end_list[-1]}")


def transfer_to_tick(time_stamp:int|pd.Timestamp|str, end=False):
    if isinstance(time_stamp, int):
        return max(time_stamp,0)
    elif isinstance(time_stamp, str):
        if date_pattern.fullmatch(time_stamp):
            time_stamp = pd.Timestamp(time_stamp+'T1500') if end else pd.Timestamp(time_stamp+'T0930')
        elif datetime_pattern.fullmatch(time_stamp):
            time_stamp = pd.Timestamp(time_stamp)
        else:
            raise Exception('The time format you input is not supported, please input int, pd.Timestamp or str in the format of "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" or "YYYY-MM-DD HH:MM:SS"')
    elif isinstance(time_stamp, pd.Timestamp):
        time_stamp = time_stamp
    else:
        raise Exception('The time format you input is not supported, please input int, pd.Timestamp or str in the format of "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" or "YYYY-MM-DD HH:MM:SS"')
    time_stamp = max(time_stamp, pd.Timestamp('2009-01-05T09:30:00'))
    real_day = trade_day_repo.find_last_less_than_day(time_stamp.to_pydatetime()).real_date if end else trade_day_repo.find_first_greater_than_day(time_stamp.normalize()).real_date
    time_stamp = datetime.datetime.combine(real_day, time_stamp.time())

    return datetime_conversion.datetime2tick(time_stamp)



def write(
        name: str,
        data: Union[int, float, pd.Series, pd.DataFrame],
        start: Union[int, str, pd.Timestamp] = None,
        end: Union[int, str, pd.Timestamp] = None,
        freq: int = None,
):
    start = transfer_to_tick(start) if start is not None else start
    end = transfer_to_tick(end,True) if end is not None else end

    mongo_data = data_meta_service.find_data(name)
    if mongo_data is None:
        raise Exception(f"{name} not exist in MongoDB")
    else:
        axes = mongo_data.get("type").get("axes")
    if len(axes) == 0:
        res = write_to_object(name, pickle.dumps(data),offset=0)

    elif len(axes) == 1:

        if isinstance(data, list):
            res = write_to_object(name, pickle.dumps(data),offset=0)
        else:
            if isinstance(data.index, pd.DatetimeIndex):
                data.index = datetime_conversion.datetime2tick_by_range(data.index[0], data.index[-1], freq)
            try:
                original_data = pickle.loads(read_from_object(name, max_size, 0))
                common_index = original_data.index.intersection(data.index)
                original_data = original_data.drop(common_index,errors='ignore')
                data = pd.concat([original_data, data], copy=False)
                data = data.reindex(index=sorted(data.index), copy=False)
            except:
                data = data
            res = write_to_object(name, pickle.dumps(data), offset=0)

    elif len(axes) == 2:
        if axes[0].get('type') == axes[1].get('type') == 'Named':
            try:
                original_data = pickle.loads(read_from_object(name, max_size, 0))
                common_index = original_data.index.intersection(data.index)
                original_data = original_data.drop(common_index, errors='ignore')
                data = pd.concat([original_data, data], copy=False)
                data = data.reindex(index=sorted(data.index), copy=False)
                res = write_to_object(name, pickle.dumps(data), offset=0)
            except:
                res = write_to_object(name, pickle.dumps(data), offset=0)
        else:
            freq = axes[0].get("freq") if freq is None else freq
            if name in ['reserve_report_date']:
                data = data.astype(int).astype(np.float64)
            res = write_df(name=name, data=data,freq=freq, start=start, end=end)

    elif len(axes) == 3:

        freq = axes[0].get("freq") if freq is None else freq
        res_t = []
        try:
            data_len = pickle.loads(read_from_object(f'{name}_len', max_size, 0))
            res_len = 0
        except:
            data_len = len(data)
            res_len = write_to_object(f'{name}_len', pickle.dumps(len(data)),offset=0)
        res_t.append(res_len)
        for length in range(data_len):
            new_name = f"{name}.{length}"
            real_data = data[length]
            res_t.append(write_df(name=new_name, data=real_data,freq=freq, start=start, end=end))
        res = sum(res_t)
    else:
        raise Exception(f"type not supported")
    if res == 0:
        return True
    else:
        raise Exception(f"{name} write failed")


def read_from_object(oid,length,offset):
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            return ioctx.read(oid, length, offset)

def form_df(oid, length, offset, shape, index,col,new_col):
    data = read_from_object(oid, length, offset)
    return pd.DataFrame(np.frombuffer(data, dtype=np.float64).reshape(-1,shape[1]),index=index,columns=col, copy=False).reindex(columns=new_col, copy=False)

def index_to_datetime(start: int, end: int, freq):
    mappings = datetime_conversion.query_trade_days(start // 4840, end // 4840)
    return pd.DatetimeIndex(datetime_conversion.tick2datetime_by_range(start, end + 1, freq, mappings))

def multithreading_read(file_name_list: list[str],
                        length_list:list[int],
                        offset_list: list[int],
                        index_list: list[np.array],
                        shape_list: list[tuple[int,int]],
                        col_list:list[list[str]],
                        new_col_list:list[list[str]]):

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(form_df, file_name,length,offset,shape,index,col,new_col) for file_name,length,offset,shape,index,col,new_col in zip(file_name_list, length_list, offset_list, shape_list,index_list, col_list,new_col_list)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results

def read_df(
        name: str,
        start: Union[int, str, pd.Timestamp] = None,
        end: Union[int, str, pd.Timestamp] = None,
        freq: int = None,
        columns: List[str] = None,
        to_datetime: bool = False
):
    try:
        col_type = data_meta_service.find_data(name).get("type").get('axes')[1].get('type')
    except:
        raise Exception(f"{name} does not exist in MongoDB")

    index_df = read_index_df(name)
    if index_df is None:
        raise Exception(f"{name} not exist")

    data_end = int(index_df.iat[-1, 2])
    start = int(index_df.iat[0,1]) if start is None else transfer_datetime_to_tick(start)
    end = data_end if end is None else transfer_datetime_to_tick(end)

    if start > end:
        raise Exception(f"start {start} should be less than end {end}")

    full_index = np.arange(data_end, start-1, -freq)
    index = full_index[(full_index >= start) & (full_index <= end)][::-1]
    if len(index) == 0:
        raise Exception(f"{name} does not exist in the time range from {start} to {end}")

    start,end = int(index[0]),int(index[-1])
    idx = index_to_datetime(start, end, freq) if to_datetime else index

    if col_type == "Stock":
        col = columns if columns is not None else find_fields(start, end)
    else:
        col = index_df.iat[0,3]
    if index_df.iat[0,4][1] == 1:
        index_df['col_list'] = [col] * len(index_df)

    index_df = index_df[((index_df.start >= start) & (index_df.end <= end)) | ((index_df.start <= end) & (index_df.end > end)) |
                        ((index_df.start < start) & (index_df.end >= start)) | ((index_df.start <= start) & (index_df.end >= end))]


    if len(index_df) == 1:
        real_start = max(start,index_df.iat[0,1])
        bytes_to_start = ((real_start - index_df.iat[0,1]) / freq) * index_df.iat[0,4][1] * 8
        length = int(((end - real_start) /freq +1) * index_df.iat[0,4][1] * 8)
        data = form_df(index_df.iat[0,0], length, int(bytes_to_start), index_df.iat[0,4],np.arange(real_start,end+1,freq), index_df.iat[0,3],col)
        data = data.reindex(index=index,copy=False)
        data.index = idx if to_datetime else index

        return data
    else:
        file_name_list,length_list, offset_list,shape_list, index_list, col_list, new_col_list = [], [], [], [], [], [], []
        first = index_df[(index_df.start < start) & (index_df.end >= start)]
        last = index_df[(index_df.start <= end) & (index_df.end > end)]
        need_to_read_df = index_df[(index_df.start >= start) & (index_df.end <= end)]
        if first.empty and last.empty and need_to_read_df.empty:
            data = pd.DataFrame(data=np.full((len(index), len(col)), np.nan), index=index, columns=col, copy=False, dtype="float64")
            data.index = idx if to_datetime else index
            return data
        else:
            if not first.empty:
                bytes_to_start = ((start - first.iat[0, 1]) / freq) * first.iat[0, 4][1] * 8
                file_name_list.append(first.iat[0, 0])
                length_list.append(int(first.iat[0, 4][0] * first.iat[0, 4][1] * 8))
                offset_list.append(int(bytes_to_start))
                shape_list.append(first.iat[0, 4])
                index_list.append(np.arange(start,first.iat[0,2]+1,freq))
                col_list.append(first.iat[0, 3])
                new_col_list.append(col)

            if not last.empty:
                length = int(((index[-1]-last.iat[0,1])/freq+1)*last.iat[0,4][1]*8)
                file_name_list.append(last.iat[0, 0])
                length_list.append(length)
                offset_list.append(0)
                shape_list.append(last.iat[0, 4])
                index_list.append(np.arange(last.iat[0,1],index[-1]+1,freq))
                col_list.append(last.iat[0, 3])
                new_col_list.append(col)

            if not need_to_read_df.empty:
                file_name_list += need_to_read_df.file_name.tolist()
                length_list += [int(i[0]*i[1]*8) for i in need_to_read_df.shape_list]
                offset_list += [0]*len(file_name_list)
                index_list += [np.arange(i[1],i[2]+1,freq) for i in need_to_read_df.itertuples(index=False)]
                shape_list += need_to_read_df.shape_list.tolist()
                col_list += need_to_read_df.col_list.tolist()
                new_col_list += [col]*len(file_name_list)

            res = multithreading_read(file_name_list, length_list, offset_list,index_list, shape_list, col_list,new_col_list)
            res = sorted(res,key=lambda x:x.index[0])
            data = concat_dfs(res, axis=0)
            data = data.reindex(index=index, copy=False)
            data.index = idx if to_datetime else index

            return data

def transfer_floatdf2datetimedf(data:pd.DataFrame):

    return pd.DataFrame(pd.to_datetime(data.astype(int).values.ravel()).values.reshape(data.shape),
                        index=data.index,
                        columns=data.columns)

def read(name: str,
         start: int|pd.Timestamp|str = None,
         end: int|pd.Timestamp|str = None,
         freq: int = None,
         columns: List[str] = None,
         to_datetime: bool = False):

    start = transfer_to_tick(start) if start is not None else start
    end = transfer_to_tick(end,True) if end is not None else end

    if pattern.findall(name):
        full_name = name.split('.')[0]
        if freq is None:
            freq = data_meta_service.find_data(full_name).get("type").get("axes")[0].get("freq")
        mongo_data = data_meta_service.find_data(full_name)
        if mongo_data is None:
            raise Exception(f"{full_name} not exist in MongoDB")
        function_id = mongo_data.get("expression").get("functionId")
        num = int(name.split('.')[-1])
        if function_id == 'Stack':
            vars = data_meta_service.find_data(full_name).get("expression").get("inputs").get("vars")
            if num > (len(vars)-1):
                raise Exception(f"serial number exceeds the length of variable when slice")
            child_name = vars[num]
            return read_df(name=child_name, start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime)
        else:
            data_len = pickle.loads(read_from_object(f"{full_name}_len", max_size, 0))
            if num > (data_len-1):
                raise Exception(f"serial number exceeds the length of variable when slice")
            else:
                return read_df(name=f"{full_name}.{num}", start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime)

    mongo_data = data_meta_service.find_data(name)
    if mongo_data is None:
        raise Exception(f"{name} not exist in MongoDB")

    axes = mongo_data.get("type").get("axes")
    freq = axes[0].get("freq") if freq is None else freq
    if len(axes) == 0 or len(axes) == 1:
        data = pickle.loads(read_from_object(name, max_size, 0))
        if axes[0].get("type") == 'List':
            return data
        else:
            start = start if start else 0
            end = end if end else data.index[-1]
            data = data[(data.index>=start)&(data.index<=end)]
            data.index = index_to_datetime(int(data.index[0]),int(data.index[-1]),freq) if to_datetime else data.index
            return data
    elif len(axes) == 2:
        if axes[0].get('type') == axes[1].get('type') == 'Named':
            data = pickle.loads(read_from_object(name, max_size, 0))
            return data
        else:
            data = read_df(name=name, start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime)
            if name in ['reserve_report_date']:
                data = transfer_floatdf2datetimedf(data)
            return data
    elif len(axes) == 3:
        function_id = mongo_data.get("expression").get("functionId")
        if function_id == 'Stack':
            vars = data_meta_service.find_data(name).get("expression").get("inputs").get("vars")
            res = []
            for i in vars:
                child_data = data_meta_service.find_data(i)
                if child_data is None:
                    raise Exception(f"{i} not exist when stack {name}")
                else:
                    freq = child_data.get('type').get('axes')[0].get('freq')
                    if i not in ['reserve_report_date']:
                        res.append(read(i,start,end,freq,columns,to_datetime))
                    else:
                        res.append(transfer_floatdf2datetimedf(read_df(name=i, start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime)))
            return res
        else:
            data_len = pickle.loads(read_from_object(f"{name}_len", max_size, 0))
            res = []
            freq = data_meta_service.find_data(name).get('type').get('axes')[0].get('freq')
            for i in range(data_len):
                res.append(read_df(name=f"{name}.{i}", start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime))
            return res
    else:
        raise Exception(f"type not supported")

def delete_single_object(name: str):
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            res = ioctx.remove_object(name)
            return res


def multithreading_delete(file_name_list: list):

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(delete_single_object, file_name) for file_name in file_name_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results

def delete_df(name):
    index_df = read_index_df(name)
    if index_df is None:
        raise Exception(f"Data {name} you require to delete does not exist")
    else:
        file_name_list = index_df.file_name.tolist()
        res = multithreading_delete(file_name_list)
        if sum(res) == len(res):
            res_index = delete_single_object(name)
            if res_index:
                return True
            else:
                raise Exception(f'{name} index_df delete failed, but data has been deleted')
        else:
            raise Exception(f"{name} delete failed")

def get_size(name:str):
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            return ioctx.stat(name)[0]/1024**2

def update_single_df(name:str,
                     data: pd.DataFrame,
                     freq:int,
                     index_df:pd.DataFrame):

    last_object_name = index_df.iat[-1,0]
    last_object_df = index_df[index_df.file_name == last_object_name]

    if all(data.columns.isin(last_object_df.iat[-1,3])):
        data = data.reindex(columns=last_object_df.iat[-1,3], copy=False)
        bytes_to_start = int(((data.index[0] - last_object_df.iat[-1,1]) / freq) * last_object_df.iat[-1,4][1] * 8)
        res = update_object(last_object_name, data.values.tobytes(), bytes_to_start)

    else:
        united_col = sorted(pd.Index(last_object_df.iat[-1,3]).union(data.columns).tolist())
        length = int(last_object_df.iat[-1,4][0] * last_object_df.iat[-1,4][1] * 8)
        original_data = form_df(last_object_name,length,0,last_object_df.iat[-1,4],np.arange(last_object_df.iat[-1,1],last_object_df.iat[-1,2]+1,freq),last_object_df.iat[-1,3],united_col)
        data = data.reindex(columns=united_col, copy=False)
        data = concat_dfs([original_data, data], axis=0)
        res = update_object(last_object_name, data.values.tobytes(), 0)
        last_object_df.iat[-1, 3] = united_col

    last_object_df.iat[-1,2] = int(data.index[-1])
    last_object_df.iat[-1,4] = (int((last_object_df.iat[-1,2]-last_object_df.iat[-1,1])/freq+1), len(last_object_df.iat[-1,3]))
    res_index = update_index_df(name, last_object_df)

    if sum([res, res_index]) != 0:
        raise Exception(f"{name} update failed")
    return 0

def loc_df(data,start,end):

    data_index = data.index
    if start is None and end is None:
        start = data.index[0]
        end = data.index[-1]
    elif start is None and end:
        start = data.index[0]
        end_loc = data.index.get_loc(data_index[data_index <= end][-1])
        data = data.iloc[:end_loc + 1]
    elif start and end is None:
        end = data.index[-1]
        start_loc = data.index.get_loc(data_index[data_index >= start][0])
        data = data.iloc[start_loc:]
    else:
        start_loc = data.index.get_loc(data_index[data_index >= start][0])
        end_loc = data.index.get_loc(data_index[data_index <= end][-1])
        data = data.iloc[start_loc:end_loc + 1]

    return data,start,end


def delete(name: str):

    mongo_data = data_meta_service.reset_eff(name)
    if mongo_data is False:
        raise Exception(f"{name} reset eff failed")
    mongo_data = data_meta_service.find_data(name)
    axes = mongo_data.get("type").get("axes")
    if len(axes) in [0,1]:
        res = delete_single_object(name)
    elif len(axes) == 2:
        res = delete_df(name)
    elif len(axes) == 3:
        function_id = mongo_data.get("expression").get("functionId")
        if function_id != 'Stack':
            res = []
            length = pickle.loads(read_from_object(f"{name}_len", max_size, 0))
            for i in range(length):
                res.append(delete_df(f"{name}.{i}"))
            res = all(res)
            if res:
                res_len = delete_single_object(f"{name}_len")
                if res_len:
                    return True
                else:
                    raise Exception(f"{name}_len delete failed")
        else:
            raise Exception(f'Name:{name} the list contains elemental data which cannot be deleted')
    else:
        raise Exception(f"length of axes not supported")
    if res:
        return True
    else:
        raise Exception(f"{name} delete failed")

def dump_single_df(df: pd.DataFrame):
    stream = io.BytesIO()
    df.to_pickle(stream, compression="zstd")
    return stream.getvalue()

def load_single_df(data):
    stream = io.BytesIO(data)
    return pd.read_pickle(stream, compression="zstd")

def transfer_tick_to_str(tick: Union[int, pd.Timestamp, str]) -> str:
    if isinstance(tick, pd.Timestamp):
        return tick.strftime("%Y-%m-%d")
    elif isinstance(tick,int):
        return datetime_conversion.tick2datetime(tick).strftime("%Y-%m-%d")
    elif isinstance(tick, str):
        return pd.Timestamp(tick).strftime("%Y-%m-%d")
    else:
        raise Exception(f"{type(tick)} type not supported")

def find_fields(start: Union[str, pd.Timestamp, int] = None, end: Union[str, pd.Timestamp, int] = None):
    index_df = load_single_df(read_from_object(total_index_df, max_size, 0))
    start = index_df.index[0] if start is None else transfer_tick_to_str(start)
    end = index_df.index[-1] if end is None else transfer_tick_to_str(end)
    index_df = index_df.loc[start:end]

    return index_df.columns[index_df.any()].tolist()

def update_total_index_df():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    close = fetch_data('close',end_date=today)['close']
    index_df = close.notna().astype(int)
    index_df = dump_single_df(index_df)
    write_to_object(total_index_df, index_df, offset=0)

def daily_update():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today = '2024-04-01'
    def get_basis_data_map():
        res = requests.get(f"http://172.17.101.48:8001/api/v1/datum_api/sourcedata_in_tfdb")
        res = res.json().get("data")
        return [i.get("name") for i in res]

    basic_data = get_basis_data_map()
    not_wanted = ('_l1', '_l2')
    ll = [data for data in basic_data if all(index not in data for index in not_wanted)]
    data = fetch_data(ll, start_date=today,end_date=today)
    for i in tqdm(ll):
        try:
            write(i, data[i])
        except:
            print(i)

def slice_minute_data():

    data_ls = ['close_min','buy_sell_min']
    minute_list = pd.date_range("09:30", "11:30", freq="min").append(
        pd.date_range("13:00", "15:00", freq="min")).strftime('%H:%M').tolist()
    minute_dict = {i: minute for i, minute in enumerate(minute_list)}
    for data_name in tqdm(data_ls):
        data = read(data_name,to_datetime=True)
        for j in tqdm(range(242)):
            data_slice = data.at_time(minute_dict[j])
            write(f'{data_name}_{j}',data_slice)

if __name__ == '__main__':
   start = time.time()
   data = read('close_min')
   print(time.time()-start)
