import os
import pandas as pd
import numpy as np
from networksecurity.entity.config_entity import pipelineconfig, ingestionconfig
from networksecurity.entity.artifact_entity import dataingestion
from networksecurity.constant import training_pipeline
from networksecurity.component.data_ingestion import ingestion_pipeline

if __name__ == '__main__':
    pipeline_config = pipelineconfig()  
    ingestion_config = ingestionconfig(pipeline_config)
    pipeline_instance = ingestion_pipeline(ingestion_config)
    source_data_path = pipeline_instance.initiate_ingestion()
    print(source_data_path)