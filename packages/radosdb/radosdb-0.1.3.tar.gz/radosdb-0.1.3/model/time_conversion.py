import datetime
import typing

import numpy as np
import pandas as pd

from radosdb.repo.mongo_trade_day_repo import MongoTradeDayRepo


class DatetimeConversion:
    def __init__(self, trade_day_repo: MongoTradeDayRepo):
        self.trade_day_repo = trade_day_repo

    def query_trade_days(self, start_d: int, end_d: int) -> typing.List[datetime.datetime]:
        return self.trade_day_repo.find_by_range(start_d, end_d)

    @staticmethod
    def tick2dpmt(tick: int) -> typing.Tuple[int, int, int, int]:
        d, tick = divmod(tick, 4840)
        p, tick = divmod(tick, 2420)
        m, tick = divmod(tick, 20)
        t = tick
        return d, p, m, t

    def tick2datetime(self, tick: int) -> datetime.datetime:
        d, p, m, t = self.tick2dpmt(tick)
        mapping = self.trade_day_repo.find_by_day(d)
        time = self.pmt2time(p, m, t)
        return datetime.datetime.combine(mapping.real_date, time)

    def datetime2tick(self, dt: datetime.datetime|pd.Timestamp) -> int:
        trade_day = self.trade_day_repo.find_by_real_date(dt).day
        _, tick = DatetimeConversion.time2tick(dt)
        return trade_day * 4840 + tick

    def datetime2tick_by_range(self, start: datetime.datetime, end: datetime.datetime, period: int) -> np.ndarray:
        start,end = self.datetime2tick(start),self.datetime2tick(end)
        return np.arange(start,end+1,period,dtype=int)

    def tick2datetime_by_range(self, start, end, period, mappings) -> typing.List[datetime.datetime]:
        mappings_map = {m.day: m.real_date for m in mappings}
        tick = start
        result = []
        while tick < end:
            d, p, m, t = self.tick2dpmt(tick)
            result.append(datetime.datetime.combine(mappings_map[d], self.pmt2time(p, m, t)))
            tick += period
        return result

    @staticmethod
    def pmt2time(p, m, t):
        if p == 0:
            m += 30
            _hour = 9
        elif p == 1:
            _hour = 13
        else:
            raise ValueError("Invalid time point(p)")

        hour, minute = divmod(m, 60)
        hour += _hour
        second = t * 3
        return datetime.time(hour=hour, minute=minute, second=second)

    @staticmethod
    def time2tick(
            ts: str or datetime.datetime or datetime.timedelta or int,
            forward: typing.Optional[bool] = True,
    ) -> tuple[int, int]:
        if isinstance(ts, str):
            ts = ts.strip()
            ts = DatetimeConversion.ftype_to_realtime(ts)
            ts = datetime.datetime.strptime(ts, "%H:%M:%S")
        if isinstance(ts, datetime.datetime):
            ts = ts - datetime.datetime(ts.year, ts.month, ts.day, 9, 30)
        elif isinstance(ts, datetime.time):
            today = datetime.datetime.today()
            ts = datetime.datetime.combine(today, ts) - datetime.datetime.combine(today, datetime.time(9, 30))
        if isinstance(ts, datetime.timedelta):
            ts = ts.total_seconds()
        if isinstance(ts, float):
            ts = int(ts)
        cross_date = 0

        if ts < 0:  # 小于开盘时间
            if forward is None:
                raise Exception(f"时间非法：{ts}")
            if forward:
                cross_date -= 1
                ts = 331 * 60
            else:
                ts = 0
        if ts > 121 * 60 - 3:
            if ts < 210 * 60:  # 中午休市时间范围
                if forward is None:
                    raise Exception(f"时间非法：{ts}")
                if forward:
                    ts = 121 * 60 - 3
                else:
                    ts = 121 * 60
            else:
                ts -= 89 * 60
        if ts > 242 * 60 - 3:  # 大于收盘时间
            if forward is None:
                raise Exception(f"时间非法：{ts}")
            if forward:
                ts = 242 * 60 - 3
            else:
                cross_date += 1
                ts = 0

        ts, r = divmod(ts, 3)
        if r > 0:
            if forward is None:
                raise Exception(f"时间非法：{ts}")
            if not forward:
                ts += 1

        return cross_date, ts
    @staticmethod
    def ftype_to_realtime(ftype: str) -> str:
        return {
            "startday": "09:30:00",
            "midday": "11:30:00",
            "endday": "15:00:00",
            "minute": "09:30:00",
        }.get(ftype.lower(), ftype)
