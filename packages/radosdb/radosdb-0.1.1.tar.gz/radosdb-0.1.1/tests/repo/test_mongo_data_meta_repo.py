import unittest

import pymongo

from radosdb.repo.mongo_data_meta_repo import MongoDataMetaRepo


class TestMongoDataMetaRepo(unittest.TestCase):

    def setUp(self):
        mongo_url = "mongodb://root:techfinsd@172.18.10.14:27017/?authMechanism=SCRAM-SHA-1"
        db_name = "test_dbv2"
        dev_client = pymongo.MongoClient(mongo_url)
        self.db = dev_client[db_name]
        self.repo = MongoDataMetaRepo(self.db)

        self.test_data_name = "test_data"
        self.repo.collection.replace_one({"id": self.test_data_name}, {"id": self.test_data_name, "eff": 0},
                                         upsert=True)

    def test_update_eff(self):
        self.assertEqual(self.repo.query_eff(self.test_data_name), 0)
        r = self.repo.update_max_eff(self.test_data_name, 10)
        self.assertTrue(r)
        self.assertEqual(self.repo.query_eff(self.test_data_name), 10)

        r = self.repo.update_max_eff(self.test_data_name, 5)
        self.assertFalse(r)
        self.assertEqual(self.repo.query_eff(self.test_data_name), 10)
