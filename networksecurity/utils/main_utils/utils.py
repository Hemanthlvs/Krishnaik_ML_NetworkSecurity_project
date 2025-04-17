import yaml
import sys
import os
import numpy as np
import pickle

from networksecurity.exception.exception import NetworkSecurityException

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