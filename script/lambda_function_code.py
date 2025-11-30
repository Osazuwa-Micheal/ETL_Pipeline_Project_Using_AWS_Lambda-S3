import boto3
import pandas as pd
import re
import io
import os

s3 = boto3.client("s3")

SOURCE_BUCKET = "my-project-source-data"
TARGET_BUCKET = "my-project-cleaned-data"
SOURCE_KEY = "movies.csv"
TARGET_KEY = "movies_cleaned.csv"

def lambda_handler(event, context):
    print("=== STARTING CSV ETL ===")

    # ---------------------------------------------------------
    # 1. DOWNLOAD FILE FROM SOURCE S3 BUCKET
    # ---------------------------------------------------------
    print(f"Downloading s3://{SOURCE_BUCKET}/{SOURCE_KEY} ...")

    obj = s3.get_object(Bucket=SOURCE_BUCKET, Key=SOURCE_KEY)
    df_movies = pd.read_csv(io.BytesIO(obj["Body"].read()))

    print("Loaded CSV. Initial shape:", df_movies.shape)

    # ---------------------------------------------------------
    # 2. ---- CLEANING LOGIC (Your Full Cleaning Code) ----
    # ---------------------------------------------------------

    # --- Step 1: Replace Missing Values with 'null' ---
    print("Replacing missing values with 'null'...")
    df_movies = df_movies.fillna('null')
    print("Missing values after replacement:")
    print(df_movies.isnull().sum())

    # --- Step 2: Standardize 'MOVIES' column and column headings ---
    print("\nStandardizing 'MOVIES' column and column headings...")
    df_movies['MOVIES'] = df_movies['MOVIES'].str.title()
    df_movies.columns = [col.title() for col in df_movies.columns]
    print("After standardizing columns:")
    print(df_movies.head().to_string())

    # --- Step 3: Clean 'Year' column ---
    print("\nCleaning 'Year' column...")

    def clean_year_column(year_str):
        if year_str == 'null':
            return 'null'

        match_range = re.search(r'\((\d{4})[–-](\d{4})\)', year_str)
        if match_range:
            return f"{match_range.group(1)} - {match_range.group(2)}"

        match_ongoing = re.search(r'\((\d{4})[–-]\s*\)', year_str)
        if match_ongoing:
            return match_ongoing.group(1)

        match_single = re.search(r'\((\d{4})\)', year_str)
        if match_single:
            return match_single.group(1)

        return year_str

    df_movies['Year'] = df_movies['Year'].apply(clean_year_column)
    print("After cleaning 'Year' column:")
    print(df_movies.head().to_string())

    # --- Step 4: Further Clean 'Movies' column ---
    print("\nFurther cleaning 'Movies' column...")
    df_movies['Movies'] = df_movies['Movies'].str.strip()
    df_movies['Movies'] = df_movies['Movies'].str.replace(r'\s+', ' ', regex=True)
    df_movies['Movies'] = df_movies['Movies'].apply(
        lambda x: re.sub(r"[^a-zA-Z0-9\s\'-]", '', x)
    )

    print("After cleaning 'Movies' column:")
    print(df_movies.head().to_string())

    # --- Step 5: Final cleaning: duplicates, whitespace, renaming, snake_case ---
    print("\nFinal transformations...")

    df_movies.drop_duplicates(inplace=True)
    print(f"Shape after removing duplicates: {df_movies.shape}")

    # Trim whitespace
    for col in df_movies.select_dtypes(include=['object']).columns:
        df_movies[col] = df_movies[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    print("Trimmed whitespaces.")

    # Rename columns
    df_movies.rename(columns={
        'Gross': 'Gross_income',
        'Movies': 'Movie_title'
    }, inplace=True)

    print("Renamed 'Gross' -> 'Gross_income', 'Movies' -> 'Movie_title'.")

    # Snake case conversion
    def to_snake_case(name):
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        return name.lower()

    df_movies.columns = [to_snake_case(col) for col in df_movies.columns]

    print("Converted headers to snake_case.")

    print("\nFinal DataFrame preview:")
    print(df_movies.head().to_string())

    # ---------------------------------------------------------
    # 3. SAVE CLEANED CSV TO TARGET S3 BUCKET
    # ---------------------------------------------------------
    print(f"\nUploading cleaned file to s3://{TARGET_BUCKET}/{TARGET_KEY} ...")

    csv_buffer = io.StringIO()
    df_movies.to_csv(csv_buffer, index=False)

    s3.put_object(
        Bucket=TARGET_BUCKET,
        Key=TARGET_KEY,
        Body=csv_buffer.getvalue().encode("utf-8")
    )

    print("Upload complete.")

    print("=== ETL COMPLETED SUCCESSFULLY ===")

    return {
        "status": "success",
        "rows_cleaned": len(df_movies),
        "output_file": f"s3://{TARGET_BUCKET}/{TARGET_KEY}"
    }
