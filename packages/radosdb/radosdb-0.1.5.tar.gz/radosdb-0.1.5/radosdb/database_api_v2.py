import concurrent.futures
import io
import math
import pickle
import re
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
from service.data_meta_service import DataMetaService
from radosdb.service.trade_day_service import TradeDayService
from rd import concat_dfs
from tdata import *
import datetime

__all__ = [
    "write",
    "read",
    "delete",
    "find_fields",
    "trade_day_repo",
    "data_meta_service",
    "trade_day_service",
    "update_single_data"
]

radosdb_config = parse_config("radosdb", path=radosdb.config)
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

def write_to_object(name:str,
                    data:bytes,
                    offset:int):
    with rados.Rados(conffile=conf_path, conf=dict(keyring=admin_path)) as cluster:
        with cluster.open_ioctx(default_pool) as ioctx:
            completion = ioctx.aio_write(name, data,offset)
            completion.wait_for_complete()
            completion.wait_for_safe()
            return completion.get_return_value()

def multithread_write(name_list:list[str],
                      data_list:list[np.array],
                      offset_list:list[int]):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(write_to_object, name, data.tobytes(), offset)
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
    data_size = data.shape[0] * data.shape[1] * 8
    if data_size/1024**3 > max_size_gb:
        raise Exception(f"{name} data size exceeds the maximum size")

    if isinstance(data.index, pd.DatetimeIndex):
        data.index = datetime_conversion.datetime2tick_by_range(data.index[0], data.index[-1], freq)

    data = data.loc[start:end]
    index_df = read_index_df(name)
    res = []

    if index_df is None:
        res.append(write_single_df(name, data))
    else:
        existing_index = np.concatenate([np.arange(row[0], row[1] + 1, freq) for row in index_df[["start", "end"]].values])
        need_to_rewrite_index = data.index[data.index.isin(existing_index)]  # 找到需要覆盖的index
        need_to_rewrite_df = index_df[(index_df.start >= start) & (index_df.end <= end)]

        first = index_df[(index_df.start < start) & (index_df.end >= start)]
        last = index_df[(index_df.start <= end) & (index_df.end > end)]

        if not first.empty:
            data_to_write = data.loc[start: first.iat[0,2]].reindex(columns=first.iat[0,3],copy=False)
            bytes_to_start = ((start-first.iat[0,1])/freq)*len(first.iat[0,3])*8
            res.append(write_to_object(first.iat[0,0], data_to_write.values.tobytes(), bytes_to_start))

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
                    index_df = concat_dfs([old_index_df, index_df], axis=0)
                    index_df = index_df.drop_duplicates(subset=['start'],keep='last').sort_values(by=["start"])
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

    res = sum(multithread_write(name_list, data_list, offset_list))

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

def update_eff(name: str,
               eff: int):
    db_data = data_meta_service.find_data(name)
    if db_data is not None:
        old_eff = db_data.get("eff")
        if eff > old_eff:
            data_meta_service.update_eff(name, int(eff))
    else:
        raise Exception(f"{name} not exist in MongoDB")

date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
datetime_pattern = re.compile(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2}(:\d{2})?)?")

def transfer_to_tick(time_stamp:int|pd.Timestamp|str, end=False):
    if isinstance(time_stamp, int):
        return time_stamp
    elif isinstance(time_stamp, str):
        if date_pattern.fullmatch(time_stamp):
            time_stamp = pd.Timestamp(time_stamp+'T1500') if end else pd.Timestamp(time_stamp+'T0930')
        elif datetime_pattern.fullmatch(time_stamp):
            time_stamp = pd.Timestamp(time_stamp)
        else:
            raise Exception('The time format you input in not supported, please input int, pd.Timestamp or str in the format of "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"')
    elif isinstance(time_stamp, pd.Timestamp):
        time_stamp = time_stamp
    else:
        raise Exception('The time format you input in not supported, please input int, pd.Timestamp or str in the format of "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"')

    real_day = trade_day_repo.find_last_less_than_day(time_stamp.to_pydatetime()).real_date if end else trade_day_repo.find_first_greater_than_day(time_stamp.to_pydatetime()).real_date
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
        new_eff = 0

    elif len(axes) == 1:

        if isinstance(data, list):
            res = write_to_object(name, pickle.dumps(data),offset=0)
            new_eff = 0
        else:
            try:
                original_data = pickle.loads(read_from_object(name, max_size, 0))
                common_index = original_data.index.intersection(data.index)
                original_data = original_data.drop(common_index)
                data = pd.concat([original_data, data], copy=False)
                data = data.sort_index()
            except:
                data = data
            res = write_to_object(name, pickle.dumps(data), offset=0)
            new_eff = int(data.index.max())

    elif len(axes) == 2:
        freq = axes[0].get("freq") if freq is None else freq
        if len(data) <= 242:
            res = update_single_data(name=name, data=data, freq=freq)
        else:
            res = write_df(name=name, data=data,freq=freq, start=start, end=end)
        new_eff = data.index.max()

    elif len(axes) == 3:

        freq = axes[0].get("freq") if freq is None else freq
        res_t = []
        res_len = write_to_object(f'{name}_len', pickle.dumps(len(data)),offset=0)
        res_t.append(res_len)
        for length in range(len(data)):
            new_name = f"{name}.{length}"
            real_data = data[length]
            if len(real_data) <= 242:
                res_t.append(update_single_data(name=new_name, data=real_data, freq=freq))
            else:
                res_t.append(write_df(name=new_name, data=real_data,freq=freq, start=start, end=end))
        res = sum(res_t)
        new_eff = data[0].index.max()

    else:
        raise Exception(f"type not supported")
    if res == 0:
        if isinstance(new_eff, pd.Timestamp):
            new_eff = datetime_conversion.datetime2tick(new_eff)
        update_eff(name, new_eff)
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
    index_df = read_index_df(name)
    data_end = int(index_df.end.max())
    if index_df is None:
        raise Exception(f"{name} not exist")

    start = int(index_df.start.min()) if start is None else transfer_datetime_to_tick(start)
    start = max(start,0)
    end = int(index_df.end.max()) if end is None else transfer_datetime_to_tick(end)
    full_index = np.arange(data_end, start-1, -freq)
    index = full_index[(full_index >= start) & (full_index <= end)][::-1]
    start,end = int(index[0]),int(index[-1])
    idx = index_to_datetime(start, end, freq) if to_datetime else index

    try:
        col_type = data_meta_service.find_data(name).get("type").get('axes')[1].get('type')
    except:
        raise Exception(f"{name} does not exist in MongoDB")
    if col_type == "Stock":
        col = columns if columns is not None else find_fields(start, end)
    else:
        col = [col_type]
    if index_df.iat[0,4][1] == 1:
        index_df['col_list'] = [col] * len(index_df)

    index_df = index_df[((index_df.start >= start) & (index_df.end <= end)) | ((index_df.start <= end) & (index_df.end > end)) | (
                (index_df.start < start) & (index_df.end >= start)) | ((index_df.start <= start) & (index_df.end >= end))]

    if len(index_df) == 1:
        real_start = max(start,index_df.iat[0,1])
        bytes_to_start = ((real_start - index_df.iat[0,1]) / freq) * index_df.iat[0,4][1] * 8
        real_end = min(end,index_df.iat[0,2])
        length = int(((real_end - real_start) /freq +1) * index_df.iat[0,4][1] * 8)
        data = form_df(index_df.iat[0,0], length, int(bytes_to_start), index_df.iat[0,4],np.arange(real_start,real_end+1,freq), index_df.iat[0,3],col)
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
            data.index = idx if to_datetime else index

            return data


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
    if len(axes) == 0 or len(axes) == 1:
        return pickle.loads(read_from_object(name, max_size, 0))
    elif len(axes) == 2:
        freq = axes[0].get("freq") if freq is None else freq
        return read_df(name=name, start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime)
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
                    res.append(read_df(name=i, start=start, end=end, freq=freq, columns=columns, to_datetime=to_datetime))
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

