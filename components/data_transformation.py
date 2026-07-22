import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder
from entity.config_entity import DataTransformationConfig
from entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from exception import CustomException
from logger import logging
from utils.common import save_object

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            scaler = StandardScaler()
            return scaler
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Read train and test data completed")

            if "Student_ID" in train_df.columns:
                train_df.drop(columns=["Student_ID"], inplace=True)
            if "Student_ID" in test_df.columns:
                test_df.drop(columns=["Student_ID"], inplace=True)

            target_column = "Post_Semester_GPA"
            
            input_feature_train_df = train_df.drop(columns=[target_column])
            target_feature_train_df = train_df[target_column]
            
            input_feature_test_df = test_df.drop(columns=[target_column])
            target_feature_test_df = test_df[target_column]

            logging.info("Applying encoders")
            
            label_cols = ['Major_Category', 'Year_of_Study', 'Primary_Use_Case', 'Institutional_Policy']
            ord_cols = ['Prompt_Engineering_Skill', 'Burnout_Risk_Level']
            
            for col in label_cols:
                le = LabelEncoder()
                input_feature_train_df[col] = le.fit_transform(input_feature_train_df[col])
                try:
                    input_feature_test_df[col] = le.transform(input_feature_test_df[col])
                except:
                    input_feature_test_df[col] = LabelEncoder().fit_transform(input_feature_test_df[col])

            for col in ord_cols:
                oe = OrdinalEncoder()
                input_feature_train_df[col] = oe.fit_transform(input_feature_train_df[[col]])
                try:
                    input_feature_test_df[col] = oe.transform(input_feature_test_df[[col]])
                except:
                    input_feature_test_df[col] = OrdinalEncoder().fit_transform(input_feature_test_df[[col]])

            logging.info("Applying standard scaler")
            preprocessing_obj = self.get_data_transformer_object()
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_train_file_path), exist_ok=True)
            np.save(self.data_transformation_config.transformed_train_file_path, train_arr)
            np.save(self.data_transformation_config.transformed_test_file_path, test_arr)

            save_object(
                file_path=self.data_transformation_config.transformed_object_file_path,
                obj=preprocessing_obj
            )
            
            logging.info("Data Transformation completed successfully")
            
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
