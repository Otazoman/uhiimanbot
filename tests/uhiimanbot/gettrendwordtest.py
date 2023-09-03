import datetime
import pathlib
import sys
from unittest import TestCase

sys.path.append("..")
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")

from libs.configreader import Configreader
from uhiimanbot.gettrendwords import GetTrendWords


class TestGetTrendWords(TestCase):
    mode = "test"
    destinationtype = "text"
    trendwords = GetTrendWords(mode)
    configreader = Configreader()
    todaystr = datetime.datetime.now().strftime("%Y-%m-%d")
    twitterauth = configreader.get_snsauth("twitter")

    # """ Twitter トレンド """
    # def test_get_trends_twitter(self):
    #     twitter = OAuth1Session(
    #         self.twitterauth["consumer_key"],
    #         self.twitterauth["consumer_secret"],
    #         self.twitterauth["token"],
    #         self.twitterauth["token_secret"],
    #     )
    #     # 日本のトレンド取得
    #     print("\n-->> JapanTwitterTrends")
    #     location = {"id": 23424856}
    #     result = self.trendwords.get_trends_twitter(twitter, location)
    #     feeddaylist = [x["published"] for x in result]
    #     datecheck = any(self.todaystr in f for f in feeddaylist)
    #     self.assertIsInstance(result, list) and self.assertTrue(datecheck)
    #     # アメリカのトレンド取得
    #     print("-->> AmericaTwitterTrends")
    #     location = {"id": 23424977}
    #     result = self.trendwords.get_trends_twitter(twitter, location)
    #     feeddaylist = [x["published"] for x in result]
    #     datecheck = any(self.todaystr in f for f in feeddaylist)
    #     self.assertIsInstance(result, list) and self.assertTrue(datecheck)
    #     # 　不正な値
    #     print("-->> Exception")
    #     location = {"id": 999999}
    #     with self.assertRaises(Exception, msg="twittertrends exception!!"):
    #         self.trendwords.get_trends_twitter(twitter, location)

    """ Googleトレンド """

    def test_get_trends_gtrend(self):
        # 日本のトレンド取得
        print("\n-->> JapanGoogleTrends")
        jp_trendsurl = (
            "https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=JP"
        )
        result = self.trendwords.get_trends_gtrend(jp_trendsurl)
        feeddaylist = [x["published"] for x in result]
        datecheck = any(self.todaystr in f for f in feeddaylist)
        self.assertIsInstance(result, list) and self.assertTrue(datecheck)
        # アメリカのトレンド取得
        print("-->> AmericaTwitterTrends")
        us_trendsurl = (
            "https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=US"
        )
        result = self.trendwords.get_trends_gtrend(us_trendsurl)
        feeddaylist = [x["published"] for x in result]
        datecheck = any(self.todaystr in f for f in feeddaylist)
        self.assertIsInstance(result, list) and self.assertTrue(datecheck)

    """ メイン関数のテスト """

    def test_main(self):
        # 正常ケース
        print("\n-->> RegularCase")
        result = self.trendwords.main()
        feeddaylist = [x["published"] for x in result]
        datecheck = any(self.todaystr in f for f in feeddaylist)
        self.assertIsInstance(result, list) and self.assertTrue(datecheck)
        # 不正な認証情報
        print("-->> Exception")
        twitterauth = {"id": 999999}
        with self.assertRaises(Exception, msg="get trendwords exception!!"):
            self.trendwords.main(twitterauth)
