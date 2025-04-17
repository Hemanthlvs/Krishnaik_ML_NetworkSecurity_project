import pandas as pd
import numpy as np
import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_pickle_file


from networksecurity.entity.config_entity import transformationconfig
from networksecurity.entity.artifact_entity import datavalidation,transformation

class transformation_pipeline():
    def __init__(self, validation_artifacts:datavalidation, transformation_config:transformationconfig):
        try:
            self.validation_artifacts = validation_artifacts
            self.transformation_config = transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_csv_data(path):
        try:
            return pd.read_csv(path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def getting_data_ready_for_preprocessing(self, data):
        try:
            input_features = data.drop(columns = [self.transformation_config.target_column], axis=1)
            output_feature = data[self.transformation_config.target_column]
            logging.info("data got divided into input features and output feature")
            output_feature = output_feature.replace(-1,0)
            logging.info("replaced -1's to 0's in output feature")
            return input_features, output_feature
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def preprocessing_data(self):
        try:
            imputer:KNNImputer = KNNImputer(**self.transformation_config.KNN_Imputer_params)
            preprocessor:Pipeline = Pipeline([("imputer",imputer)])
            return preprocessor
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_transformation(self):
        try:
            train_csv_path = self.validation_artifacts.Train_validation_path
            test_csv_path = self.validation_artifacts.Test_validation_path
            logging.info("reading train data")
            train_data = transformation_pipeline.read_csv_data(train_csv_path)
            logging.info("reading test data")
            test_data = transformation_pipeline.read_csv_data(test_csv_path)
            training_input_feature_cleaned, training_output_feature_cleaned = self.getting_data_ready_for_preprocessing(train_data)
            test_input_feature_cleaned, test_output_feature_cleaned = self.getting_data_ready_for_preprocessing(test_data)
            logging.info("starting preprocessing")
            preprocessor = self.preprocessing_data()
            training_preprocessed_data = preprocessor.fit_transform(training_input_feature_cleaned)
            logging.info("preprocessed training data")
            testing_preprocessed_data = preprocessor.transform(test_input_feature_cleaned)
            logging.info("preprocessed testing data")
            processed_training = np.c_[training_preprocessed_data, np.array(training_output_feature_cleaned)]
            processed_testing = np.c_[testing_preprocessed_data, np.array(test_output_feature_cleaned)]
            os.makedirs(os.path.dirname(self.transformation_config.train_file), exist_ok=True)
            save_numpy_array_data(self.transformation_config.train_file, processed_training)
            logging.info(f"train transformation file got loaded into path --> {self.transformation_config.train_file}")
            save_numpy_array_data(self.transformation_config.test_file, processed_testing)
            logging.info(f"test transformation file got loaded into path --> {self.transformation_config.test_file}")
            os.makedirs(os.path.dirname(self.transformation_config.preprocessing_file),exist_ok=True)
            save_pickle_file(self.transformation_config.preprocessing_file, preprocessor)
            logging.info(f"preprocessor object got saved in the path --> {self.transformation_config.preprocessing_file}")
            transformation_artifacts = transformation(
                traindata_transformed_path = self.transformation_config.train_file,
                testdata_transformed_path = self.transformation_config.test_file,
                preprocessing_obj_path = self.transformation_config.preprocessing_file)
            return transformation_artifacts
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
