import os
import sys
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import pipelineconfig, ingestionconfig
from networksecurity.entity.artifact_entity import dataingestion
from networksecurity.constant import training_pipeline
from networksecurity.component.data_ingestion import ingestion_pipeline

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

if __name__ == '__main__':
    try:
        logging.info("Ingestion Initiated")
        pipeline_config = pipelineconfig()  
        ingestion_config = ingestionconfig(pipeline_config)
        ingestionPipeline = ingestion_pipeline(ingestion_config)
        ingestionartifacts = ingestionPipeline.initiate_ingestion()
        logging.info(f"Artifacts of ingestion : {ingestionartifacts}")
        logging.info("Ingestion completed")

    except Exception as e:
        NetworkSecurityException(e,sys)