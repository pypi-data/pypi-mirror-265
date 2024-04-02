import time

from rd import *
from rd.eva.support._utils import get_cumulative_forward_returns_v2
from rd.eva.support.utils import ForwardReturns

from database_api import index_to_datetime, read


def compute_forward_returns_v3(
    idx:int,
    start:str,
    end:str,
    datetime_index=False,
    split=False,
    action="set_zero",
):
    data = read(f'close_min_{idx}',start,end,to_datetime=True)
    stock_mark = read(f'buy_sell_min_{idx}',start,end,to_datetime=True)
    data.index = stock_mark.index = data.index.strftime('%Y-%m-%d')

    def extract(x):
        if x is not None:
            if not datetime_index:
                x.index = x.index.astype(str)
            return x

    result_long = {}
    point_1 = 1
    point_2s = [2,6,11]
    key = ['1D', '5D','10D']

    for id,point_2 in enumerate(point_2s):
        l, s = frame_wrapper_for_numba(get_cumulative_forward_returns_v2)(
            data,
            data,
            stock_mark,
            stock_mark,
            point_1,
            point_2,
            split_returns=split,
            set_nan=action == "set_zero",
        )
        result_long[key[id]] = extract(l)
    result_long = DataCube(result_long)
    return result_long

def compute_ic(data, method="spearman"):

    minute_list = pd.date_range("09:30", "11:30", freq="min").append(
        pd.date_range("13:00", "15:00", freq="min")).strftime('%H:%M').tolist()
    data_index = data.index
    day_index = data_index.strftime('%Y-%m-%d').unique()
    intraday_time = data_index.strftime('%H:%M').unique()

    def get_next_minute(intra_time):
        index = minute_list.index(intra_time)
        if index == len(minute_list)-1:
            return minute_list[0]
        else:
            return minute_list[index + 1]

    res = []
    for i in intraday_time:
        factor = data[data_index.strftime("%H:%M") == i]
        factor.index = factor.index.strftime("%Y-%m-%d")
        factor = DataCube({'factor': factor})
        next_minute = get_next_minute(i).replace(":", "")
        forward_returns = compute_forward_returns_v3(minute_list.index(i), day_index[0], day_index[-1])
        ic_data = factor.corr_with(
            forward_returns,
            method=method,
            by_date=True,
            reindex_to="self"
        )
        ic_data = ic_data[factor.keys[0]]
        ic_data.index = pd.to_datetime(ic_data.index + f'T{next_minute}')
        res.append(ic_data)
    res = concat_dfs(res, axis=0)
    res = res.reindex(sorted(res.index))
    return res


def parse_ic(ic_data):
    ic_data = ic_data[ic_data.notna().any(axis=1)]
    ic_mean = ic_data.mean()
    ic_std = ic_data.std()
    ir = ic_mean / ic_std

    ops = ["> 0", "< 0", "> 3%", "< -3%", "> 5%", "< -5%"]
    summary_table = pd.DataFrame(np.nan, index=["mean", "std", "ir"] + ops, columns=ic_data.columns)
    summary_table.loc["mean", "std", "ir"] = [ic_mean, ic_std, ir]
    ic_fnt_sum = np.isfinite(ic_data).sum()
    for op in ops:
        summary_table.loc[op] = eval(f"ic_data{op.replace('%', '/100')}").sum() / ic_fnt_sum

    return summary_table

if __name__ == '__main__':
    data = read('close',to_datetime=True)
    start = time.time()
    fr = compute_ic(data)
    print(time.time()-start)
    print(fr.sum(0))