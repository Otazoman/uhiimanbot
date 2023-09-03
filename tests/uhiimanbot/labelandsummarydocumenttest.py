import json
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.datacrud import Datacrud
from uhiimanbot.labelandsummarydocument import LabelandSummaryDocument
from uhiimanbot.targetinformationacquisition import TargetInformationAcquisition


class TestLabelandSummaryDocument(TestCase):
    mode = "test"
    destinationtype = "text"
    labelandsummarydocument = LabelandSummaryDocument(mode, destinationtype)
    targetinformationacquisition = TargetInformationAcquisition(mode, destinationtype)
    datacrud = Datacrud(mode, destinationtype)

    filepath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/output.db"
    articles = [
        {
            "name": "気になる、記になる…",
            "category": "IT",
            "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
            "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
            "link": "https://taisy0.com/2023/06/18/173142.html",
            "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
            "published": "2023-06-18 02:17:48",
            "updated": "2023-06-18 02:17:48",
            "_id": "20230618172417-1",
        },
        {
            "name": "気になる、記になる…",
            "category": "IT",
            "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
            "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
            "link": "https://taisy0.com/2023/06/18/173129.html",
            "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
            "published": "2023-06-18 01:38:21",
            "updated": "2023-06-18 01:38:21",
            "_id": "20230618172417-92",
        },
    ]

    def setup(self):
        with open(self.filepath, mode="r+") as f:
            f.truncate(0)
        with open(self.filepath, mode="w") as f:
            f.write(str(json.dumps(self.articles, ensure_ascii=False)))

    """ 保存しているRSSフィードデータ群を取得する """

    def test_get_article(self):
        print("\nNormal -->>")
        self.setup()
        results = self.labelandsummarydocument.get_article()
        self.assertEqual(self.articles, results)

    """ ラベルと要約文章を付与する """

    def test_create_labels_and_summary(self):
        print("\nNormal -->>")
        self.setup()
        with open(self.filepath, mode="r") as f:
            text = f.read()
        articles = json.loads(text)
        assumptiondatas = [
            {
                "name": "気になる、記になる…",
                "category": "IT",
                "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
                "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
                "link": "https://taisy0.com/2023/06/18/173142.html",
                "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
                "published": "2023-06-18 02:17:48",
                "updated": "2023-06-18 02:17:48",
                "_id": "20230618172417-1",
                "addlabel": ["pixel", "android", "authority"],
                "summary": ["pixel", "android", "authority"],
                "labelstat": "added",
            },
            {
                "name": "気になる、記になる…",
                "category": "IT",
                "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
                "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
                "link": "https://taisy0.com/2023/06/18/173129.html",
                "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
                "published": "2023-06-18 01:38:21",
                "updated": "2023-06-18 01:38:21",
                "_id": "20230618172417-92",
                "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
                "summary": ["iosipadosmacossonoma", "macos", "macrumors"],
                "labelstat": "added",
            },
        ]
        self.labelandsummarydocument.create_labels_and_summary(articles)
        with open(self.filepath, mode="r") as f:
            text = f.read()
        results = json.loads(text)
        self.assertEqual(assumptiondatas, results)
        print("Exception -->>")
        with self.assertRaises(Exception, msg="create_labels_and_summary exception!!"):
            articles = [{"aaaa", "aaa"}]
            self.labelandsummarydocument.create_labels_and_summary(articles)

    """ メイン関数のテスト """

    def test_main(self):
        self.setup()
        # 正常ケース
        print("\n-->> RegularCase")
        self.labelandsummarydocument.main()
        # 例外の確認
        print("-->> Exception")
        with self.assertRaises(Exception, msg="LabelandSummaryDocument exception!!"):
            test = 1
            self.labelandsummarydocument.main(test)
