import os
import sys
import pandas as pd
from entity.config_entity import DataValidationConfig
from entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from exception import CustomException
from logger import logging

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise CustomException(e, sys)

    def validate_columns(self) -> bool:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            status = len(train_df.columns) > 0
            
            dir_path = os.path.dirname(self.data_validation_config.valid_status_file_dir)
            os.makedirs(dir_path, exist_ok=True)
            
            with open(self.data_validation_config.valid_status_file_dir, "w") as f:
                f.write(f"Validation status: {status}")
                
            return status
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            status = self.validate_columns()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                message="Data Validation Completed"
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)
