import os
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import ingestionconfig
from networksecurity.entity.artifact_entity import dataingestion
from networksecurity.constant import training_pipeline


class ingestion_pipeline():
    def __init__(self, ingestionconfig:ingestionconfig):
        self.ingestion_config = ingestionconfig

    def export_data_from_source(self):
        self.source_data_path = os.path.join(training_pipeline.source_dir,training_pipeline.source_file)
        #self.source_data_path = training_pipeline.source_dir
        df = pd.read_csv(self.source_data_path)
        # Now we are going to replace nan to null values
        df.replace({"na":np.nan}, inplace=True)
        return df
    
    def loading_data(self, dataframe:pd.DataFrame):
        self.load_path = os.path.join(self.ingestion_config.feature_store,training_pipeline.source_file)
        os.makedirs(self.load_path,exist_ok=True)
        dataframe.to_csv(self.load_path,index=False,header=True)

    def initiate_ingestion(self):
        df = self.export_data_from_source()
        load_path = self.loading_data(df)
        return load_path
    


