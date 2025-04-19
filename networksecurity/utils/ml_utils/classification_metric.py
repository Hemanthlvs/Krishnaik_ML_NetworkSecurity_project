from sklearn.metrics import f1_score, precision_score, recall_score
from networksecurity.entity.artifact_entity import classification_metrics_artifacts
from networksecurity.exception.exception import NetworkSecurityException
import sys

def classification_metrics(y_true, y_pred):
    try:
        f1score = f1_score(y_true, y_pred)
        precisionscore = precision_score(y_true, y_pred)
        recallscore = recall_score(y_true, y_pred)
        classification_metrics = classification_metrics_artifacts(f1_score = f1score,
                                                            precision_score = precisionscore,
                                                            recall_score = recallscore)
        return classification_metrics
    except Exception as e:
        raise NetworkSecurityException(e,sys)



