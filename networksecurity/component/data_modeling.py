import pandas as pd
import numpy as np
import sys
import os
import mlflow

from networksecurity.entity.config_entity import modelconfig
from networksecurity.entity.artifact_entity import transformation, data_model
from networksecurity.utils.main_utils.utils import load_array_data, evaluate_model, write_yaml, load_pickle_file, save_pickle_file
from networksecurity.utils.ml_utils.classification_metric import classification_metrics
from networksecurity.utils.ml_utils.estimator import networkmodel

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

# import dagshub
# dagshub.init(repo_owner='Hemanthlvs', repo_name='Krishnaik_ML_NetworkSecurity_project', mlflow=True)
# #by using dagshug we are creating mlflow experiments in dagshub instead of local machine.
# #for this we need to create a account in dagshub and connect that with guthub.

class data_modeling_pipeline():
    def __init__(self, transformation_artifacts: transformation, model_config:modelconfig):
        try:
            self.transformation_artifacts = transformation_artifacts
            self.model_config = model_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self, best_model, classification_metrics):
        with mlflow.start_run():
            f1_score = classification_metrics.f1_score
            precision_score = classification_metrics.precision_score
            recall_score = classification_metrics.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    def model_training(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "random forest": RandomForestClassifier(verbose=1),
                "decision tree": DecisionTreeClassifier(),
                "gradinet boosting": GradientBoostingClassifier(verbose=1),
                "logistic regression": LogisticRegression(verbose=1),
                "Ada boost": AdaBoostClassifier()
                }
            
            params = {
                "random forest": {
                    # 'criterion':['gini', 'entropy', 'log_loss'],                
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                    },
                "decision tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                    },
                "gradinet boosting": {
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                    },
                "logistic regression": {},
                "Ada boost": {
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                    }
            }
            logging.info("started model evaluation")
            models_report = evaluate_model(X_train, y_train, X_test, y_test, models=models, params=params)
            logging.info("model evaluation completed")
            os.makedirs(os.path.dirname(self.model_config.models_report), exist_ok=True)
            logging.info("report: models_report")
            write_yaml(self.model_config.models_report, models_report)
            logging.info(f"models report file created in the path --> {self.model_config.models_report}")

            logging.info("selecting model based on best r2_score")
            best_r2_score = max(models_report.values())
            best_model_name = list(models_report.keys())[list(models_report.values()).index(best_r2_score)]
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(X_train)
            train_classification_metrics = classification_metrics(y_train,y_train_pred)
            logging.info("..........................train classfication metrics............................")
            logging.info(train_classification_metrics)
            ## Tracking the experiements with mlflow
            self.track_mlflow(best_model,train_classification_metrics)

            y_test_pred = best_model.predict(X_test)
            test_classification_metrics = classification_metrics(y_test,y_test_pred)
            logging.info("..........................test classfication metrics............................")
            logging.info(test_classification_metrics)
            ## Tracking the experiements with mlflow
            self.track_mlflow(best_model,test_classification_metrics)


            save_pickle_file(self.model_config.model_file, best_model)
            logging.info(f"best model saved in the path --> {self.model_config.model_file}")

            preprocessor = load_pickle_file(self.transformation_artifacts.preprocessing_obj_path)
            network_model = networkmodel(preprocessor, best_model)

            os.makedirs(os.path.dirname(self.model_config.final_model_file_path), exist_ok=True)
            save_pickle_file(self.model_config.final_model_file_path, best_model)
            logging.info(f"Final model loaded into the path --> {self.model_config.final_model_file_path}")

            os.makedirs(os.path.dirname(self.model_config.final_transformed_obj_path), exist_ok=True)
            save_pickle_file(self.model_config.final_transformed_obj_path, preprocessor)
            logging.info(f"Final model loaded into the path --> {self.model_config.final_transformed_obj_path}")
            
            data_model_artifacts = data_model(
                models_report_path = self.model_config.models_report,
                best_model_path = self.model_config.model_file,
                trained_classification_metrics = train_classification_metrics,
                test_classification_metrics = test_classification_metrics
            )

            return data_model_artifacts



        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_model_training(self):
        try:
            train_path = self.transformation_artifacts.traindata_transformed_path
            test_path = self.transformation_artifacts.testdata_transformed_path

            train_data = load_array_data(train_path)
            test_data = load_array_data(test_path)

            X_train = train_data[:,:-1]
            y_train = train_data[:,-1]

            X_test = test_data[:,:-1]
            y_test = test_data[:,-1]

            data_model_artifacts = self.model_training(X_train,y_train,X_test,y_test)

            return data_model_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    
