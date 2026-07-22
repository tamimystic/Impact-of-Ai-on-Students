import os
import sys
import shutil
from entity.config_entity import ModelPusherConfig
from entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from exception import CustomException
from logger import logging

class ModelPusher:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_pusher_config: ModelPusherConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Initiating model pusher")
            os.makedirs(os.path.dirname(self.model_pusher_config.model_file_path), exist_ok=True)
            
            shutil.copy(
                self.model_trainer_artifact.trained_model_file_path,
                self.model_pusher_config.model_file_path
            )
            
            shutil.copy(
                self.data_transformation_artifact.transformed_object_file_path,
                self.model_pusher_config.preprocessor_path
            )
            
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path=self.model_pusher_config.model_file_path,
                saved_preprocessor_path=self.model_pusher_config.preprocessor_path
            )
            
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise CustomException(e, sys)
