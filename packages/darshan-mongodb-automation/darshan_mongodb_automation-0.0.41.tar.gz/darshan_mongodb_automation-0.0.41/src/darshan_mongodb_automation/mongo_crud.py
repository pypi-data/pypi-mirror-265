from typing import Any
import os
import pandas as pd
import pymongo
from pymongo.mongo_client import MongoClient
import json
from ensure import ensure_annotations

class MongoOperation:
    def __init__(self, client_uri:str, database_name:str=None, collection_name:str=None):
        self.client_uri = client_uri
        self.database_name = database_name
        self.collection_name = collection_name
        
    def create_client(self):
        client = MongoClient(self.client_uri)
        return client
    
    def create_database(self, database_name:str=None):
        client = self.create_client()
        self.database_name = database_name
        database = client[self.database_name]
        return database
    
    def create_collection(self, collection_name:str=None, database_name:str=None):
        database = self.create_database(database_name)
        self.collection_name = collection_name
        collection = database[self.collection_name]
        return collection
    
    def insert_data(self, data, collection:str, database:str) -> None:
        collection = self.create_collection(collection, database)
        if type(data) == list:
            collection.insert_many(data)
        elif type(data) == dict:
            collection.insert_one(data)
            
    def insert_bulk(self, file_path:str, collection:str, database:str) -> None:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('xlsx'):
            data = pd.read_excel(file_path)
        data_json = json.loads(data.to_json(orient = 'record'))
        collection = self.create_collection(collection, database)
        collection.insert_many(data_json)