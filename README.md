# Network Security Project

## Introduction
The "Network Security" project aims to build a machine learning pipeline that detects phishing attacks. Phishing is a type of cyber attack where attackers impersonate legitimate organizations to steal sensitive information. This project involves several stages, including data ingestion, validation, transformation, modeling, and prediction. The goal is to create a robust system that can effectively identify phishing attempts and enhance network security.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation Instructions](#installation-instructions)
3. [Usage](#usage)
4. [Project Workflow](#project-workflow)
5. [Scripts Overview](#scripts-overview)
   - [Data Ingestion](#data-ingestion)
   - [Data Validation](#data-validation)
   - [Data Transformation](#data-transformation)
   - [Modeling](#modeling)
   - [Prediction](#prediction)
   - [Training Pipeline](#training-pipeline)
   - [S3 Syncer](#s3-syncer)
   - [Dockerfile](#dockerfile)
   - [Setup.py](#setup.py)
   - [Logger](#logger)
   - [Exception Handling](#exception-handling)
6. [Key Concepts](#key-concepts)
   - [MLflow](#mlflow)
   - [DagsHub](#dagshub)
7. [Dependencies](#dependencies)
8. [Future Improvements](#future-improvements)
9. [Conclusion](#conclusion)
10. [References](#references)

bash
## Installation Instructions
To set up the project on your local machine, follow these steps:
1. Clone the repository:
   ```bash
   git clone <repository-url>

Navigate to the project directory:
bash
cd NetworkSecurity

Install the required packages using:
bash
pip install -r requirements.txt

Usage
Start the FastAPI application:
bash
uvicorn app:app --reload

Access the API documentation at http://127.0.0.1:8000/docs.
Use the /train endpoint to train the model.
Use the /predict endpoint to make predictions by uploading a CSV file.
Project Workflow

The project follows a sequential workflow, which can be broken down into the following stages:

Data Ingestion: The first step involves loading the raw data from a source file (e.g., phishingdata.csv). The data is cleaned, and any missing values are handled. The cleaned data is then split into training and testing datasets.

Data Validation: After ingestion, the data is validated against a predefined schema. This step checks for missing columns, data types, and data drift (changes in data distribution). If the data fails validation, it is flagged for further inspection.

Data Transformation: The validated data undergoes preprocessing, where features are transformed, and missing values are imputed. The transformed data is saved for model training.

Model Training: In this stage, various machine learning models are trained using the transformed data. The models are evaluated based on performance metrics (e.g., accuracy, F1 score), and the best-performing model is selected for deployment.

Prediction: Once the model is trained, it can be used to make predictions on new data. The predictions are returned to the user, along with any relevant information.

Scripts Overview
Data Ingestion
File: data_ingestion.py
Purpose: To load data from the source, clean it, and split it into training and testing datasets.
Key Functions:
export_data_from_source(): Loads data from the source CSV file and replaces any 'na' values with NaN.
loading_data(): Saves the cleaned data to the feature store for further processing.
traintest_split(): Splits the data into training and testing sets based on a specified ratio.
Data Validation
File: data_validation.py
Purpose: To validate the data against a predefined schema and check for data drift.
Key Functions:
check_column_count(): Validates the number of columns in the dataset against the schema.
check_missing_columns(): Checks for any missing columns in the dataset.
detect_dataset_drift(): Identifies any drift in the dataset compared to the training data using statistical tests.
Data Transformation
File: data_transformation.py
Purpose: To preprocess the data by handling missing values and transforming features.
Key Functions:
getting_data_ready_for_preprocessing(): Prepares input and output features for modeling.
preprocessing_data(): Creates a preprocessing pipeline using KNN imputer to handle missing values.
Modeling
File: data_modeling.py
Purpose: To train machine learning models and evaluate their performance.
Key Functions:
model_training(): Trains multiple models (e.g., Random Forest, Decision Tree) and selects the best one based on performance metrics.
track_mlflow(): Logs model metrics and artifacts using MLflow for tracking experiments.
Prediction
File: batch_prediction.py
Purpose: To make predictions on new data using the trained model.
Key Functions:
start_prediction(): Loads the model and preprocessor, then predicts on the input data.
Training Pipeline
File: training_pipeline.py
Purpose: To orchestrate the entire machine learning workflow, including data ingestion, validation, transformation, and model training.
Key Functions:
start_ingestion_pipeline(): Initiates the data ingestion process.
start_validation_pipeline(): Initiates the data validation process.
start_transformation_pipeline(): Initiates the data transformation process.
start_model_training_pipeline(): Initiates the model training process.
run_pipeline(): Runs the entire pipeline sequentially, ensuring that each step is completed before moving to the next.
S3 Syncer
File: s3_syncer.py
Purpose: To synchronize local directories with AWS S3 buckets for backup and deployment.
Key Functions:
sync_folder_to_s3(): Syncs a local folder to a specified S3 bucket.
sync_folder_from_s3(): Syncs a specified S3 bucket to a local folder.
Dockerfile
File: Dockerfile
Purpose: To create a Docker image for the application, allowing it to run in a containerized environment.
Key Instructions:
FROM python:3.10-slim-buster: Specifies the base image.
WORKDIR /app: Sets the working directory inside the container.
COPY . /app: Copies the project files into the container.
RUN apt update -y && apt install awscli -y: Installs necessary packages.
RUN pip install -r requirements.txt: Installs Python dependencies.
CMD ["python3", "app.py"]: Specifies the command to run the application.
Setup.py
File: setup.py
Purpose: To define the package metadata and dependencies for the project, allowing it to be installed as a package.
Key Functions:
get_requirements(): Reads the requirements.txt file and returns a list of dependencies.
setup(): Uses the setuptools library to define the package name, version, author, and install requirements.
Logger
File: logger.py
Purpose: To configure logging for the application, allowing for tracking of events and errors.
Key Configuration:
Sets the log file path and format.
Configures the logging level to INFO.
Exception Handling
File: exception.py
Purpose: To define custom exceptions for the project, providing better error handling and debugging.
Key Class:
NetworkSecurityException: Custom exception that captures error messages and details, including the line number and file name where the error occurred.
Key Concepts
MLflow

MLflow is an open-source platform for managing the machine learning lifecycle, including experimentation, reproducibility, and deployment. It provides tools to track experiments, log metrics, and manage models.

Example: In this project, MLflow is used to log the performance metrics of different models during training. This allows you to compare models and select the best one based on metrics like F1 score and accuracy.

DagsHub

DagsHub is a platform for managing machine learning projects, similar to GitHub but tailored for data science. It allows teams to collaborate on projects, track experiments, and share datasets.

Example: DagsHub can be used to store the project's code, datasets, and MLflow tracking information, making it easier for team members to collaborate and access the latest updates.

Dependencies

The project relies on several Python libraries:

pandas: For data manipulation and analysis.
numpy: For numerical operations and handling arrays.
scikit-learn: For implementing machine learning algorithms.
mlflow: For tracking experiments and managing models.
fastapi: For building the web API to interact with the model.
uvicorn: ASGI server for running the FastAPI application.
Future Improvements
Implement more advanced models and techniques for better accuracy, such as ensemble methods or deep learning.
Add more extensive logging and monitoring features to track model performance in production.
Explore cloud deployment options (e.g., AWS, Azure) for scalability and accessibility.
Conclusion

The "Network Security" project demonstrates a complete machine learning pipeline for detecting phishing attacks. Each component is modular, making it easy to update or replace parts of the pipeline as needed. The project serves as a valuable reference for building similar machine learning applications in the future.

