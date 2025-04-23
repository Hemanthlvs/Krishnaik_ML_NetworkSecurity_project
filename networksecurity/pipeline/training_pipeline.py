import sys
from networksecurity.entity.config_entity import (pipelineconfig, 
                                                  ingestionconfig, 
                                                  validationconfig, 
                                                  transformationconfig, 
                                                  modelconfig)
from networksecurity.entity.artifact_entity import (dataingestion,
                                                    datavalidation,
                                                    transformation,
                                                    data_model)
from networksecurity.component.data_ingestion import ingestion_pipeline
from networksecurity.component.data_validation import data_validation_pipeline
from networksecurity.component.data_transformation import transformation_pipeline
from networksecurity.component.data_modeling import data_modeling_pipeline

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class training_pipeline():
    def __init__(self):
        try:
            self.pipeline_config = pipelineconfig() 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_ingestion_pipeline(self):
        try:
            logging.info("Ingestion started.......")
            ingestion_config = ingestionconfig(self.pipeline_config)
            ingestionPipeline = ingestion_pipeline(ingestion_config)
            ingestionartifacts = ingestionPipeline.initiate_ingestion()
            logging.info("......................Ingestion artifacts......................")
            logging.info(ingestionartifacts)
            logging.info("Ingestion completed")            
            logging.info("###################################################################################################")
            return ingestionartifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_validation_pipeline(self, ingestionartifacts:dataingestion):
        try:
            logging.info("validation started........")
            validation_config = validationconfig(self.pipeline_config)
            validation_pipeline = data_validation_pipeline(ingestionartifacts, validation_config)
            validation_artifacts = validation_pipeline.initiate_validation()
            logging.info("......................Validation artifacts......................")
            logging.info(validation_artifacts)
            logging.info("Validation completed")
            
            logging.info("###################################################################################################")
            return validation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_transformation_pipeline(self, validation_artifacts:datavalidation):
        try:
            logging.info("transformation started........")
            transformation_config = transformationconfig(self.pipeline_config)
            trnsfrmtn_pipeline = transformation_pipeline(validation_artifacts, transformation_config)
            transformation_artifacts = trnsfrmtn_pipeline.initiate_transformation()
            logging.info("......................transformation artifacts......................")
            logging.info(transformation_artifacts)
            logging.info("transformation completed")
            
            logging.info("###################################################################################################")
            return transformation_artifacts
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_training_pipeline(self, transformation_artifacts:transformation)->data_model:
        try:
            logging.info("model training started........")
            modeling_config = modelconfig(self.pipeline_config)
            modeling_pipeline = data_modeling_pipeline(transformation_artifacts, modeling_config)
            model_artifacts = modeling_pipeline.initiate_model_training()
            logging.info("......................model artifacts......................")
            logging.info(model_artifacts)
            logging.info("modeling completed")        
            logging.info("###################################################################################################")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            ingestionartifacts = self.start_ingestion_pipeline()
            validation_artifacts = self.start_validation_pipeline(ingestionartifacts)
            transformation_artifacts = self.start_transformation_pipeline(validation_artifacts)
            model_artifacts = self.start_model_training_pipeline(transformation_artifacts)

            return model_artifacts
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)