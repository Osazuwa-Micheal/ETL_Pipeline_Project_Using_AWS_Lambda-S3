import pandas as pd
from lambda_function import transform_chunk, clean_year_column

# Load raw CSV
df_movies = pd.read_csv("dataset/movies.csv")

# Replace missing values
df_movies = df_movies.fillna('null')

# Standardize Movies column and clean Year
df_movies['Movies'] = df_movies['Movies'].str.title()
df_movies['Year'] = df_movies['Year'].apply(clean_year_column)

# Apply final transformations
df_movies = transform_chunk(df_movies)

# Save cleaned CSV locally
df_movies.to_csv("dataset/movies_cleaned_test.csv", index=False)

# Preview
print(df_movies.head())
