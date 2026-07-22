import os
import sys
import pymongo
import pandas as pd
from dotenv import load_dotenv
from exception import CustomException
from logger import logging

load_dotenv()

class MongoDBOperation:
    def __init__(self):
        self.DB_URL = os.getenv("MONGO_DB_URL")
        self.client = pymongo.MongoClient(self.DB_URL)

    def get_collection_as_dataframe(self, db_name: str, collection_name: str) -> pd.DataFrame:
        try:
            logging.info(f"Connecting to Database: {db_name} and Collection: {collection_name}")
            database = self.client[db_name]
            collection = database[collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])
                
            logging.info(f"Data retrieved successfully. Shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(e, sys)
