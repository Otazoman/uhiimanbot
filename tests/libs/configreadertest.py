import pathlib
import sys
from unittest import TestCase

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from libs.configreader import Configreader

setting_file_path = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/config/test_config.yaml"
)


class TestAuthentications(TestCase):
    mode = "test"
    """ Assert Data """
    auth_blogger = {
        "client_id": "dummy.com",
        "client_secret": "blogger_clientsecret",
        "scope": "https://www.googleapis.com/auth/blogger",
        "redirect_uri": "urn:aaaaa",
        "post_blog_id": "xxxxxx",
        "credentials": "/home/matarain/pythonapp/uhiimanbot/tests/"
        "testmaterials/config/credentials.dat",
    }
    auth_twitter = {
        "parent_screen_name": "parent",
        "my_screen_name": "child",
        "consumer_key": "twitter1234567",
        "consumer_secret": "token123",
        "token": "token234",
        "token_secret": "secret998",
    }
    auth_flickr = {"secret": "a123", "api_key": "apikeys"}
    auth_other = {
        "user_name": "hatebuser",
        "consumer_key": "hateb",
        "consumer_secret": "hatenasecret",
        "token": "token889",
        "token_secret": "secret884",
    }

    authentications = Configreader(mode)
    """ Blogger """

    def test_getauth_blogger(self):
        snsname = "blogger"
        result = self.authentications.get_snsauth(snsname)
        self.assertDictEqual(result, self.auth_blogger)

    """ twitter """

    def test_getauth_twitter(self):
        snsname = "twitter"
        result = self.authentications.get_snsauth(snsname)
        self.assertDictEqual(result, self.auth_twitter)

    """ flickr """

    def test_getauth_flickr(self):
        snsname = "flickr"
        result = self.authentications.get_snsauth(snsname)
        self.assertDictEqual(result, self.auth_flickr)

    """ その他 """

    def test_getauth_hateb(self):
        snsname = "hatena"
        result = self.authentications.get_snsauth(snsname)
        self.assertDictEqual(result, self.auth_other)

    """ exception """

    def test_getauth_exception(self):
        snsname = "other"
        with self.assertRaises(Exception, msg="get snsauth config exception!!"):
            self.authentications.get_snsauth(snsname)


class TestDataBase(TestCase):
    mode = "test"
    database_text = {
        "filepath": "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
        "data/output.db",
        "filetype": "text",
    }
    database_mongo = {
        "host": "localhost",
        "username": "testtohonokai",
        "password": "password",
        "authSource": "test_cr_tohonokai",
        "authMechanism": "SCRAM-SHA-1",
        "dbname": "test_cr_tohonokai",
        "collection": "rss_article",
    }
    database_sql = {
        "host": "localhost",
        "username": "username",
        "password": "password",
        "dbname": "databasename",
        "tablename": "tablename",
    }

    databases = Configreader(mode)
    """ テスト用DB """

    def test_getdb_setting_text(self):
        databasename = "text"
        result = self.databases.get_database(databasename)
        self.assertDictEqual(result, self.database_text)

    """ mongo """

    def test_getdb_setting_mongo(self):
        databasename = "mongo"
        result = self.databases.get_database(databasename)
        self.assertDictEqual(result, self.database_mongo)

    """ SQL """

    def test_getdb_setting_sql(self):
        databasename = "database"
        result = self.databases.get_database(databasename)
        self.assertDictEqual(result, self.database_sql)

    """ exception """

    def test_getdb_setting_exception(self):
        databasename = ""
        with self.assertRaises(Exception, msg="get database config exception!!"):
            self.databases.get_database(databasename, 123)


class TestFile(TestCase):
    mode = "test"
    logpath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/logs/app.log"
    csvpath = (
        "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/config/rssfeed.csv"
    )
    filepath = Configreader(mode)
    """ ログファイル """

    def test_getlog_setting_test(self):
        pathstring = "applog"
        result = self.filepath.get_filepath(pathstring)
        self.assertEqual(result, self.logpath)

    """ CSVファイル """

    def test_getcsv_setting_test(self):
        pathstring = "csvfile"
        result = self.filepath.get_filepath(pathstring)
        self.assertEqual(result, self.csvpath)

    """ exception """

    def test_getdb_setting_exception(self):
        pathstring = "other"
        with self.assertRaises(Exception, msg="get filepath exception!!"):
            self.filepath.get_filepath(pathstring)


class TestCSVReader(TestCase):
    mode = "test"
    feeds = [
        [
            "＠IT Smart & Socialフォーラム 最新記事一覧",
            "https://rss.itmedia.co.jp/rss/2.0/ait_smart.xml",
            "IT",
        ],
        ["気になる、記になる…", "https://taisy0.com/feed", "IT"],
        ["PCパーツまとめ", "http://blog.livedoor.jp/bluejay01-review/index.rdf", "IT"],
        [
            "＠IT Database Expertフォーラム 最新記事一覧",
            "https://rss.itmedia.co.jp/rss/2.0/ait_db.xml",
            "IT",
        ],
    ]
    csvread = Configreader(mode)

    """ CSVファイル取得 """

    def test_get_rss_feed(self):
        results = self.csvread.get_rss_feed()
        self.assertEqual(results, self.feeds)

    """ exception """

    def test_get_rssfeed_exception(self):
        path = "other"
        with self.assertRaises(Exception, msg="get csvfile exception!!"):
            self.csvread.get_filepath(path)


class TestMessage(TestCase):
    mode = "test"
    message = Configreader(mode)
    smtp = {
        "server": "mail.google.com",
        "port": 465,
        "user": "sample",
        "password": "password",
        "from": "aaa@gmail.com",
    }
    sendgrid = {"apikey": "SG.api_key", "from": "aaa@aaa.com"}
    slack = {"token": "xoxb-token", "channel": "Cannel"}

    """SMTP Mail"""

    def test_get_smtp(self):
        messagetype = "smtp"
        result = self.message.get_message_auth(messagetype)
        self.assertEqual(result, self.smtp)

    """ SendGrid """

    def test_get_sendgrid(self):
        messagetype = "sendgrid"
        result = self.message.get_message_auth(messagetype)
        self.assertEqual(result, self.sendgrid)

    """ Slack """

    def test_get_slack(self):
        messagetype = "slack"
        result = self.message.get_message_auth(messagetype)
        self.assertEqual(result, self.slack)

    """ exception """

    def test_get_message_exception(self):
        messagetype = "other"
        with self.assertRaises(Exception, msg="get message auth config exception!!"):
            self.message.get_message_auth(messagetype)
