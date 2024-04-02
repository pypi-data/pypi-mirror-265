import database
import pymongo
import pytz

from model.trade_day import TradeDayMapping
from repo.mongo_trade_day_repo import MongoTradeDayRepo
from radosdb.config.config import parse_config
import radosdb
radosdb_config = parse_config("radosdb", path=radosdb.config)
mongo_config = radosdb_config["mongo"]
mongo_url = mongo_config["url"]
db_name = mongo_config["db_name"]
dev_client = pymongo.MongoClient(mongo_url)
mongodb = dev_client[db_name]

trade_day_repo = MongoTradeDayRepo(mongodb)

tfdb = database.TFDB()
start = 0

while True:
    dt = tfdb.select_trade_date(start).astimezone(pytz.timezone("Asia/Shanghai"))
    # print(dt)
    trade_day_repo.save_trade_day([TradeDayMapping(start, dt)])
    start += 1


