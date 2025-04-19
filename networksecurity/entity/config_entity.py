import os
import numpy as np
from datetime import datetime
from networksecurity.constant import training_pipeline

class pipelineconfig():
    def __init__(self,timestamp=datetime.now()):
        datetime = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_dir = training_pipeline.artifact_dir
        self.artifact_time_stamp_dir = os.path.join(self.artifact_dir,datetime)
        self.target_column = training_pipeline.Target_column

class ingestionconfig:
    def __init__(self,pipelineconfig:pipelineconfig):
        self.ingestion_dir = os.path.join(pipelineconfig.artifact_time_stamp_dir,training_pipeline.ingestion_dir)
        self.feature_store = os.path.join(self.ingestion_dir,training_pipeline.feature_dir)
        self.ingested = os.path.join(self.ingestion_dir,training_pipeline.data_ingested_dir)
        self.train_data_dir = os.path.join(self.ingested,training_pipeline.training_dir)
        self.test_data_dir = os.path.join(self.ingested,training_pipeline.testing_dir)
        self.source = os.path.join(training_pipeline.source_dir,training_pipeline.source_file)

        self.train_file = os.path.join(self.train_data_dir,training_pipeline.train_file)
        self.test_file = os.path.join(self.test_data_dir,training_pipeline.test_file)
        
        self.traintest_split_ratio = training_pipeline.train_test_split_ratio

class validationconfig:
    def __init__(self, pipelineconfig:pipelineconfig):
        self.validation_dir = os.path.join(pipelineconfig.artifact_time_stamp_dir,training_pipeline.datavalidation_dir)
        self.validated_dir = os.path.join(self.validation_dir,training_pipeline.validated_dir)
        self.invalidated_dir = os.path.join(self.validation_dir,training_pipeline.invalidated_dir)
        self.drift_report_dir = os.path.join(self.validation_dir,training_pipeline.drift_report_dir)
        
        self.validated_train_file = os.path.join(self.validated_dir,training_pipeline.train_file)
        self.validated_test_file = os.path.join(self.validated_dir,training_pipeline.test_file)
        
        self.invalidated_train_file = os.path.join(self.invalidated_dir,training_pipeline.train_file)
        self.invalidated_test_file = os.path.join(self.invalidated_dir,training_pipeline.test_file)
        
        self.drift_report_file = os.path.join(self.drift_report_dir,training_pipeline.drift_report_file)

        self.SCHEMA_FILE_PATH = os.path.join(training_pipeline.schema_folder,training_pipeline.schema_file)

class transformationconfig:
    def __init__(self, pipelineconfig:pipelineconfig):
        self.transformation_dir = os.path.join(pipelineconfig.artifact_time_stamp_dir,training_pipeline.transformation_dir)
        self.transformed_dir = os.path.join(self.transformation_dir,training_pipeline.transformed_dir)
        self.transformed_obj = os.path.join(self.transformation_dir,training_pipeline.transformed_obj)
        self.preprocessing_file = os.path.join(self.transformed_obj,training_pipeline.preprocessing_file)
        self.target_column = pipelineconfig.target_column
        self.KNN_Imputer_params:dict = {"missing_values":np.nan,
                                        "n_neighbors":3,
                                        "weights": "uniform"}
        self.train_file = os.path.join(self.transformed_dir, training_pipeline.train_file.replace("csv","npy"))
        self.test_file = os.path.join(self.transformed_dir, training_pipeline.test_file.replace("csv","npy"))


class modelconfig:
    def __init__(self, pipelineconfig:pipelineconfig):
        self.model_directory = os.path.join(pipelineconfig.artifact_time_stamp_dir, training_pipeline.model_dir)
        self.model_trained_directory = os.path.join(self.model_directory, training_pipeline.model_trained_dir)
        self.model_file = os.path.join(self.model_trained_directory, training_pipeline.model_file_name)
        self.models_report = os.path.join(self.model_trained_directory, training_pipeline.models_report_file)



# if __name__ == '__main__':
#     # Create an instance of pipelineconfig
#     pipeline_config_instance = pipelineconfig()
#     # Pass the instance to ingestionconfig
#     ingestion_config_instance = ingestionconfig(pipeline_config_instance)
#     # Print the ingestion_dir
#     print(ingestion_config_instance.feature_store)