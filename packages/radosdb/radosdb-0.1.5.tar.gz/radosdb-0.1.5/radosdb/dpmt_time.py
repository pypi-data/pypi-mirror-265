import numpy as np
from tdata import query_trade_calendar
import pandas as pd

class DpmtTimeConversion:

    def __init__(self):
        self.trade_calendar = query_trade_calendar()['trade_date'].astype('str').tolist()
        self.start_date = pd.to_datetime('2009-01-05 09:30:00')
        self.start_date_idx = self.trade_calendar.index(self.start_date.strftime('%Y-%m-%d'))

    def single_dpmt_to_datetime(self, dpmt:int):
        if dpmt < 0:
            raise ValueError('dpmt should be non-negative')
        if not isinstance(dpmt, int):
            raise ValueError('dpmt should be integer')


        d = dpmt//4840
        end_date = pd.to_datetime(''.join([self.trade_calendar[self.start_date_idx+d]," 09:30:00"]))
        remainder = dpmt%4840
        minute = remainder//20
        second = remainder%20*3

        if minute > 120:
            minute += 89

        return pd.to_datetime(end_date) + pd.Timedelta(minutes=minute,seconds=second)

    # def dpmt_to_datetime(self,dpmt:list[int] | np.array(int) | pd.Series[int]):
    #     if not isinstance(dpmt, (list,np.ndarray,pd.Series)):
    #         raise ValueError('dpmt should be list, np.array or pd.Series')
    #     _dpmt = pd.Series(dpmt)
    #     _d = _dpmt//4840
    #     _end_date = pd.to_datetime(pd.Series([self.trade_calendar[self.start_date_idx+d] for d in _d])+ " 09:30:00")
    #     _remainder = _dpmt%4840
    #     _minute = _remainder//20
    #     _second = _remainder%20*3
    #     _minute[_minute > 120] += 89
    #     return _end_date + pd.to_timedelta(_minute*60+_second,unit='s')


def single_dpmt_to_datetime(dpmt:int):

    start_date = pd.to_datetime('2009-01-05 09:30:00')
    trade_calendar = query_trade_calendar()['trade_date'].astype('str').tolist()
    start_date_idx = trade_calendar.index(start_date.strftime('%Y-%m-%d'))
    d = dpmt//4840
    end_date = pd.to_datetime(''.join([trade_calendar[start_date_idx+d]," 09:30:00"]))
    remainder = dpmt%4840
    minute = remainder//20
    second = remainder%20*3

    if minute > 120:
        minute += 89

    return pd.to_datetime(end_date) + pd.Timedelta(minutes=minute,seconds=second)

def single_datetime_to_dpmt(date:pd.Timestamp):
    start_date = pd.to_datetime('2009-01-05 09:30:00')
    calendar_list = query_trade_calendar().astype('str')['trade_date'].tolist()
    start_index = calendar_list.index('2009-01-05')
    end_index = calendar_list.index(date.strftime('%Y-%m-%d'))
    days = end_index-start_index
    diff = date - start_date
    return days*4840 + diff.seconds//3

if __name__ == '__main__':
    import time
    start = time.time()
    print(single_dpmt_to_datetime(20*121))
    end = time.time()
    print(end-start)
