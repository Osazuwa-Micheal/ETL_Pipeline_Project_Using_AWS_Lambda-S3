# ETL Pipeline Project Using (AWS Lambda + S3)

## 🚀 Project Overview

This repository contains a **serverless data engineering ETL pipeline** designed to clean, standardize, and transform a raw **movies.csv** dataset stored in Amazon S3.  
The pipeline is implemented entirely using **AWS Lambda**, **Python**, **pandas**, and **S3**, following modern, cloud-native data engineering practices.

The goal of this project is to demonstrate how to build a **production-ready, scalable, event-driven ETL workflow** using AWS services — suitable for real deployments, portfolio projects, and enterprise data pipelines.

---

## 🎯 Key Objectives

- Build a **fully automated ETL pipeline** using serverless architecture  
- Read raw CSV data from an S3 bucket (full-load processing)  
- Clean and transform the dataset using `pandas`  
- Enforce data quality rules and standardization  
- Store the processed dataset in a target S3 bucket  
- Produce detailed logs that illustrate every stage of the transformation  
- Demonstrate practical skills in **cloud data engineering**

---

## 🏗 Architecture

The ETL pipeline follows a simple but powerful serverless design:
![AWS Architecture](https://github.com/Osazuwa-Micheal/ETL_Pipeline_Project_Using_AWS_Lambda-S3/blob/main/document/AWS_Architecture.png)

This architecture provides:

- **Zero-server management**  
- **Horizontal scalability**  
- **Low cost**  
- **Event-driven automation**  
- **Fast deployment and iteration**
---

## 📦 Data Flow Description

1. **Event Trigger**  
   When `movies.csv` is uploaded to the source bucket (`my-project-source-data`), S3 triggers the Lambda.

2. **Extract**  
   Lambda downloads the full CSV file into memory using pandas.  
   (`chunksize` is not used; full load is intentional).

3. **Transform**  
   The following transformations are performed:
   - Replace missing values with `'null'`
   - Standardize movie titles  
   - Normalize text fields  
   - Clean and standardize the `Year` column  
   - Remove duplicates  
   - Convert all column names to `snake_case`
   - Validate row retention (basic data quality check)

4. **Load**  
   The cleaned dataset is saved into the target S3 bucket:

5. **Logging**  
  Detailed `print()` statements document:
  - Row counts  
  - Cleaning steps  
  - Before/after statistics  
  - ETL success status
    
---

## 🧹 Data Cleaning Rules (Transformation Logic)

### **1. Handle Missing Values**
All `NaN` entries are replaced with the string `'null'`.

### **2. Standardize Movie Titles**
- Trim whitespace  
- Normalize spacing  
- Convert to Proper Case  
- Remove punctuation & special characters  

### **3. Clean Movie Year**
The pipeline supports multiple inconsistent formats:
- `2001–2003` → cleaned  
- `2015–` → to "2015"  
- `(2009)` → stripped to `2009`  
- `N/A` → handled  

### **4. Column Standardization**
All column names are converted to:
snake_case


### **5. Deduplication**
Exact duplicates are removed to ensure a clean dataset.

---

## 🛠 Technologies Used

- **Python 3.12**  
- **AWS Lambda** (serverless ETL)
  <img width="1882" height="757" alt="image" src="https://github.com/user-attachments/assets/7c1381c8-b51e-430f-96fb-778371eb9912" />
 
- **AWS S3** (source and target storage)
  <img width="1883" height="756" alt="image" src="https://github.com/user-attachments/assets/babfd39c-d9a4-4675-bfbb-aadebfbbddb8" />
 
- **AWS CloudWatch** (metrics and logging)
  <img width="1875" height="755" alt="image" src="https://github.com/user-attachments/assets/2f0d24ba-5851-475e-a46b-5a8f476d6875" />

  
- **pandas** (data cleaning and transformation)  
- **re (regex)** (string and year processing)

This reflects a typical **Lakehouse / Data Lake ETL pattern** on AWS.

---

## 🚀 Deployment Instructions

1. Create a Lambda function (Python 3.12 runtime)  
2. Attach an IAM role with **S3 read/write permissions**  
3. Package **pandas** as a Lambda Layer or include in deployment zip  
4. Configure the following **environment variables**:

| Variable | Description | Example |
|----------|-------------|---------|
| SOURCE_BUCKET | S3 bucket containing raw CSV | my-project-source-data |
| TARGET_BUCKET | S3 bucket for cleaned CSV | my-project-cleaned-data |
| INPUT_FOLDER | Prefix/folder in source bucket | "" |
| OUTPUT_FOLDER | Prefix/folder in target bucket | movies-cleaned |
| OVERWRITE_OUTPUT | Overwrite existing target files (`true`/`false`) | false |
| MIN_ROW_RETENTION | Minimum % of rows to retain after cleaning | 10 |
| TMP_OUTPUT_FILENAME | Optional temporary local file path | "" |
| METRIC_NAMESPACE | CloudWatch metric namespace | MoviesETL |

5. Set Lambda **memory to 1024 MB** and **timeout to 2 minutes**  
6. Add **S3 trigger** for new objects in `my-project-source-data`  
7. Upload code and deploy  

---

## 📚 Use Cases

This project demonstrates real data engineering skills, including:

- Building a scalable serverless ETL pipeline  
- Cleaning semi-structured CSV data  
- Designing cloud data workflows  
- Applying data quality checks  
- Using AWS console and IAM policies  
- Preparing datasets for analytics or downstream systems  

Perfect for:

- Portfolios  
- Interviews  
- Real production solutions  
- Automation workflows  

---

## 📄 License
MIT License — Feel free to use and modify.


