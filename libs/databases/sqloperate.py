from sqlalchemy import Column, and_, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class SqlOperator:
    def __init__(self, db_type, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

    def create_table(self, table_name: str, columns: str, keycolumn: str):
        try:
            """Create table dynamically"""
            columns_def = {}
            for col_name, col_type in columns.items():
                if col_name == keycolumn:
                    columns_def[col_name] = Column(col_type, primary_key=True)
                else:
                    columns_def[col_name] = Column(col_type)
            table = type(
                table_name, (self.Base,), {"__tablename__": table_name, **columns_def}
            )
            if not hasattr(self.Base, table_name):
                setattr(self.Base, table_name, table)
                table.__table__.create(bind=self.engine)
        except Exception:
            raise Exception("create exception")

    """ Count """

    def count(self, table_name: str, criteria: dict = None):
        try:
            session = self.Session()
            findresult = self.search_generate(session, table_name, criteria)
            return len(findresult)
        except Exception:
            raise Exception("count exception")

    """ Find """

    def find(self, table_name: str, criteria: dict):
        try:
            session = self.Session()
            findresult = self.search_generate(session, table_name, criteria)
            results = []
            for obj in findresult:
                row = {}
                for col in obj.__table__.columns:
                    row[col.name] = getattr(obj, col.name)
                results.append(row)
            return results
        except Exception:
            raise Exception("find exception")

    def search_generate(self, session: object, table_name: str, criteria: dict):
        try:
            table = getattr(self.Base, table_name)
            query = session.query(table)
            conditions = []
            # Multiple
            if "$and" in criteria.keys():
                and_conditions = []
                for cond in criteria["$and"]:
                    cond_conditions = self.generate_conditions(table, cond)
                    if cond_conditions:
                        and_conditions.append(and_(*cond_conditions))
                if and_conditions:
                    query = query.filter(and_(*and_conditions))
            else:
                conditions = self.generate_conditions(table, criteria)
                if conditions:
                    query = query.filter(*conditions)
            return query.all()
        except Exception:
            raise Exception("search genarate exception")

    def generate_conditions(self, table, criteria):
        try:
            conditions = []
            for key, value in criteria.items():
                column = getattr(table, key)
                if not isinstance(value, dict):
                    condition = column == value
                elif "$ne" in value.keys():
                    condition = column != value["$ne"]
                elif "$gt" in value.keys():
                    condition = column > value["$gt"]
                elif "$lt" in value.keys():
                    condition = column < value["$lt"]
                elif "$gte" in value.keys():
                    condition = column >= value["$gte"]
                elif "$lte" in value.keys():
                    condition = column <= value["$lte"]
                elif "$regex" in value.keys():
                    likesentence = self.convert_regexp_to_like(value["$regex"])
                    condition = column.like(likesentence)
                else:
                    condition = None
                if condition is not None:
                    conditions.append(condition)
            return conditions
        except Exception:
            raise Exception("generate condition exception")

    def convert_regexp_to_like(self, regexp_pattern):
        try:
            # Convert regular expression patterns to LIKE
            like_pattern = regexp_pattern.replace(".", "")
            if like_pattern.startswith("^") and like_pattern.endswith("$"):
                like_pattern = like_pattern.replace("^", "")
                like_pattern = like_pattern.replace("$", "%")
                like_pattern = like_pattern.replace("*", "%")
                like_pattern = like_pattern.replace("%%", "%")
            else:
                like_pattern = like_pattern.replace("^", "") + "%%%%"
            return like_pattern
        except Exception:
            raise Exception("convert regexp exception")

    """ Insert """

    def insert(self, table_name: str, data: dict):
        try:
            session = self.Session()
            table = getattr(self.Base, table_name)
            obj = table(**data)
            session.add(obj)
            session.commit()
        except Exception:
            raise Exception("insert exception")

    """ Update """

    def update(self, table_name: str, criteria: dict, updates: dict):
        try:
            session = self.Session()
            findresults = self.search_generate(session, table_name, criteria)
            if findresults:
                for findresult in findresults:
                    for key, value in updates["$set"].items():
                        setattr(findresult, key, value)
                session.commit()
        except Exception:
            raise Exception("update exception")

    """ Delete """

    def delete(self, table_name: str, criteria: dict):
        try:
            session = self.Session()
            findresults = self.search_generate(session, table_name, criteria)

            if findresults:
                for findresult in findresults:
                    session.delete(findresult)
                session.commit()
        except Exception:
            raise Exception("delete exception")


""" Connection """
"""
# sqlite
from libs.databases.sqloperate import SQLiteDatabase
db = SQLiteDatabase('sqlite:///test.db')
db = SQLiteDatabase('sqlite:///:memory:')

# MySQL
from libs.databases.sqloperate import MySQLDatabase
db = MySQLDatabase('mysql+pymysql://user:password@hostname/dbname')

# PostgreSQL
from libs.databases.sqloperate import PostgreSQLDatabase
db = PostgreSQLDatabase('postgresql+psycopg2://user:password@hostname/dbname')

"""


class MySQLDatabase(SqlOperator):
    def __init__(self, connection_string):
        super().__init__("mysql", connection_string)


class PostgreSQLDatabase(SqlOperator):
    def __init__(self, connection_string):
        super().__init__("postgresql", connection_string)


class SQLiteDatabase(SqlOperator):
    def __init__(self, connection_string):
        super().__init__("sqlite", connection_string)
