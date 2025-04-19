from networksecurity.exception.exception import NetworkSecurityException
import sys


class networkmodel():
    def __init__(self,preprocessor,model):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def predict(self,data):
        try:
            preprocessed_data = self.preprocessor.transform(data)
            predicted_data = self.model.predict(preprocessed_data)
            return predicted_data
        except Exception as e:
            raise NetworkSecurityException(e,sys)