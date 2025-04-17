import os
import sys
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import pipelineconfig, ingestionconfig,validationfig
from networksecurity.entity.artifact_entity import dataingestion
from networksecurity.constant import training_pipeline
from networksecurity.component.data_ingestion import ingestion_pipeline
from networksecurity.component.data_validation import data_validation_pipeline

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

if __name__ == '__main__':
    try:
        logging.info("Ingestion Initiated.......")
        pipeline_config = pipelineconfig()  
        ingestion_config = ingestionconfig(pipeline_config)
        ingestionPipeline = ingestion_pipeline(ingestion_config)
        ingestionartifacts = ingestionPipeline.initiate_ingestion()
        logging.info("......................Ingestion artifacts......................")
        logging.info(ingestionartifacts)
        logging.info("Ingestion completed")
        logging.info("###################################################################################################")
        logging.info("validation initiated........")
        validation_config = validationfig(pipeline_config)
        validation_pipeline = data_validation_pipeline(ingestionartifacts, validation_config)
        validation_artifcats = validation_pipeline.initiate_validation()
        logging.info("......................Validation artifacts......................")
        logging.info(validation_artifcats)
        logging.info("Validation completed")
        logging.info("###################################################################################################")


    except Exception as e:
        NetworkSecurityException(e,sys)