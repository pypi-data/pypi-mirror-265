import time
import unittest

import numpy as np
import pandas as pd

from radosdb import database_api
from tdata import *

class TestMongoDataMetaRepo(unittest.TestCase):

    def test_read(self):
        # col = fetch_data('close')['close'].columns
        s = time.time()
        data = database_api.read("__c6a74a65f3bd4ffc9cceb13f26453390",freq=4840,to_datetime=True)
        print(data)
        print(time.time()-s)

    def test_write(self):
        data = fetch_data('close_min','2022-09-20','2023-01-01')['close_min']
        s = time.time()
        database_api.write("close_min_tt",  data,freq=20)
        print(time.time()-s)

    def test_read_write_read(self):
        col = fetch_data('close')['close'].columns
        s = time.time()
        data = database_api.read("close", freq=4840, columns=col, to_datetime=True)
        print(data)
        data = data.shift(1)
        print(data)
        database_api.write("close_tttt", data, freq=4840)
        data_2 = database_api.read("close_tttt", freq=4840, columns=col, to_datetime=True)
        print(data_2)
        print(time.time() - s)
        print(data)

    def test_delete(self):
        print(database_api.delete("close_min_tt"))

    def test_database_v2(self):
        # data = fetch_data('close_min','2021-11-10','2021-12-01')['close_min']
        data = fetch_data('close_min','2024-03-22','2024-03-22')['close_min']
        print(data)
        start = time.time()
        print(database_api.write('close_min',data))
        end = time.time()
        print(end-start)

    def test_database_v2_read(self):
        start = time.time()
        data = database_api.read('__ff1dc26bc8c74b24b9f7fc5afff1c787',to_datetime=True)
        print(data)
        end = time.time()
        print(end-start)