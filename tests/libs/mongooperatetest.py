import pathlib
import sys
from unittest import TestCase

import mongomock
import pymongo

sys.path.append("..")
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
import database_test_data
from libs.databases.mongooperate import MongoOperate


class TestMongoOperate(TestCase):

    """初期設定"""

    client = mongomock.MongoClient()
    db = client.db
    collection = db.collection
    testtitles = database_test_data.testtitles
    conditions = database_test_data.conditions

    def setup(self):
        self.collection.delete_many({})
        testdata = database_test_data.testdata
        self.collection.insert_many(testdata)

    """ データ作成 """

    def test_connection(self):
        # 接続テスト(ローカルにmongo入っていればOK返ってくる)
        connectiondict = {
            "host": "localhost",
            "username": "username",
            "password": "password",
            "authSource": "databasename",
            "authMechanism": "SCRAM-SHA-1",
            "dbname": "databasename",
            "collection": "collectionname",
        }
        result = MongoOperate.MongoConnect(connectiondict).connect()
        self.assertIsInstance(result, pymongo.collection.Collection, "connect=True")

    """ 件数カウント """

    def test_count(self):
        self.setup()
        m = MongoOperate.MongoCount(self.collection)
        expectedresults = database_test_data.countsdata
        for testtitle, condition, expectedresult in zip(
            self.testtitles, self.conditions, expectedresults
        ):
            print(testtitle + "-->>>")
            result = m.count(condition)
            self.assertEqual(result, expectedresult)

    """ 検索 """

    def test_find(self):
        self.setup()
        m = MongoOperate.MongoFind(self.collection)
        print("\nfind_one-->>>")
        # 条件指定(一意)
        condition = {"name": "山田太郎"}
        result = m.find_one(condition)
        self.assertTrue(result["name"] == "山田太郎")
        # 1件にならないような結果
        condition = {"name": {"$regex": "郎$"}}
        with self.assertRaises(ValueError):
            m.find_one(condition)
        print("find-->>>")

        expectedresults = database_test_data.find_expected_results
        for testtitle, condition, expectedresult in zip(
            self.testtitles, self.conditions, expectedresults
        ):
            print(testtitle + "-->>>")
            self.setup()
            if condition == {}:
                data = m.find()
                result = [
                    {k: v for k, v in item.items() if k != "_id"} for item in list(data)
                ]
            else:
                data = list(m.find(filter=condition))
                result = [
                    {k: v for k, v in item.items() if k != "_id"} for item in list(data)
                ]
            self.assertEqual(result, expectedresult)

    """ 更新 """

    def test_update(self):
        print("\nupdate_one-->>>")
        self.setup()
        m = MongoOperate.MongoUpdate(self.collection)
        testcases = [
            {
                # 条件指定(一意)
                "condition": {"name": "山田太郎"},
                "update": {"$set": {"salary": 100000}},
            },
            {
                # 1件にならないような結果
                "condition": {"name": {"$regex": "郎$"}},
                "update": {"$set": {"salary": 100000}},
            },
            {
                # 指定なし
                "condition": {},
                "update": {"$set": {"salary": 100000}},
            },
        ]
        for t in testcases:
            condition = t["condition"]
            update = t["update"]
            result = m.update_one(condition, update)
            self.assertTrue(result.raw_result["updatedExisting"])
        print("update_many-->>>")
        testcases = [
            {
                # 条件指定(一意)
                "condition": {"name": "山田太郎"},
                "update": {"$set": {"salary": 300000}},
                "result": 1,
            },
            {
                # 特定値以上
                "condition": {"ID": {"$gte": 4}},
                "update": {"$set": {"salary": 30}},
                "result": 3,
            },
            {
                # 正規表現
                "condition": {"name": {"$regex": "郎$"}},
                "update": {"$set": {"salary": 600000}},
                "result": 4,
            },
            {
                # 条件指定なし
                "condition": {},
                "update": {"$set": {"salary": 120000}},
                "result": 6,
            },
        ]
        for t in testcases:
            condition = t["condition"]
            update = t["update"]
            result = m.update_many(condition, update)
            self.assertEqual(result.matched_count, t["result"])
        print("replace_one-->>>")
        testcases = [
            {
                # 条件指定(一意)
                "condition": {"name": "山田太郎"},
                "update": {
                    "fullname": "山田　太郎",
                    "rank": 5,
                    "profession": "Engineer",
                    "position": "Manager",
                },
            },
            {
                # 1件にならないような場合
                "condition": {"name": {"$regex": "郎$"}},
                "update": {
                    "fullname": "田中　一郎",
                    "rank": 5,
                    "profession": "Engineer",
                    "position": "Manager",
                },
            },
        ]
        for t in testcases:
            self.setup()
            m = MongoOperate.MongoUpdate(self.collection)
            condition = t["condition"]
            update = t["update"]
            result = m.replace_one(condition, update)
            self.assertTrue(result.raw_result["updatedExisting"])
        print("find_one_and_replace-->>>")
        testcases = [
            {
                # 条件指定(一意)
                "condition": {"name": "山下一郎"},
                "update": {
                    "fullname": "山下　太郎",
                    "rank": 1,
                    "profession": "Engineer",
                    "position": "tester",
                },
                "assert": "self.assertTrue(\
                    filter(\
                          lambda x: '山下一郎'\
                          in x, result\
                            )\
                    )",
            },
            {
                # 1件にならないような場合
                "condition": {"name": {"$regex": "郎$"}},
                "update": {
                    "fullname": "田中　一郎",
                    "rank": 5,
                    "profession": "Engineer",
                    "position": "Manager",
                },
                "assert": "self.assertTrue(\
                    filter(\
                        lambda x: '山田太郎'\
                        in x, result\
                            )\
                    )",
            },
        ]
        for t in testcases:
            self.setup()
            m = MongoOperate.MongoUpdate(self.collection)
            condition = t["condition"]
            update = t["update"]
            result = m.find_one_and_replace(condition, update)
            eval(t["assert"])

    """ 作成 """

    def test_insert(self):
        m = MongoOperate.MongoInsert(self.collection)
        print("\ninsert_one-->>>")
        testcases = [
            # 0件
            {},
            # 1件
            {"no": 1, "name": "Taro", "skill": "java"},
            # 複数件
            [
                {"no": 2, "name": "Jiro", "skill": "vb"},
                {"no": 3, "name": "Sabro", "skill": "Ruby"},
                {"no": 4, "name": "Shiro", "skill": "Python"},
            ],
        ]
        for t in testcases:
            if isinstance(t, dict):
                result = m.insert_one(t)
                self.assertTrue(result.acknowledged)
            else:
                with self.assertRaises(TypeError):
                    m.insert_one(t)
        MongoOperate.MongoDelete(self.collection).delete_many({})
        print("insert_many-->>>")
        for t in testcases:
            if len(t) > 1:
                if isinstance(t, list):
                    result = m.insert_many(t)
                    self.assertTrue(result.acknowledged)
                else:
                    li = [t]
                    result = m.insert_many(li)
                    self.assertTrue(result.acknowledged)
            else:
                with self.assertRaises(TypeError):
                    m.insert_many(t)

    """ 削除 """

    def test_delete(self):
        m = MongoOperate.MongoDelete(self.collection)
        print("\ndelete_one-->>>")
        self.setup()
        testcases = [
            # 1件
            {"name": "山田太郎"},
            # 特定値以上
            {"ID": {"$gte": 4}},
            # 正規表現
            {"name": {"$regex": "郎$"}},
            # 条件なし
            {},
            # 複数件
            [
                {"no": 2, "name": "Jiro", "skill": "vb"},
                {"no": 3, "name": "Sabro", "skill": "Ruby"},
                {"no": 4, "name": "Shiro", "skill": "Python"},
            ],
        ]
        for t in testcases:
            if isinstance(t, dict):
                result = m.delete_one(t)
                self.assertTrue(result.acknowledged)
            else:
                with self.assertRaises(TypeError):
                    m.delete_one(t)
        print("delete_many-->>>")
        self.setup()
        for t in testcases:
            self.setup()
            if isinstance(t, dict):
                result = m.delete_many(t)
                self.assertTrue(result.acknowledged)
            else:
                with self.assertRaises(TypeError):
                    m.delete_many(t)
