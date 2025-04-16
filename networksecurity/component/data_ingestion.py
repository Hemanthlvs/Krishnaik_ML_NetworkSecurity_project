import os
import sys
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import ingestionconfig
from networksecurity.entity.artifact_entity import dataingestion
from networksecurity.constant import training_pipeline

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from sklearn.model_selection import train_test_split

class ingestion_pipeline():
    def __init__(self, ingestionconfig:ingestionconfig):
        try:
            self.ingestion_config = ingestionconfig

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_data_from_source(self):
        try:
            self.source_data_path = self.ingestion_config.source
            logging.info("Exporting the data from source folder")
            df = pd.read_csv(self.source_data_path)
            logging.info("created dataframe")
            # Now we are going to replace nan to null values
            df.replace({"na":np.nan}, inplace=True)
            logging.info("replaced na values to nan values")
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def loading_data(self, dataframe:pd.DataFrame):
        try:
            self.load_path = os.path.join(self.ingestion_config.feature_store,training_pipeline.source_file)
            os.makedirs(os.path.dirname(self.load_path), exist_ok=True)
            logging.info(f"{self.load_path} -- path got created")
            dataframe.to_csv(self.load_path,index=False,header=True)
            logging.info(f"data loaded into {self.load_path} -- path")
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def traintest_split(self, df):
        try:
            self.train_file = self.ingestion_config.train_file
            os.makedirs(os.path.dirname(self.train_file), exist_ok=True)
            logging.info(f"{self.train_file} -- path got created")
            self.test_file = self.ingestion_config.test_file
            os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
            logging.info(f"{self.test_file} -- path got created")
            traintestsplit_ratio = self.ingestion_config.traintest_split_ratio
            train_set, test_set = train_test_split(df, test_size = traintestsplit_ratio, random_state=42)
            logging.info(f"Data splitted into train and test")
            train_set.to_csv(self.train_file, index=False, header=True)
            logging.info(f"train data loaded into path -- {self.train_file}")
            test_set.to_csv(self.test_file, index=False, header=True)
            logging.info(f"test data loaded into path -- {self.test_file}")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_ingestion(self):
        try:
            df = self.export_data_from_source()
            df = self.loading_data(df)
            self.traintest_split(df)
            dataingestionartifacts = dataingestion(train_data_path=self.train_file, test_data_path=self.test_file)
            return dataingestionartifacts
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