def update_single_data(name:str, data: pd.DataFrame, freq:int):
    try:
        index_df = read_index_df(name)
    except:
        raise Exception(f"{name} not exist")

    last_object_name = index_df.file_name.iloc[-1]
    size = get_size(last_object_name)

    if isinstance(data.index, pd.DatetimeIndex):
        data.index = datetime_conversion.datetime2tick_by_range(data.index[0], data.index[-1], freq)

    if size > max_size:
        res = write_df(name, data, freq)
        res_index = 0

    else:
        if all(data.columns.isin(index_df.col_list.iloc[-1])):
            data = data.reindex(columns=index_df.col_list.iloc[-1], copy=False)
            bytes_to_start = int(((data.index[-1] - index_df.iat[-1,1]) / freq) * index_df.iat[-1,4][1] * 8)
            res = write_to_object(last_object_name, data.values.tobytes(), bytes_to_start)

        else:
            united_col = sorted(index_df.col_list.iloc[-1].union(data.columns).tolist())
            original_data = form_df(last_object_name,max_size,0,index_df.iat[-1,4],np.arange(index_df.iat[-1,1],index_df.iat[-1,2]+1,freq),index_df.col_list.iloc[-1],united_col)
            data = data.reindex(columns=united_col, copy=False)
            data = concat_dfs([original_data, data], axis=0)
            res = write_to_object(last_object_name, data.values.tobytes(), 0)
            index_df.iat[-1, 3] = united_col

        index_df.iat[-1,2] = int(data.index[-1])
        index_df.iat[-1,4] = (int((index_df.iat[-1,2]-index_df.iat[-1,1])/freq+1), len(index_df.iat[-1,3]))
        res_index = update_index_df(name, index_df.iloc[[-1]])

    if sum([res, res_index]) != 0:
        raise Exception(f"{name} update failed")
    return 0


def delete(name: str):

    mongo_data = data_meta_service.reset_eff(name)
    if mongo_data is False:
        raise Exception(f"{name} reset eff failed")
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
    close = fetch_data("close")["close"]
    index_df = close.notna().astype(int)
    index_df = dump_single_df(index_df)
    write_to_object(total_index_df, index_df, offset=0)

if __name__ == '__main__':
    # def get_basis_data_map():
    #     res = requests.get(f"http://172.17.101.48:8001/api/v1/datum_api/sourcedata_in_tfdb")
    #     res = res.json().get("data")
    #     return [i.get("name") for i in res]
    # basic_data = get_basis_data_map()
    # not_wanted = ('_l1', '_l2')
    # ll = [data for data in basic_data if all(index not in data for index in not_wanted)]
    # ll = sorted(ll)
    # lll = ['market_order_min','proceeds_from_sub_to_mino_s','CPI_city','CPI_countryside','CashDiviRMB_3y_mean','ci_minority_owners','limit_order_min']
    #
    # from tqdm import *
    # for i in tqdm(ll):
    #     if i not in lll:
    #     data = pickle.loads(read_from_object(i, max_size, 0))
    #     data['file_name'] = data['file_name']+'_'+data['end'].astype(str)
    #     if i not in lll:
    #         data.iat[-1,0] = data.iat[-1,0][:data.iat[-1,0].rfind('_')]+'_17849900'
    #     write_to_object(i, pickle.dumps(data), 0)
    # pd.set_option('display.max_columns', 10)
    import time
    start = time.time()
    print(read('open',to_datetime=True))
    print(time.time()-start)