
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



