import bson
from bson.codec_options import TypeRegistry
from pymongo.database import Database


class MongoDataMetaRepo:

    def __init__(self,
                 db: Database,
                 collection_name,
                 ):
        type_registry = TypeRegistry()
        codec_options = bson.codec_options.CodecOptions(type_registry=type_registry)
        db = db.with_options(codec_options=codec_options)
        self.db = db

        self.collection_name = collection_name
        self.collection = self.db[self.collection_name]

    def update_max_eff(self, name, eff):
        item = self.collection.find_one_and_update(
            {"id": name, "eff": {"$lt": eff}},
            {"$set": {"eff": eff}},
            upsert=True
        )
        if item is None:
            return False
        return True

    def update_eff(self, name, eff):
        item = self.collection.update_one(
            {"id": name},
            {"$set": {"eff": eff}},
            upsert=True
        )
        return not item is None

    def reset_eff(self, name):
        return self.update_eff(name, 0)

    def query_eff(self, name):
        item = self.collection.find_one({"id": name})
        if item is None:
            return None
        return item['eff']

    def find_data(self, name):
        item = self.collection.find_one({"id": name})
        if item is None:
            return None
        return item

    def insert_data(self,
                    name: str = None,
                    data_type: dict = None,
                    eff: int = None,
                    expression: dict = None,
                    should_update: bool = None,
                    perfData: str = None,
                    must_store: bool = None,
                    depth: int = None
                    ):
        data = {
            "id": name,
            "refName": name,
            "namespaces": {},
            "type": data_type,
            "eff": eff,
            "expression": expression,
            "shouldUpdate": should_update,
            "mustStore": must_store,
            "perfData": perfData,
            "depth": depth
        }
        item = self.collection.replace_one({"id": name}, data, upsert=True)
        return not item is None
