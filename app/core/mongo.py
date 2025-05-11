from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.ner
        self.data_collection = self.db.data

    def insert_data_from_fields(self, data: dict):
        self.data_collection.insert_one(data)
        
    def insert_data_from_json(self, data: list[dict]):
        self.data_collection.insert_many(data)
            
    def retrieve_data(self):
        if self.data_collection.count_documents({}) > 3:
            return self.data_collection.find()
        
    def delete_all_data(self):
        if self.data_collection.count_documents({}) > 0:
            self.data_collection.drop()
        else:
            raise Exception("The database is empty!")
