import traceback

from .applicationlogs import ApplicationLogs
from .configreader import Configreader
from .databases.mongooperate import MongoOperate
from .databases.sqloperate import MySQLDatabase, PostgreSQLDatabase
from .databases.textoperate import TextOperator


class Datacrud:
    def __init__(self, mode: str = "prod", destinationtype: str = "mongo"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        config = Configreader(mode)
        logpath = config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.destinationtype = destinationtype
        dbconnection = config.get_database(self.destinationtype)
        self.db = None
        self.table = None
        if "tablename" in dbconnection:
            self.table = dbconnection["tablename"]

        match destinationtype:
            case "mongo":
                self.db = MongoOperate.MongoConnect(dbconnection)
            case "mysql":
                self.db = MySQLDatabase(
                    f"mysql+pymysql://{dbconnection['user']}:"
                    f"{dbconnection['password']}@{dbconnection['host']}/"
                    f"{dbconnection['dbname']}"
                )
            case "postgre":
                self.db = PostgreSQLDatabase(
                    f"postgresql+psycopg2://{dbconnection['user']}:"
                    f"{dbconnection['password']}@{dbconnection['host']}/"
                    f"{dbconnection['dbname']}"
                )
            case "text":
                self.db = TextOperator(dbconnection["filepath"])

    """ Create(Insert) """

    def create_data(self, data: dict = None) -> None:
        try:
            # Conversion due to different argument types in Mongo and text and SQL
            insertdatas = [data] if isinstance(data, dict) else data
            match self.destinationtype:
                case "mongo":
                    mongo = MongoOperate.MongoInsert(self.db.collection)
                    mongo.insert_many(insertdatas)
                case "mysql":
                    self.db.insert(self.table, insertdatas)
                case "postgre":
                    self.db.insert(self.table, insertdatas)
                case "text":
                    self.db.text_create(insertdatas)
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("create data exception!!")

    """ Read(Find) """

    def read_data(self, search_condition: dict = None) -> list:
        try:
            if isinstance(search_condition, dict):
                result = []
                match self.destinationtype:
                    case "mongo":
                        mongo = MongoOperate.MongoFind(self.db.collection)
                        cursor = mongo.find(filter=search_condition)
                        result = list(cursor)
                    case "mysql":
                        result = self.db.find(self.table, search_condition)
                    case "postgre":
                        result = self.db.find(self.table, search_condition)
                    case "text":
                        result = self.db.text_read(search_condition)
                return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("read data exception")

    """ Update """

    def update_data(self, update_condition: dict, replace_value: dict) -> None:
        try:
            if isinstance(update_condition, dict):
                match self.destinationtype:
                    case "mongo":
                        mongo = MongoOperate.MongoUpdate(self.db.collection)
                        mongo.update_many(filter=update_condition, update=replace_value)
                    case "mysql":
                        self.db.update(self.table, update_condition, replace_value)
                    case "postgre":
                        self.db.update(self.table, update_condition, replace_value)
                    case "text":
                        self.db.text_update(update_condition, replace_value)
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("update data exception!!")

    """ Delete """

    def delete_data(self, delete_condition: dict = None) -> None:
        try:
            if isinstance(delete_condition, dict):
                match self.destinationtype:
                    case "mongo":
                        mongo = MongoOperate.MongoDelete(self.db.collection)
                        mongo.delete_many(filter=delete_condition)
                    case "mysql":
                        self.db.delete(self.table, delete_condition)
                    case "postgre":
                        self.db.delete(self.table, delete_condition)
                    case "text":
                        self.db.text_delete(delete_condition)
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("delete data exception!!")
