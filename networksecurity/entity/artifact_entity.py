from dataclasses import dataclass

@dataclass
class dataingestion():
    train_data_path:str
    test_data_path:str

@dataclass
class datavalidation():
    validation_status:bool
    Train_validation_path:str
    Test_validation_path:str
    Drift_report_path:str
    Train_invalidation_path:str
    Test_invalidation_path:str
    