import unittest

import pandas as pd
import pymongo

from radosdb.model.trade_day import TradeDayMapping
from radosdb.repo.mongo_trade_day_repo import MongoTradeDayRepo


class TestMongoTradeDayRepo(unittest.TestCase):

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


    def test_save(self):
        self.repo.save_trade_day(self.mappings)

    def test_find_by_day(self):
        mapping = self.repo.find_by_day(1)
        print(mapping)
        self.assertEqual(mapping, TradeDayMapping(1, "2009-01-06"))

    def test_find_by_real_date(self):
        mapping = self.repo.find_by_real_date(pd.Timestamp("2009-01-05 09:30:00"))
        print(mapping)
        self.assertEqual(mapping, TradeDayMapping(0, "2009-01-05"))

