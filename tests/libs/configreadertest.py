import pathlib
import sys
from unittest import TestCase

import testdata.config_test_data as config_test_data

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from libs.configreader import Configreader


class TestConfigRead(TestCase):
    mode = "test"
    config = Configreader(mode)

    """ Auth """

    def test_getauth(self):
        testtitles = config_test_data.sns_testtitles
        sns_names = config_test_data.sns_names
        auth_datas = config_test_data.sns_auth_datas
        print("Get sns -->>>")
        for testtitle, snsname, expectedresult in zip(
            testtitles, sns_names, auth_datas
        ):
            print(testtitle + "-->>>")
            result = self.config.get_snsauth(snsname)
            self.assertDictEqual(result, expectedresult)
            print("exception-->>>")
        snsname = "other"
        with self.assertRaises(Exception, msg="get snsauth config exception!!"):
            self.config.get_snsauth(snsname)

    """ database """

    def test_getdb_setting(self):
        testtitles = config_test_data.database_testtitles
        databasenames = config_test_data.databasenames
        databases = config_test_data.databases

        print("Get dataBase -->>>")
        for testtitle, databasename, expectedresult in zip(
            testtitles, databasenames, databases
        ):
            print(testtitle + "-->>>")
            result = self.config.get_database(databasename)
            self.assertDictEqual(result, expectedresult)
        print("exception-->>>")
        databasename = 123
        with self.assertRaises(Exception, msg="get database config exception!!"):
            self.config.get_database(databasename, 123)

    """ file """

    def test_getfile_setting(self):
        testtitles = config_test_data.file_testtitles
        pathstrings = config_test_data.pathstrings
        filepaths = config_test_data.filepaths

        print("Get dataBase -->>>")
        for testtitle, pathstring, expectedresult in zip(
            testtitles, pathstrings, filepaths
        ):
            print(testtitle + "-->>>")
            result = self.config.get_filepath(pathstring)
            self.assertEqual(result, expectedresult)
        pathstring = "other"
        with self.assertRaises(Exception, msg="get filepath exception!!"):
            self.config.get_filepath(pathstring)

    """ rssfeed """

    def test_get_rss_feed(self):
        feeds = config_test_data.feeds

        print("Get rssfeed -->>>")
        results = self.config.get_rss_feed()
        self.assertEqual(results, feeds)
        print("exception-->>>")
        path = "other"
        with self.assertRaises(Exception, msg="get csvfile exception!!"):
            self.config.get_filepath(path)

    """ message """

    def test_get_message(self):
        testtitles = config_test_data.message_testtitles
        messagetypes = config_test_data.messagetypes
        messages = config_test_data.messages

        print("Get message -->>>")
        for testtitle, messagetype, expectedresult in zip(
            testtitles, messagetypes, messages
        ):
            print(testtitle + "-->>>")
            result = self.config.get_message_auth(messagetype)
            self.assertEqual(result, expectedresult)
        print("exception-->>>")
        messagetype = 123
        with self.assertRaises(Exception, msg="get message auth config exception!!"):
            self.config.get_message_auth(messagetype)
