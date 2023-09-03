import pathlib
import sys
from unittest import TestCase

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")

from unittest.mock import MagicMock, patch

from libs.datacrud import Datacrud


class TestDatacrud(TestCase):
    filepath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/output.db"
    mode = "test"
    destinationtype = "text"

    def setUp(self):
        self.datacrud = Datacrud(mode="test", destinationtype="mock")
        self.data = {"no": "sample", "sampledata": "sample"}
        self.mock_db = MagicMock()

    """データ挿入"""

    def test_create_data(self):
        # それぞれのメソッドを実行できているかを確認
        print("\nCall Method-->>")
        with patch.object(self.datacrud, "db", self.mock_db):
            self.datacrud.create_data(self.data)
            if self.datacrud.destinationtype == "mongo":
                self.mock_db.insertmany.assert_called_once_with([self.data])
            elif self.datacrud.destinationtype in ["mysql", "postgre"]:
                self.mock_db.insert.assert_called_once_with(
                    self.datacrud.table, [self.data]
                )
            elif self.datacrud.destinationtype == "text":
                self.mock_db.text_create.assert_called_once_with([self.data])
        # テキストの書込みを行えるかを確認
        print("Sample execution -->>")
        textcreate = Datacrud(self.mode, self.destinationtype)
        textcreate.create_data(self.data)
        with open(self.filepath, mode="r+") as f:
            text = f.read()
            self.assertIn("no", text)
            f.truncate(0)
        # 例外を発生させる
        print("Exception -->>")
        with self.assertRaises(Exception, msg="create data exception!!"):
            data = {"aaa", {}}
            textcreate.create_data(data)

    """ データ検索 """

    def test_read_data(self):
        # それぞれのメソッドを実行できているかを確認
        print("\nCall Method-->>")
        search_condition = {}
        with patch.object(self.datacrud, "db", self.mock_db):
            self.datacrud.read_data(self.data)
            if self.datacrud.destinationtype == "mongo":
                self.mock_db.find.assert_called_once_with([search_condition])
            elif self.datacrud.destinationtype in ["mysql", "postgre"]:
                self.mock_db.find.assert_called_once_with(
                    self.datacrud.table, [search_condition]
                )
            elif self.datacrud.destinationtype == "text":
                self.mock_db.text_read.assert_called_once_with([search_condition])
        # テキストモードで実行して成功することを確認
        print("Sample execution -->>")
        read = Datacrud(self.mode, self.destinationtype)
        read.create_data(self.data)
        result = read.read_data(search_condition)
        self.assertTrue(any("no" in item for item in result))
        with open(self.filepath, mode="r+") as f:
            f.truncate(0)
        # 例外を発生させる
        print("Exception -->>")
        with self.assertRaises(Exception, msg="read data exception!!"):
            data = {"aaa", {}}
            read.read_data(data)

    """ データ更新 """

    def test_update_data(self):
        print("\nCall Method-->>")
        search_condition = {}
        update_condition = {
            "$set": {"values": {"sampledata": "dataupdate"}},
        }
        with patch.object(self.datacrud, "db", self.mock_db):
            self.datacrud.update_data(search_condition, update_condition)
            if self.datacrud.destinationtype == "mongo":
                self.mock_db.update_many.assert_called_once_with(
                    search_condition, update_condition
                )
            elif self.datacrud.destinationtype in ["mysql", "postgre"]:
                self.mock_db.find.assert_called_once_with(
                    self.datacrud.table, search_condition, update_condition
                )
            elif self.datacrud.destinationtype == "text":
                self.mock_db.text_update.assert_called_once_with(
                    search_condition, update_condition
                )
        # テキストモードで実行して成功することを確認
        print("Sample execution -->>")
        update = Datacrud(self.mode, self.destinationtype)
        update.create_data(self.data)
        update.update_data(search_condition, update_condition)
        result = update.read_data(search_condition)
        self.assertTrue(any("no" in item for item in result))
        with open(self.filepath, mode="r+") as f:
            f.truncate(0)
        # 例外を発生させる
        print("Exception -->>")
        with self.assertRaises(Exception, msg="update data exception!!"):
            data = {"aaa", {}}
            update.update_data(data)

    """ データ削除 """

    def test_delete_data(self):
        # それぞれのメソッドを実行できているかを確認
        print("\nCall Method-->>")
        delete_condition = {}
        with patch.object(self.datacrud, "db", self.mock_db):
            self.datacrud.delete_data(self.data)
            if self.datacrud.destinationtype == "mongo":
                self.mock_db.delete_many.assert_called_once_with([delete_condition])
            elif self.datacrud.destinationtype in ["mysql", "postgre"]:
                self.mock_db.delete.assert_called_once_with(
                    self.datacrud.table, [delete_condition]
                )
            elif self.datacrud.destinationtype == "text":
                self.mock_db.text_delete.assert_called_once_with([delete_condition])
        # テキストモードで実行して成功することを確認
        print("Sample execution -->>")
        delete = Datacrud(self.mode, self.destinationtype)
        delete.create_data(self.data)
        delete.delete_data(delete_condition)
        delete.read_data(delete_condition)
        with open(self.filepath, mode="r+") as f:
            text = f.read()
            self.assertEqual("[]", text)
            f.truncate(0)
        # 例外を発生させる
        print("Exception -->>")
        with self.assertRaises(Exception, msg="delete data exception!!"):
            data = {"aaa", {}}
            delete.delete_data(data)
