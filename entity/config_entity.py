from dataclasses import dataclass
import os

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join("artifacts", "data_ingestion")
    dataset_path: str = os.path.join(data_ingestion_dir, "dataset.csv")
    train_data_path: str = os.path.join(data_ingestion_dir, "train.csv")
    test_data_path: str = os.path.join(data_ingestion_dir, "test.csv")
    train_test_split_ratio: float = 0.33
    db_name: str = "AI_Impact_DB"
    collection_name: str = "Students_Collection"

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join("artifacts", "data_validation")
    valid_status_file_dir: str = os.path.join(data_validation_dir, "status.txt")

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join("artifacts", "data_transformation")
    transformed_train_file_path: str = os.path.join(data_transformation_dir, "train.npy")
    transformed_test_file_path: str = os.path.join(data_transformation_dir, "test.npy")
    transformed_object_file_path: str = os.path.join(data_transformation_dir, "preprocessing.pkl")

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join("artifacts", "model_trainer")
    trained_model_file_path: str = os.path.join(model_trainer_dir, "model.keras")
    source_model_path: str = os.path.join("models", "ai_student_impact_model.keras")

@dataclass
class ModelEvaluationConfig:
    model_evaluation_dir: str = os.path.join("artifacts", "model_evaluation")
    report_file_path: str = os.path.join(model_evaluation_dir, "report.yaml")
    
@dataclass
class ModelPusherConfig:
    saved_model_dir: str = "saved_models"
    model_file_path: str = os.path.join(saved_model_dir, "model.keras")
    preprocessor_path: str = os.path.join(saved_model_dir, "preprocessing.pkl")
