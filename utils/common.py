import os
import sys
import pickle
from exception import CustomException
from logger import logging

def save_object(file_path: str, obj: object):
    try:
        logging.info(f"Saving object to: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Object saved to: {file_path}")
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path: str):
    try:
        logging.info(f"Loading object from: {file_path}")
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
