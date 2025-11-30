# ETL_Pipeline_Project_Using_AWS_Lambda-S3
This pipeline consumes a raw CSV file (movies.csv) uploaded to an S3 bucket. Once the file is detected, an S3 Event Trigger automatically invokes an AWS Lambda function, which loads the data using Pandas, performs a series of transformations, and delivers a cleaned, standardized dataset into a target S3 bucket for downstream analytics.
