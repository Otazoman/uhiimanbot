import pathlib
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

import testdata.database_test_data as database_test_data
from sqlalchemy import Integer, String

sys.path.append("..")
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from libs.databases.sqloperate import MySQLDatabase, PostgreSQLDatabase, SQLiteDatabase


class TestSqlOperate(TestCase):
    tablename = "users"
    testtitles = database_test_data.testtitles
    conditions = database_test_data.conditions

    """ 試験データ準備 """

    def setup(self):
        db = SQLiteDatabase("sqlite:///:memory:")
        db.create_table(
            self.tablename, {"ID": Integer, "name": String, "salary": Integer}, "ID"
        )
        testdata = database_test_data.testdata
        for data in testdata:
            db.insert(self.tablename, data)
        return db

    """ データベース接続 """

    def test_connection(self):
        engine = MagicMock()
        dbs = [
            SQLiteDatabase("sqlite:///:memory:"),
            MySQLDatabase("mysql+pymysql://user:password@hostname/dbname"),
            PostgreSQLDatabase("postgresql+psycopg2://user:password@hostname/dbname"),
        ]
        targetstrs = [
            "SQLiteDatabase",
            "MySQLDatabase",
            "PostgreSQLDatabase",
        ]
        for db, tstr in zip(dbs, targetstrs):
            with patch("sqlalchemy.create_engine") as create_engine_mock:
                create_engine_mock.return_value = engine
                condb = db
                print(tstr + "--->>>")
                self.assertIn(tstr, str(type(condb)))

    """ テーブル作成 """

    def test_create_table(self):
        db = SQLiteDatabase("sqlite:///:memory:")
        db.create_table(
            self.tablename, {"ID": Integer, "name": String, "salary": Integer}, "ID"
        )
        expecteddata = {"ID": 1, "name": "山田太郎", "salary": 400000}
        db.insert(self.tablename, expecteddata)
        result = db.find(self.tablename, {})
        self.assertEqual(result[0], expecteddata)

    """ 件数カウント """

    def test_count(self):
        countdb = self.setup()
        countsdata = database_test_data.countsdata
        for testtitle, condition, count in zip(
            self.testtitles, self.conditions, countsdata
        ):
            print(testtitle + "-->>>")
            result = countdb.count(self.tablename, condition)
            self.assertEqual(result, count)

    """ 検索 """

    def test_find(self):
        finddb = self.setup()
        expectedresults = database_test_data.find_expected_results
        for testtitle, condition, expectedresult in zip(
            self.testtitles, self.conditions, expectedresults
        ):
            print(testtitle + "-->>>")
            result = finddb.find(self.tablename, condition)
            self.assertEqual(result, expectedresult)

    """ 更新 """

    def test_update(self):
        testtitles = database_test_data.update_test_titles
        conditions = database_test_data.update_conditions
        values = database_test_data.replacements_values
        expectedresults = database_test_data.update_expected_results
        for testtitle, condition, value, expectedresult in zip(
            testtitles, conditions, values, expectedresults
        ):
            updatedb = self.setup()
            beforedata = updatedb.find(self.tablename, {})
            updatedb.update(self.tablename, condition, value)
            afterdata = updatedb.find(self.tablename, {})
            print(testtitle + "-->>>")
            diffvalue = [item for item in afterdata if item not in beforedata]
            self.assertEqual(expectedresult, diffvalue)

    """ 挿入 """

    def test_insert(self):
        print("\nNew data -->>")
        expecteddata = [
            {"ID": 1, "name": "山田太郎", "salary": 400000},
            {"ID": 2, "name": "田中一郎", "salary": 500000},
        ]
        db = SQLiteDatabase("sqlite:///:memory:")
        db.create_table(
            self.tablename, {"ID": Integer, "name": String, "salary": Integer}, "ID"
        )
        print("\nNew -->>>")
        db.insert(self.tablename, expecteddata[0])
        result = db.find(self.tablename, {})
        self.assertEqual(result[0], expecteddata[0])
        print("Add -->>>")
        db.insert(self.tablename, expecteddata[1])
        result = db.find(self.tablename, {})
        self.assertEqual(result, expecteddata)

    """ 削除 """

    def test_delete(self):
        expectedresults = database_test_data.delete_expected_results
        for testtitle, condition, expectedresult in zip(
            self.testtitles, self.conditions, expectedresults
        ):
            deletedb = self.setup()
            deletedb.delete(self.tablename, condition)
            afterdata = deletedb.find(self.tablename, {})
            print(testtitle + "-->>>")
            self.assertEqual(expectedresult, afterdata)
