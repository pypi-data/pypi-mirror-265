from unittest import TestCase

import pymongo

from radosdb.model.trade_day import TradeDayMapping
from radosdb.repo.mongo_trade_day_repo import MongoTradeDayRepo
from radosdb.service.trade_day_service import TradeDayService


class TestTradeDayService(TestCase):
    def setUp(self):
        mongo_url = "mongodb://root:techfinsd@172.18.10.14:27017/?authMechanism=SCRAM-SHA-1"
        db_name = "testcase_dbv2"
        dev_client = pymongo.MongoClient(mongo_url)
        self.db = dev_client[db_name]
        self.repo = MongoTradeDayRepo(self.db)
        self.mappings = [
            TradeDayMapping(0, "2009-01-05"),
            TradeDayMapping(1, "2009-01-06"),
            TradeDayMapping(2, "2009-01-07"),
            TradeDayMapping(3, "2009-01-10"),
            TradeDayMapping(4, "2009-01-11"),
        ]

        self.service = TradeDayService(self.repo)
        self.repo.save_trade_day(self.mappings)

    def test_find_near(self):
        self.assertEqual(
            TradeDayMapping(2, "2009-01-07"),
            self.service.find_near("2009-01-08", forward=True)
        )
        self.assertEqual(
            TradeDayMapping(3, "2009-01-10"),
            self.service.find_near("2009-01-08", forward=False)
        )
