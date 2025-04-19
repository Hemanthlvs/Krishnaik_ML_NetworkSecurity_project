import yaml
import sys
import os
import numpy as np
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml(file_path):
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml(file_path, content):
    try:
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array_data(file_path, array):
    try:
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_pickle_file(file_path, content):
    try:
        with open(file_path, "wb") as file:
            pickle.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_pickle_file(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_array_data(file_path):
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException
    
def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]
            gs = GridSearchCV(model, param, cv=3)
            gs.fit(X_train,y_train)

            best_params = gs.best_params_
            model.set_params(**best_params)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            r2_score_train = r2_score(y_train, y_train_pred)
            r2_score_test = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = r2_score_test
        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)