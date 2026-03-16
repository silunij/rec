import pandas as pd

# Load raw data
file_path = "data/raw/Reviews.csv" 
df = pd.read_csv(file_path)

# Keep only relevant columns
df = df[['UserId', 'ProductId', 'Score', 'Text']]

# Rename columns properly
df.rename(columns={
    'UserId': 'user_id',
    'ProductId': 'product_id',
    'Score': 'rating',
    'Text': 'review_text'
}, inplace=True)  # ensures df is updated

# Save cleaned data to processed folder
df.to_csv("data/processed/Reviews_cleaned.csv", index=False)

print(df.head())