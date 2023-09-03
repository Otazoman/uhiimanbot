import datetime
import itertools
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.datacrud import Datacrud
from uhiimanbot.targetinformationacquisition import TargetInformationAcquisition


class TestTargetInformationAcquisitiontest(TestCase):
    mode = "test"
    destinationtype = "text"
    targetinformationacquisition = TargetInformationAcquisition(mode, destinationtype)
    datacrud = Datacrud(mode, destinationtype)
    todaystr = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterdaystr = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    filepath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/output.db"

    """  RSSフィードを取得する """

    def test_get_rssfeed(self):
        feedlist = [
            # 日本語パターン
            {
                "name": "gcpタグが付けられた新着投稿 - Qiita",
                "feedurl": "https://qiita.com/tags/gcp/feed.atom",
                "category": "GCP",
            },
            # 英語パターン
            {
                "name": "DEV Community",
                "feedurl": "https://dev.to/feed",
                "category": "海外TECH",
            },
            #
            {
                "name": "気になる、記になる…",
                "feedurl": "https://taisy0.com/feed",
                "category": "IT",
            },
        ]
        # キー値チェック
        keys = [
            "name",
            "category",
            "title",
            "description",
            "link",
            "orgdescription",
            "orgpublished",
            "published",
            "updated",
        ]
        # 取得したデータの確認
        print("\nformatcheck -->>")
        for fd in feedlist:
            results = self.targetinformationacquisition.get_rssfeed(
                fd, timedifference=24
            )
            for result in results:
                self.assertEqual(keys, list(result.keys()))
                for key in keys:
                    self.assertIsInstance(result[key], str)
        # 引数指定パターン
        print("argument -->>")
        for fd in feedlist:
            result = self.targetinformationacquisition.get_rssfeed(
                fd, timedifference=24
            )
            self.assertIsInstance(result, list, fd["name"])
        # 引数未指定
        print("no argument -->>")
        for fd in feedlist:
            result = self.targetinformationacquisition.get_rssfeed(fd)
            self.assertIsInstance(result, list, fd["name"])
        # リスト内のURLがおかしかったり空欄の場合のケース
        print("not available -->>")
        feedlist = [
            # アクセス不可
            {
                "name": "google",
                "feedurl": "https://test.tohonokai.com/tst",
                "category": "TEST",
            },
            # 空欄
            {"name": "", "feedurl": "", "category": ""},
        ]
        difflist = []
        for fd in feedlist:
            result = self.targetinformationacquisition.get_rssfeed(fd)
            self.assertEqual(result, difflist)

    """ RSSフィードを並列で取得する """

    def test_get_rssfeeds(self):
        # 当日と前日を含んでいるか
        result = list(
            itertools.chain.from_iterable(
                self.targetinformationacquisition.get_rssfeeds(settingtime=24)
            )
        )
        feeddaylist = [x["published"] for x in result]
        datecheck = any(self.yesterdaystr in f for f in feeddaylist) and any(
            self.todaystr in f for f in feeddaylist
        )
        self.assertIsInstance(result, list) and self.assertTrue(datecheck)

    """ 取得した記事データの保存 """

    def test_store_postsdata(self):
        storedata = [
            {
                "name": "気になる、記になる…",
                "category": "IT",
                "title": "Nothingの｢Phone (2)｣がUAEの認証機関を通過",
                "description": "Nothingは来月に新型スマホ Phone  を発売予定です",
                "link": "https://taisy0.com/2023/06/10/172841.html",
                "orgpublished": "Sat, 10 Jun 2023 03:29:02 +0000",
                "published": "2023-06-10 03:29:02",
                "updated": "2023-06-10 03:29:02",
            },
            {
                "name": "気になる、記になる…",
                "category": "IT",
                "title": "｢Bing｣のAIチャット、デスクトップ版もボイスチャットに対応",
                "description": "米Microsoftが  Bing の"
                "AIチャットのデスクトップ版でボイスチャットが利用可能になったことを発表しました",
                "link": "https://taisy0.com/2023/06/10/172836.html",
                "orgpublished": "Sat, 10 Jun 2023 03:12:46 +0000",
                "published": "2023-06-10 03:12:46",
                "updated": "2023-06-10 03:12:46",
            },
        ]
        store = self.targetinformationacquisition.store_postsdata(storedata)
        if store:
            condition = {}
            result = self.datacrud.read_data(condition)
            feeddaylist = [x["published"] for x in result]
            datecheck = any(self.yesterdaystr in f for f in feeddaylist) and any(
                self.todaystr in f for f in feeddaylist
            )
            self.assertIsInstance(result, list) and self.assertTrue(datecheck)
        with open(self.filepath, mode="r+") as f:
            f.truncate(0)

    """ メイン処理のテスト """

    def test_main(self):
        # 正常ケース
        print("\n-->> RegularCase")
        self.targetinformationacquisition.main()
        # 例外の確認
        print("-->> Exception")
        with self.assertRaises(
            Exception, msg="TargetInformationAcquisition exception!!"
        ):
            test = "test"
            self.targetinformationacquisition.main(test)
        with open(self.filepath, mode="r+") as f:
            f.truncate(0)
