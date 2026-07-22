import os
import sys
import shutil
from entity.config_entity import ModelTrainerConfig
from entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from exception import CustomException
from logger import logging

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("We have a pre-trained .keras model. Skipping training and wrapping the model.")
            
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path), exist_ok=True)
            
            # Copy the source model to artifact folder
            shutil.copy(
                self.model_trainer_config.source_model_path,
                self.model_trainer_config.trained_model_file_path
            )

            # In a real scenario we might load and evaluate it, but here we just pass it along
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=0.0 # dummy metric
            )
            
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
            
        except Exception as e:
            raise CustomException(e, sys)
