import pandas as pd
import numpy as np
import os
import sys

from networksecurity.entity.config_entity import validationfig
from networksecurity.entity.artifact_entity import dataingestion, datavalidation
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import read_yaml, write_yaml
from scipy.stats import ks_2samp

class data_validation_pipeline():
    def __init__(self, data_ingestion_artifacts: dataingestion, validation_config:validationfig):
        try:
            self.dataIngestionArtifacts = data_ingestion_artifacts
            self.validationConfig = validation_config
            self._schema = read_yaml(self.validationConfig.SCHEMA_FILE_PATH) 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_csv_data(path):
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def check_column_count(self, df, schema):
        try:
            status = True
            df_count = len(df.columns)            
            schema_count = len(schema['columns'])
            logging.info(f"columns counts : {df_count},{schema_count}")
            if df_count != schema_count:
                False
            return True        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def check_missing_columns(self, df, schema):
        try:
            df_columns = set(df.columns)
            schema_columns = {list(col.keys())[0] for col in schema['columns']}

            missing_columns_in_schema = df_columns - schema_columns
            missing_columns_in_df = schema_columns - df_columns

            if not missing_columns_in_schema and not missing_columns_in_df :
                logging.info("All columns are matching")
                return True
            else:
                logging.info("Below are the columns missing :")
                logging.info(f"missing columns in data : {missing_columns_in_df}")
                logging.info(f"missing columns in schema : {missing_columns_in_schema}")
                return False
        except Exception as e:
            logging.error(f"Error in check_column_count: {e}")
            raise NetworkSecurityException(e, sys)       

    def detect_dataset_drift(self, base_df, current_df, threshold=0.02):
        try:
            report = {}
            status = True
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sump_dist = ks_2samp(d1,d2)
                if threshold <= is_sump_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {"pvalue":float(is_sump_dist.pvalue),
                                        "drift_status":is_found}})
            report_file_path = self.validationConfig.drift_report_file
            os.makedirs(os.path.dirname(report_file_path), exist_ok=True)            
            write_yaml(report_file_path, report)
            logging.info(f"report file : {report_file_path} --> got created and data got loaded into it")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_validation(self):
        try:
            train_data_path = self.dataIngestionArtifacts.train_data_path
            test_data_path = self.dataIngestionArtifacts.test_data_path
            logging.info(f"reading train_data from path --> {train_data_path}")
            train_data = data_validation_pipeline.read_csv_data(train_data_path)
            logging.info(f"reading train_data from path --> {test_data_path}")
            test_data = data_validation_pipeline.read_csv_data(test_data_path)

            logging.info("column count check")
            status = self.check_column_count(train_data, self._schema)
            if not status:
                logging.info("Train dataframe columns count is not matching with given schema")
            else:
                logging.info("Train dataframe columns are matching with schema given")
            status = self.check_column_count(test_data, self._schema)
            if not status:
                logging.info("Test dataframe columns count is not matching with given schema")
            else:
                logging.info("Test dataframe columns are matching with schema given")
            
            logging.info("Missing columns check")
            logging.info("checking missing columns in train data")
            status = self.check_missing_columns(train_data, self._schema)
            if not status:
                logging.info("above are the missing columns details in train data")
            else:
                logging.info("All training data columns are matching with schema")
            logging.info("checking missing columns in test data")
            status = self.check_missing_columns(test_data, self._schema)
            if not status:
                logging.info("above are the missing columns details in test data")
            else:
                logging.info("All training data columns are matching with schema")   
            
            logging.info("data drift started")
            self.detect_dataset_drift(train_data, test_data)
            logging.info("data drift completed")
            os.makedirs(os.path.dirname(self.validationConfig.validated_train_file),exist_ok=True)
            train_data.to_csv(self.validationConfig.validated_train_file, index=False, header=True)
            logging.info(f"Train data loaded into the path ---> {self.validationConfig.validated_train_file}")
            test_data.to_csv(self.validationConfig.validated_test_file, index=False, header=True)
            logging.info(f"Test data loaded into the path ---> {self.validationConfig.validated_test_file}")

            validation_artifacts = datavalidation(validation_status = status,
                                            Train_validation_path = self.validationConfig.validated_train_file,
                                            Test_validation_path = self.validationConfig.validated_test_file,
                                            Drift_report_path = self.validationConfig.drift_report_file,
                                            Train_invalidation_path = None,
                                            Test_invalidation_path = None)
            return validation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
