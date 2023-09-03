import json
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from uhiimanbot.afteroperationprocessing import AfterOperationProcessing


class TestAfterOperationProcessing(TestCase):
    def setUp(self):
        self.mode = "test"
        self.destinationtype = "text"
        self.afop = AfterOperationProcessing(self.mode, self.destinationtype)

        self.database_filepath = (
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/output.db"
        )
        self.log_filepath = (
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/logs/app.log"
        )
        self.output_mail_filepath = (
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/mail.txt"
        )
        # データベース削除テスト用
        self.post_after_data = [
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
                "summary": "pixel,android,authority",
                "labelstat": "added",
                "poststatus": "POSTED",
                "trendwordstatus": "subject",
                "wordcloud": "completed",
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
                "summary": "iosipadosmacossonoma,macos,macrumors",
                "labelstat": "added",
                "poststatus": "POSTED",
            },
        ]
        self.expected_result = [
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
                "summary": "iosipadosmacossonoma,macos,macrumors",
                "labelstat": "added",
                "poststatus": "POSTED",
            },
        ]
        # エラー発生時のログ
        self.error_log_content = """
        2023-08-11T18:07:38 - libs.snspost - ERROR - 400 {"Vary": "Origin", "Access-Control-Allow-Origin": "*", "Content-Type": "application/json; charset=UTF-8", "WWW-Authenticate": "OAuth \"Facebook Platform\" \"invalid_token\" \"Invalid OAuth access token - Cannot parse access token\"", "Strict-Transport-Security": "max-age=15552000; preload", "Pragma": "no-cache", "Cache-Control": "no-store", "Expires": "Sat, 01 Jan 2000 00:00:00 GMT", "x-fb-request-id": "AueZDn_MQODuNE5sSoExuR9", "x-fb-trace-id": "B9gZjCeuiiR", "x-fb-rev": "1008017685", "X-FB-Debug": "Y86JEEz6bLT3DExOaqQbC4qvCxWMxN5fDof6LsGyVODTDo0BjvjmzY7I8stR+SHnR8dBWa6N3soCDx2vtygX6Q==", "Date": "Fri, 11 Aug 2023 09:07:38 GMT", "Alt-Svc": "h3=\":443\"; ma=86400", "Connection": "keep-alive", "Content-Length": "152"} {"error":{"message":"Invalid OAuth access token - Cannot parse access token","type":"OAuthException","code":190,"fbtrace_id":"AueZDn_MQODuNE5sSoExuR9"}}
        2023-08-11T18:09:01 - libs.snspost - ERROR - 400 {"Vary": "Origin", "Access-Control-Allow-Origin": "*", "cross-origin-resource-policy": "cross-origin", "x-app-usage": "{\"call_count\":5,\"total_cputime\":0,\"total_time\":1}", "Content-Type": "application/json; charset=UTF-8", "WWW-Authenticate": "OAuth \"Facebook Platform\" \"invalid_request\" \"An active access token must be used to query information about the current user.\"", "facebook-api-version": "v17.0", "Strict-Transport-Security": "max-age=15552000; preload", "Pragma": "no-cache", "Cache-Control": "no-store", "Expires": "Sat, 01 Jan 2000 00:00:00 GMT", "x-fb-request-id": "A5z-KCpSa1u0Uzoii5FO83s", "x-fb-trace-id": "Axa55768KV3", "x-fb-rev": "1008017685", "X-FB-Debug": "lIqoELRnnTg3+ZCdlxGqmcoLlRuC23Ko6N/Bdwm8DoF7t1z7HmtFGnCsGBeeJgjaqqYOINPEOsO/gWubpUhgsQ==", "Date": "Fri, 11 Aug 2023 09:09:01 GMT", "Alt-Svc": "h3=\":443\"; ma=86400", "Connection": "keep-alive", "Content-Length": "179"} {"error":{"message":"An active access token must be used to query information about the current user.","type":"OAuthException","code":2500,"fbtrace_id":"A5z-KCpSa1u0Uzoii5FO83s"}}
        2023-08-12T11:28:12 - uhiimanbot.gettrendwords - INFO - 処理時間:1.4937447610009258秒
        2023-08-12T11:28:13 - uhiimanbot.gettrendwords - CRITICAL - Traceback (most recent call last):
        File "/home/matarain/pythonapp/uhiimanbot/tests/uhiimanbot/../../uhiimanbot/gettrendwords.py", line 103, in main
            twitterauth["consumer_key"],
        KeyError: 'consumer_key'
        """
        # 正常時のログ
        self.normal_log_content = """
        2023-08-12T11:28:12 - uhiimanbot.gettrendwords - INFO - 処理時間:1.4937447610009258秒
        2023-08-12T11:28:12 - uhiimanbot.gettrendwords - INFO - 処理時間:1.4937447610009258秒
        2023-08-12T11:28:12 - uhiimanbot.gettrendwords - INFO - 処理時間:1.4937447610009258秒
        2023-08-12T11:28:12 - uhiimanbot.gettrendwords - INFO - 処理時間:1.4937447610009258秒
        """

    def setUpDBandClearlog(self, contents, logdetail):
        with open(self.database_filepath, mode="r+") as f:
            f.truncate(0)
        with open(self.database_filepath, mode="w") as f:
            f.write(json.dumps(contents, ensure_ascii=False))
        with open(self.output_mail_filepath, mode="r+") as f:
            f.truncate(0)
        with open(self.log_filepath, mode="w") as f:
            f.write(logdetail)

    """ 投稿済データ削除 """

    def test_submitted_post_delete(self):
        print("\n-->> RegularCase")
        self.setUpDBandClearlog(self.post_after_data, self.normal_log_content)
        self.afop.submitted_post_delete()
        with open(self.database_filepath, mode="r") as f:
            file_contents = f.read()
            result = eval(file_contents)
            self.assertEqual(result, self.expected_result)
        print("-->> exception")
        with self.assertRaises(Exception, msg="submitted post exception!!"):
            test = 1
            self.afop.submitted_post_delete(test)

    """ ログファイルの正常終了を確認する """

    def test_checked_log_normalization(self):
        titles = ["Error", "Normal"]
        logfiles = [self.error_log_content, self.normal_log_content]
        expected_results = [False, True]

        for title, logfile, expected_result in zip(titles, logfiles, expected_results):
            print("-->> " + title)
            self.setUpDBandClearlog(self.post_after_data, logfile)
            result = self.afop.checked_log_normalization()
            self.assertEqual(result, expected_result)

    """ エラーメールの送信確認 """

    def test_notification_error_sending(self):
        mailaddress = "ujimasa@hotmail.com"
        subject = "【Alert】"
        content = "CRITICAL - Traceback"
        self.setUpDBandClearlog(self.post_after_data, self.error_log_content)
        self.afop.notification_error_sending()
        with open(self.output_mail_filepath, mode="r") as f:
            mail = f.read()
        self.assertRegex(mail, mailaddress)
        self.assertRegex(mail, subject)
        self.assertRegex(mail, content)

    """ メイン関数のテスト """

    def test_main(self):
        # 正常ケース
        print("\n-->> RegularCase")
        self.setUpDBandClearlog(self.post_after_data, self.normal_log_content)
        result = self.afop.main()
        expected_result = True
        self.assertEqual(result, expected_result)
        # 例外ケース
        print("-->> Exception")
        self.setUpDBandClearlog(self.post_after_data, self.normal_log_content)
        with self.assertRaises(Exception, msg="ArticlePosting exception!!"):
            test = "aaa"
            self.afop.main(test)
