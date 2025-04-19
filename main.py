import os
import sys
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import pipelineconfig, ingestionconfig, validationconfig, transformationconfig, modelconfig
from networksecurity.entity.artifact_entity import dataingestion
from networksecurity.constant import training_pipeline
from networksecurity.component.data_ingestion import ingestion_pipeline
from networksecurity.component.data_validation import data_validation_pipeline
from networksecurity.component.data_transformation import transformation_pipeline
from networksecurity.component.data_modeling import data_modeling_pipeline

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
        validation_config = validationconfig(pipeline_config)
        validation_pipeline = data_validation_pipeline(ingestionartifacts, validation_config)
        validation_artifacts = validation_pipeline.initiate_validation()
        logging.info("......................Validation artifacts......................")
        logging.info(validation_artifacts)
        logging.info("Validation completed")
        
        logging.info("###################################################################################################")
        
        logging.info("transformation initiated........")
        transformation_config = transformationconfig(pipeline_config)
        trnsfrmtn_pipeline = transformation_pipeline(validation_artifacts, transformation_config)
        transformation_artifacts = trnsfrmtn_pipeline.initiate_transformation()
        logging.info("......................transformation artifacts......................")
        logging.info(transformation_artifacts)
        logging.info("transformation completed")
        
        logging.info("###################################################################################################")
        logging.info("modeling initiated........")
        modeling_config = modelconfig(pipeline_config)
        modeling_pipeline = data_modeling_pipeline(transformation_artifacts, modeling_config)
        model_artifacts = modeling_pipeline.initiate_model_training()
        logging.info("......................model artifacts......................")
        logging.info(model_artifacts)
        logging.info("modeling completed")        
        logging.info("###################################################################################################")


    except Exception as e:
        raise NetworkSecurityException(e,sys)