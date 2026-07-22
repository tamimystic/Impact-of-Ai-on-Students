import os
import sys
from entity.config_entity import ModelEvaluationConfig
from entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from exception import CustomException
from logger import logging

class ModelEvaluation:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_evaluation_config: ModelEvaluationConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_evaluation_config = model_evaluation_config
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Initiating model evaluation")
            
            is_model_accepted = True
            
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=0.0
            )
            
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise CustomException(e, sys)
