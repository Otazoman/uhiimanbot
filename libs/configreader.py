import csv
import os
import traceback

import yaml

from .applicationlogs import ApplicationLogs


class Configreader:
    def __init__(self, mode: str = "prod"):
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        logpath = {
            "prod": "/home/matarain/pythonapp/uhiimanbot/logs/app.log",
            "test": "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/logs/"
            "app.log",
        }
        self.applog = ApplicationLogs(name, logmode, logpath[mode])
        filepath = {
            "prod": "/home/matarain/pythonapp/uhiimanbot/config/settings.yaml",
            "test": "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
            "config/settings.yaml",
        }
        settingfile = filepath[mode]
        if os.path.exists(settingfile):
            with open(settingfile, "r") as yml:
                self.config = yaml.safe_load(yml)
        else:
            self.applog.output_log(self.loglevel, traceback.format_exc())

    """ setting filepath """

    def get_filepath(self, settingtype: str) -> str:
        try:
            result = self.config["FilePath"][settingtype]
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get filepath exception!!")

    """ database setting information """

    def get_database(self, databasename: str) -> dict:
        try:
            result = {}
            database_config = self.config["DataBase"]
            match databasename:
                case "text":
                    result = {
                        "filepath": database_config[databasename]["filepath"],
                        "filetype": database_config[databasename]["filetype"],
                    }
                case "mongo":
                    result = {
                        "host": database_config[databasename]["host"],
                        "username": database_config[databasename]["username"],
                        "password": database_config[databasename]["password"],
                        "authSource": database_config[databasename]["authSource"],
                        "authMechanism": database_config[databasename]["authMechanism"],
                        "dbname": database_config[databasename]["dbname"],
                        "collection": database_config[databasename]["collection"],
                    }
                case "database":
                    result = {
                        "host": database_config[databasename]["host"],
                        "username": database_config[databasename]["username"],
                        "password": database_config[databasename]["password"],
                        "dbname": database_config[databasename]["dbname"],
                        "tablename": database_config[databasename]["tablename"],
                    }
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get database config exception!!")

    """ sns authentication information """

    def get_snsauth(self, snsname: str) -> dict:
        try:
            snsauth_config = self.config["SNSAuthentication"]
            match snsname:
                case "blogger":
                    result = {
                        "client_id": snsauth_config[snsname]["client_id"],
                        "client_secret": snsauth_config[snsname]["client_secret"],
                        "scope": snsauth_config[snsname]["scope"],
                        "redirect_uri": snsauth_config[snsname]["redirect_uri"],
                        "post_blog_id": snsauth_config[snsname]["post_blog_id"],
                        "credentials": snsauth_config[snsname]["credentials"],
                    }
                case "twitter":
                    result = {
                        "parent_screen_name": snsauth_config[snsname][
                            "parent_screen_name"
                        ],
                        "my_screen_name": snsauth_config[snsname]["my_screen_name"],
                        "consumer_key": snsauth_config[snsname]["consumer_key"],
                        "consumer_secret": snsauth_config[snsname]["consumer_secret"],
                        "token": snsauth_config[snsname]["token"],
                        "token_secret": snsauth_config[snsname]["token_secret"],
                    }
                case "bluesky":
                    result = {
                        "user_name": snsauth_config[snsname]["user_name"],
                        "app_password": snsauth_config[snsname]["app_password"],
                    }
                case "flickr":
                    result = {
                        "secret": snsauth_config[snsname]["secret"],
                        "api_key": snsauth_config[snsname]["api_key"],
                    }
                case _:
                    result = {
                        "user_name": snsauth_config[snsname]["user_name"],
                        "consumer_key": snsauth_config[snsname]["consumer_key"],
                        "consumer_secret": snsauth_config[snsname]["consumer_secret"],
                        "token": snsauth_config[snsname]["token"],
                        "token_secret": snsauth_config[snsname]["token_secret"],
                    }
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get snsauth config exception!!")

    """ Csv setting """

    def get_rss_feed(self, path: str = None) -> str:
        try:
            settingtype = "csvfile"

            if path is None:
                filepath = self.get_filepath(settingtype)
            else:
                filepath = path

            with open(filepath, "r") as f:
                data = csv.reader(f)
                result = [r for r in data if r]
                del result[0]
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get csvfile exception!!")

    """ Message setting """

    def get_message_auth(self, messagetype: str) -> dict:
        try:
            message_config = self.config["SendMessage"]
            match messagetype:
                case "smtp":
                    result = {
                        "server": message_config[messagetype]["server"],
                        "port": message_config[messagetype]["port"],
                        "user": message_config[messagetype]["user"],
                        "password": message_config[messagetype]["password"],
                        "from": message_config[messagetype]["from"],
                    }
                case "sendgrid":
                    result = {
                        "apikey": message_config[messagetype]["apikey"],
                        "from": message_config[messagetype]["from"],
                    }
                case "slack":
                    result = {
                        "token": message_config[messagetype]["token"],
                        "channel": message_config[messagetype]["channel"],
                    }
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get message auth config exception!!")
