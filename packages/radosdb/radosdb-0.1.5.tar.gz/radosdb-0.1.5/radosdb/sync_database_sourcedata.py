import requests
import argparse
import numpy as np
import datetime

from ddp import  TFDBConnection
from tdata import fetch_data
FIRE_ADDRESS = 'http://172.18.10.161:8080'

def get_effectivePtr():
    db = TFDBConnection()
    return db.get_dpmt(input_datetime=date + " 15:00:00", freq="M")


def _get_basis_data_map():
    res = requests.get(f"http://172.17.101.48:8001/api/v1/datum_api/sourcedata_in_tfdb")
    res = res.json().get("data")
    return [i.get("name") for i in res]


def log(name, effectivePtr):
    try:
        r = requests.post(f"{FIRE_ADDRESS}/run/root", json={"dataId": name, "effectivePtr": effectivePtr})
    except Exception as e:
        print(f"[{name}]推送结果：", e)


def main():
    effectivePtr = get_effectivePtr()
    need = [data for data in _get_basis_data_map() if not data.endswith(("_l1", "_l2"))]

    for name in need:
        df = fetch_data(name, date, date)[name]
        df = df.replace(np.nan, "null")
        df.index = df.index.strftime("%Y-%m-%d %H:%M:%S")
        data = df.to_dict()
        r = requests.put(f"http://172.17.101.203:50051/name/{name}", json=data)
        if r.status_code != 200:
            print(f"{name} 同步失败: status_code: {r.status_code}, result: {r.text}")
        else:
            log(name, effectivePtr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trade_date", "-d", default=str('2024-03-28'))
    args = parser.parse_args()
    date = args.trade_date
    # main()
    print(get_effectivePtr())

    #
    # def get_basis_data_map():
    #     res = requests.get(f"http://172.17.101.48:8001/api/v1/datum_api/sourcedata_in_tfdb")
    #     res = res.json().get("data")
    #     return [i.get("name") for i in res]
    # basic_data = get_basis_data_map()
    # not_wanted = ('_l1', '_l2')
    # ll = [data for data in basic_data if all(index not in data for index in not_wanted)]
    # ll = sorted(ll)
 #    ll = ['cd_cl_min',
 # 'cd_hi_min',
 # 'cd_lo_min',
 # 'cd_mn_min',
 # 'cd_op_min',
 # 'cd_vl_min',
 # 'cj_close_min',
 # 'cj_high_min',
 # 'cj_low_min',
 # 'cj_money_min',
 # 'cj_open_min',
 # 'cj_volume_min',
 # 'cj_vwap_min',
 # 'wt_cl_min',
 # 'wt_hi_min',
 # 'wt_lo_min',
 # 'wt_mn_min',
 # 'wt_op_min',
 # 'wt_vl_min'
 # 'close_min',
 # 'high_min',
 # 'low_min',
 # 'money_min',
 # 'open_min',
 # 'volume_min',
 # 'vwap_min']
 #    eff = get_effectivePtr()
 #    from tqdm import tqdm
 #
 #    for i in tqdm(ll):
 #        log(i, eff)
