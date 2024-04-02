import datetime

import bson
import pymongo
from bson.codec_options import TypeRegistry
from pymongo.database import Database
from typing import List

from radosdb.model.trade_day import TradeDayMapping


class MongoTradeDayRepo:

    def __init__(self, db: Database, collection_name: str = "trade_day"):
        type_registry = TypeRegistry()
        codec_options = bson.codec_options.CodecOptions(type_registry=type_registry)
        db = db.with_options(codec_options=codec_options)
        self.db = db

        self.collection_name = collection_name
        self.collection = self.db[self.collection_name]

    @staticmethod
    def to_model(data):
        return TradeDayMapping(day=data['_id'], real_date=data['real_date'])

    def save_trade_day(self, mappings: List[TradeDayMapping]):
        for mapping in mappings:
            self.collection.replace_one(
                {"_id": mapping.day},
                {
                    "_id": mapping.day,
                    "real_date": datetime.datetime(mapping.real_date.year,
                                                   mapping.real_date.month,
                                                   mapping.real_date.day)
                },
                upsert=True)

    def find_by_day(self, day):
        mapping = self.collection.find_one({"_id": day})
        if mapping is None:
            return None
        return self.to_model(mapping)

    def find_first_greater_than_day(self, day):
        mapping = self.collection.find_one({"real_date": {"$gte": day}},sort=[("_id", pymongo.ASCENDING)])
        if mapping is None:
            return None
        return self.to_model(mapping)

    def find_last_less_than_day(self, day):
        mapping = self.collection.find_one({"real_date": {"$lte": day},},sort=[("_id", pymongo.DESCENDING)])
        if mapping is None:
            return None
        return self.to_model(mapping)

    def find_by_range(self, start_day, end_day):
        mappings = self.collection.find({"_id": {"$gte": start_day, "$lte": end_day}})
        return [self.to_model(mapping) for mapping in mappings]

    @staticmethod
    def format_real_date(real_date):
        if isinstance(real_date, datetime.date):
            real_date = datetime.datetime(real_date.year,
                                          real_date.month,
                                          real_date.day)
        if isinstance(real_date, str):
            real_date = datetime.datetime.strptime(real_date, "%Y-%m-%d")
        return real_date

    def find_by_real_date(self, real_date):
        real_date = self.format_real_date(real_date)

        mapping = self.collection.find_one({"real_date": real_date})
        if mapping is None:
            return None
        return self.to_model(mapping)

    def find_one_gte_real_date(self, real_date):
        real_date = self.format_real_date(real_date)
        mapping = self.collection.find_one(
            {"real_date": {"$gte": real_date}},
            sort=[("real_date", pymongo.ASCENDING)],
        )
        if mapping is None:
            return None
        return self.to_model(mapping)

    def find_one_lte_real_date(self, real_date):
        real_date = self.format_real_date(real_date)
        mapping = self.collection.find_one(
            {"real_date": {"$lte": real_date}},
            sort=[("real_date", pymongo.DESCENDING)],
        )
        if mapping is None:
            return None
        return self.to_model(mapping)
