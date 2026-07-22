from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    metric_artifact: float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float

@dataclass
class ModelPusherArtifact:
    saved_model_path: str
    saved_preprocessor_path: str
