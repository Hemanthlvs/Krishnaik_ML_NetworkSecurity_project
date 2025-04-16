import os
from datetime import datetime
from networksecurity.constant import training_pipeline

class pipelineconfig():
    def __init__(self,timestamp=datetime.now()):
        datetime = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_dir = training_pipeline.artifact_dir
        self.artifact_time_stamp_dir = os.path.join(self.artifact_dir,datetime)

class ingestionconfig:
    def __init__(self,pipelineconfig:pipelineconfig):
        self.ingestion_dir = os.path.join(pipelineconfig.artifact_time_stamp_dir,training_pipeline.ingestion_dir)
        self.feature_store = os.path.join(self.ingestion_dir,training_pipeline.feature_dir)
        self.ingested = os.path.join(self.ingestion_dir,training_pipeline.data_ingested_dir)
        self.train_data_dir = os.path.join(self.ingested,training_pipeline.training_dir)
        self.test_data_dir = os.path.join(self.ingested,training_pipeline.testing_dir)

# if __name__ == '__main__':
#     # Create an instance of pipelineconfig
#     pipeline_config_instance = pipelineconfig()
#     # Pass the instance to ingestionconfig
#     ingestion_config_instance = ingestionconfig(pipeline_config_instance)
#     # Print the ingestion_dir
#     print(ingestion_config_instance.feature_store)