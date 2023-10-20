import json
import os
import pathlib
import shutil
import sys
from unittest import TestCase

import testdata.database_test_data as database_test_data

sys.path.append("..")
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from libs.databases.textoperate import TextOperator


class TestTextOperate(TestCase):

    """初期設定"""

    filepath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/output.db"
    copyfile = (
        "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/bk_output.db"
    )
    textdb = TextOperator(filepath)

    testtitles = database_test_data.testtitles
    conditions = database_test_data.conditions

    def setup(self):
        self.tearDown()
        testdata = database_test_data.testdata
        self.textdb.text_create(testdata)

    def tearDown(self):
        with open(self.filepath, mode="r+") as f:
            f.truncate(0)
        if os.path.isfile(self.copyfile):
            os.remove(self.copyfile)

    """ 件数カウント """

    def test_count(self):
        self.setup()
        countsdata = database_test_data.countsdata
        for testtitle, condition, count in zip(
            self.testtitles, self.conditions, countsdata
        ):
            print(testtitle + "-->>>")
            result = self.textdb.text_count(condition)
            self.assertEqual(result, count)

    """ 検索 """

    def test_find(self):
        self.setup()
        expectedresults = database_test_data.find_expected_results
        for testtitle, condition, expectedresult in zip(
            self.testtitles, self.conditions, expectedresults
        ):
            print(testtitle + "-->>>")
            result = self.textdb.text_read(condition)
            self.assertEqual(result, expectedresult)

    """ 更新 """

    def test_update(self):
        testtitles = (
            database_test_data.update_test_titles + database_test_data.add_test_titles
        )
        conditions = database_test_data.update_conditions * 2
        values = database_test_data.replacements_values + database_test_data.add_values
        expectedresults = (
            database_test_data.update_expected_results
            + database_test_data.add_expected_results
        )
        for testtitle, condition, value, expectedresult in zip(
            testtitles, conditions, values, expectedresults
        ):
            self.setup()
            shutil.copyfile(self.filepath, self.copyfile)
            self.textdb.text_update(condition, value)
            with open(self.copyfile) as f2:
                beforetext = f2.read()
                beforetextarray = eval(beforetext)
            with open(self.filepath, mode="r+") as f1:
                aftertext = f1.read()
                aftertextarray = eval(aftertext)
                f1.truncate(0)
            print(testtitle + "-->>>")
            diffvalue = [item for item in aftertextarray if item not in beforetextarray]
            self.assertEqual(expectedresult, diffvalue)

    """ 挿入 """

    def test_insert(self):
        self.tearDown()
        # 新規ケース
        print("\nNew file-->>")
        newtestcases = [
            # 1件
            [
                {"no": 1, "name": "Taro", "skill": "java"},
            ],
            # 複数件
            [
                {"no": 2, "name": "Jiro", "skill": "vb"},
                {"no": 3, "name": "Sabro", "skill": "Ruby"},
                {"no": 4, "name": "Shiro", "skill": "Python"},
            ],
        ]
        for t in newtestcases:
            self.textdb.text_create(t)
            with open(self.filepath, mode="r+") as f:
                text = f.read()
                textarray = eval(text)
                for text in textarray:
                    if len(t) > 0:
                        # print(json.dumps(textarray))
                        self.assertEqual(json.dumps(t), json.dumps(textarray))
                        f.truncate(0)

        # 上書きケース
        print("Appennd file-->>")
        appendtestcases = [
            [
                {"no": 2, "name": "Jiro", "skill": "vb"},
                {"no": 3, "name": "Sabro", "skill": "Ruby"},
                {"no": 4, "name": "Shiro", "skill": "Python"},
            ],
            # 追加分
            [
                {"no": 1, "name": "Taro", "skill": "java"},
            ],
        ]
        appendtestresult = [
            {"no": 2, "name": "Jiro", "skill": "vb"},
            {"no": 3, "name": "Sabro", "skill": "Ruby"},
            {"no": 4, "name": "Shiro", "skill": "Python"},
            {"no": 1, "name": "Taro", "skill": "java"},
        ]
        for t in appendtestcases:
            self.textdb.text_create(t)
        with open(self.filepath, mode="r+") as f:
            text = f.read()
            textarray = eval(text)
            # print(textarray)
            self.assertEqual(json.dumps(appendtestresult), json.dumps(textarray))
            f.truncate(0)

    """ 削除 """

    def test_delete(self):
        expectedresults = database_test_data.delete_expected_results

        for testtitle, condition, expectedresult in zip(
            self.testtitles, self.conditions, expectedresults
        ):
            self.setup()
            shutil.copyfile(self.filepath, self.copyfile)
            self.textdb.text_delete(condition)
            with open(self.copyfile) as f2:
                beforetext = f2.read()
                beforetextarray = eval(beforetext)
            with open(self.filepath, mode="r+") as f1:
                aftertext = f1.read()
                aftertextarray = eval(aftertext)
                f1.truncate(0)
            print(testtitle + "-->>>")
            diffvalue = [item for item in aftertextarray if item in beforetextarray]
            self.assertEqual(expectedresult, diffvalue)
            os.remove(self.copyfile)
