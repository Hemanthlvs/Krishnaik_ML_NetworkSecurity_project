import pandas as pd
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.estimator import networkmodel
from networksecurity.utils.main_utils.utils import load_pickle_file
from networksecurity.entity.config_entity import pipelineconfig, modelconfig

class data_prediction():
    def __init__(self):
        try:
            logging.info("started predicting........")
            self.pipeline_config = pipelineconfig() 
            self.model_config = modelconfig(self.pipeline_config)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_prediction(self, df):
        try:            
            logging.info("loading preprocessor from final path")
            preprocessor = load_pickle_file(self.model_config.final_transformed_obj_path)

            logging.info("loading model from final path")
            model = load_pickle_file(self.model_config.final_model_file_path)

            network_model = networkmodel(preprocessor,model)

            logging.info("reading the data that needs to be predicted")
            # df = pd.read_csv("valid_data/test.csv")
            logging.info(df)
            
            predicted_data = network_model.predict(df)
            logging.info("below is the predicted data")
            logging.info(predicted_data)

            return predicted_data

        except Exception as e:
            raise NetworkSecurityException(e,sys)