#!/bin/bash
#This file generates the enviroment variables needed to operate the system. From here, you
#can modify it's values.
#After creating these variables, the script initiates the containers and run's the system.

#-----------------------------

#Set Airflow constants

# Set Airflow UID
AIRFLOW_UID=$(id -u)

#Set Airflow GID
AIRFLOW_GID="0"
#-----------------------------

#Set Stocks DB constants

#Set Stocks DB user
STOCKS_DB_USER="lionelb"

#Set Stocks DB pass
STOCKS_DB_PASS="pass"

#Set DB name
STOCKS_DB_NAME="stocks"

#-----------------------------

#Staging Area

#Set path to directory where staging data will be saved within the worker container.
#Keep in mind that the YAML file has mounted a default directory to the host, so if you change
#the staging directory, you might need to change the mounted directory also.

STAGING_PATH="/opt/airflow/tmp_data"

#Stocks API Key
STOCKS_API_KEY="9JSQ9RIN9I4YN1NS"
#-----------------------------

#Stocks to follow
STOCKS_LS="MSFT,AMZN,GOOG"
#-----------------------------

#S3 Bucket
#S3 AWS Bucket Name where daily report will be uploaded
S3_BUCKET="stocks-daily-report"

#Generate .env file
echo -e "AIRFLOW_UID=${AIRFLOW_UID}
AIRFLOW_GID=${AIRFLOW_GID}
STOCKS_DB_USER=${STOCKS_DB_USER}
STOCKS_DB_PASS=${STOCKS_DB_PASS}
STOCKS_DB_NAME=${STOCKS_DB_NAME}
STAGING_PATH=${STAGING_PATH}
STOCKS_API_KEY=${STOCKS_API_KEY}
STOCKS_LS=${STOCKS_LS}
S3_BUCKET=${S3_BUCKET}" > .env

# Init airflow db metadata
docker-compose up airflow-init

# Run airflow
docker-compose up -d
