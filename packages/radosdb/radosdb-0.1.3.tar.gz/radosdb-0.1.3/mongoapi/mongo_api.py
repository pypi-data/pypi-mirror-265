import typing
import bson
import pymongo
from bson.codec_options import TypeRegistry
from pydantic.v1 import BaseSettings

import radosdb
from radosdb.config.config import parse_config

radosdb_config = parse_config("radosdb", path=radosdb.config)
mongo_config = radosdb_config['mongo']
class MongoConfig(BaseSettings):

    mongo_url = mongo_config['url']
    db_name = mongo_config['db_name']
    collection_name = mongo_config['collection_name']

class MongodbAPI:

    def __init__(self,name:str,
                 data_type:dict = None,
                 eff: int = None,
                 expression:dict = None,
                 should_update:bool = None,
                 is_perf_calculated:bool = None,
                 perfData:str = None,
                 must_store:bool = None,
                 depth:int = None):

        self.name = name
        mongo_config = MongoConfig()
        db = pymongo.MongoClient(mongo_config.mongo_url)[mongo_config.db_name]
        type_registry = TypeRegistry()
        codec_options = bson.codec_options.CodecOptions(type_registry=type_registry)
        self.db = db.with_options(codec_options=codec_options)[mongo_config.collection_name]
        self.eff = eff
        self.data_type = data_type
        self.should_update = should_update
        self.is_perf_calculated = is_perf_calculated
        self.perfData = perfData
        self.must_store = must_store
        self.depth = depth
        self.expression = expression
        self.data = self.generate_data()


    def generate_data(self):

        return {
            "id": self.name,
            "refName": self.name,
            "namespaces": {},
            "type":self.data_type,
            "eff": self.eff,
            "expression": self.expression,
            "shouldUpdate": self.should_update,
            "isPerfCalculated": self.is_perf_calculated,
            "mustStore": self.must_store,
            "perfData": self.perfData,
            "depth": self.depth
        }

    def update_eff(self,eff):
        return self.db.update_one({"id": self.name}, {"$set": {"eff": eff}})

    def update_type(self,type):
        return self.db.update_one({"id": self.name}, {"$set": {"type": type}})

    def insert_data(self):
        return self.db.replace_one({"id": self.name}, self.data, upsert=True)

    def find_data(self):
        return self.db.find_one({"id": self.name})
    def delete_data(self):
        return self.db.delete_one({"id": self.name})

    def find_null_data(self):
        return self.db.find({"type": {"$type": 10}})

if __name__ == '__main__':
    axes = {
        "date": "date",
        "code": "code"
    }
    expression = {'inputs':{'vars':[],'args':None},"functionId":None}
#     data = MongodbAPI(name="test_data",
#                         data_type="time_series",
#                         axes=axes,
#                         value_type="float",
#                         eff=0,
#                         expression=expression,
#                         should_update=True,
#                         is_perf_calculated=False,
#                         perfData="",
#                         must_store=True,
#                         depth=0
# )
#     data.insert_data()
#     lis = ['__0ee23bbf1456495a9ac8727b495c9c0a',
# '__cfe583f7beee46808843f2e5c1137e1d',
# '__b2ed3ebee4a94ddcb8c3a18944749ec2'
# '__6c5874bcc15d46a0b15c8442ec75fec8'
# '__0b9afffeb55743e8a12ffe875ff66d9b'
# '__15bdbda587ae4a41ab5ba0f3825b9ef0'
# '__7733e23913c4492dac6bd52e48ceb04a']
#     for i in lis:
    updated_type = {"axes":{"0":{"type":"Time","freq":4840,"offset":4820},"1":{"type":"STOCK"}},"valueType":"DOUBLE"}
    data = MongodbAPI(name='__283b8b6ea0594d43b3d42c2751dd8770')
    print(data.find_data())
    # for i in data.find_null_data():
    #     print(i)
        # mongo = MongodbAPI(name=i.get('id'))
        # mongo.update_type(updated_type)
    # data.delete_data()
    # import time
    # start = time.time()
    # print(data.find_data())
    # print(time.time()-start)
    # data.update_data("eff",10)
    # data.insert_data()
    # print(data.find_data())
    # data.update_data("eff",5)
    # data.insert_data()
    # print(data.find_data())
