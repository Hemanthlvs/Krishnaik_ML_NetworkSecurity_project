
"common constants required"
artifact_dir:str = 'Artifact'
train_file:str = 'train.csv'
test_file:str = 'test.csv'
Target_column = 'Result'

"Constants required for Ingestion"
source_dir:str = 'Source'
source_file:str = 'phisingData.csv'
ingestion_dir:str = 'ingestion'
feature_dir:str = 'feature_data'
data_ingested_dir:str = 'ingested'
training_dir:str = 'training_data'
testing_dir:str = 'testing_data'
train_test_split_ratio:float = 0.2


"Constants required for Validation"
datavalidation_dir:str = 'datavalidation'
validated_dir:str = 'validated'
invalidated_dir:str = 'invalidated'
drift_report_dir:str = 'drift_report'
drift_report_file:str = 'report.yaml'
schema_folder:str = 'data_schema'
schema_file:str = 'schema.yaml'


"Constants required for transformation"
transformation_dir = 'data_transformation'
transformed_dir = 'transformed'
transformed_obj = 'transformed_object'
preprocessing_file = 'preprocessing.pkl'
final_transformed_obj_folder = 'final_Transformer'
final_transformed_obj = 'preprocessing.pkl'


"Constants required for transformation"
model_dir = 'model_trainer'
model_trained_dir = 'trained_model'
model_file_name = 'model.pkl'
models_report_file = 'models_report'
final_folder = 'final'
final_model_folder = 'model'
final_model_file = 'model.pkl'