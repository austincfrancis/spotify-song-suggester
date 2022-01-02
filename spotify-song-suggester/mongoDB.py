from pymongo import MongoClient

class Mongo:
    def __init__(self, URI):
        self.client = MongoClient(URI)

        self.db = self.client["spotify"]
        self.col = self.db["data"]

    def insert_one(self, data):
        self.col.insert_one(data)

    def insert_many(self, data):
        self.col.insert_many(data)

    def find_one(self, query):
        return self.col.find(query)[0]

    def find(self, query):
        return self.col.find(query)

