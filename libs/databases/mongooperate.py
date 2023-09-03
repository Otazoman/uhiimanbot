from pymongo import MongoClient


class MongoOperate:
    class MongoConnect:
        def __init__(self, config: dict):
            self.client = MongoClient(
                config["host"],
                username=config["username"],
                password=config["password"],
                authSource=config["authSource"],
                authMechanism=config["authMechanism"],
            )
            self.db = self.client[config["dbname"]]
            self.collection = self.db.get_collection(config["collection"])

        """ Connection """

        def connect(self):
            return self.collection

    """ Count """

    class MongoCount:
        def __init__(self, collection: object):
            self.collection = collection

        def count(self, filter=None):
            return self.collection.count_documents(filter)

    """ Find """

    class MongoFind:
        def __init__(self, collection: object):
            self.collection = collection

        def find_one(self, projection=None, filter=None, sort=None):
            return self.collection.find_one(
                projection=projection, filter=filter, sort=sort
            )

        def find(self, projection=None, filter=None, sort=None):
            return self.collection.find(
                projection=projection, filter=filter, sort=sort, no_cursor_timeout=True
            )

    """ Insert """

    class MongoInsert:
        def __init__(self, collection: object):
            self.collection = collection

        def insert_one(self, document):
            return self.collection.insert_one(document)

        def insert_many(self, documents):
            return self.collection.insert_many(documents)

    """ Update """

    class MongoUpdate:
        def __init__(self, collection: object):
            self.collection = collection

        def update_one(self, filter, update):
            return self.collection.update_one(filter, update)

        def update_many(self, filter, update):
            return self.collection.update_many(filter, update)

        def replace_one(self, filter, replacement):
            return self.collection.replace_one(filter, replacement)

        def find_one_and_replace(self, filter, replacement):
            return self.collection.find_one_and_replace(filter, replacement)

    """ Delete """

    class MongoDelete:
        def __init__(self, collection: object):
            self.collection = collection

        def delete_one(self, filter):
            return self.collection.delete_one(filter)

        def delete_many(self, filter):
            return self.collection.delete_many(filter)
