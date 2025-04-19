from dataclasses import dataclass

@dataclass
class dataingestion:
    train_data_path:str
    test_data_path:str

@dataclass
class datavalidation:
    validation_status:bool
    Train_validation_path:str
    Test_validation_path:str
    Drift_report_path:str
    Train_invalidation_path:str
    Test_invalidation_path:str

@dataclass
class transformation:
    traindata_transformed_path:str
    testdata_transformed_path:str
    preprocessing_obj_path:str

@dataclass
class classification_metrics_artifacts:
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class data_model:
    models_report_path:str
    best_model_path:str
    trained_classification_metrics:classification_metrics_artifacts
    test_classification_metrics:classification_metrics_artifacts