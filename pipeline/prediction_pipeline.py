import os
import sys
import pandas as pd
from tensorflow.keras.models import load_model
from utils.common import load_object
from exception import CustomException
from logger import logging
from entity.config_entity import ModelPusherConfig

class PredictionPipeline:
    def __init__(self):
        self.model_pusher_config = ModelPusherConfig()
        
    def predict(self, features: pd.DataFrame):
        try:
            model_path = self.model_pusher_config.model_file_path
            preprocessor_path = self.model_pusher_config.preprocessor_path
            
            logging.info(f"Loading preprocessor from {preprocessor_path}")
            preprocessor = load_object(file_path=preprocessor_path)
            
            logging.info(f"Loading model from {model_path}")
            model = load_model(model_path)
            
            scaled_features = preprocessor.transform(features)
            preds = model.predict(scaled_features)
            return preds
        except Exception as e:
            raise CustomException(e, sys)
