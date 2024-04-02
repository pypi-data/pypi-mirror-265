import datetime
import typing

from radosdb.model.trade_day import TradeDayMapping
from radosdb.repo.mongo_trade_day_repo import MongoTradeDayRepo


class TradeDayService:
    def __init__(self, repo: MongoTradeDayRepo):
        self.repo = repo

    def defined(self, trade_day_mappings: dict[int, typing.Union[str, datetime.date]]):
        mappings = [TradeDayMapping(day, date) for day, date in trade_day_mappings.items()]
        self.repo.save_trade_day(mappings)
        return mappings

    def find_by_day(self, day: int):
        return self.repo.find_by_day(day)

    def find_near(self, real_date, forward:bool):
        if forward:
            return self.repo.find_one_lte_real_date(real_date)
        else:
            return self.repo.find_one_gte_real_date(real_date)

