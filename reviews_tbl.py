from sqlalchemy import create_engine
import pandas as pd

# Adjust username/password/host as needed
engine = create_engine(
    f"postgresql+psycopg2://siluni:SiluAbc@localhost:5432/amazon_rec"
)

# Load cleaned CSV
df = pd.read_csv("data/processed/Reviews_cleaned.csv")

# Push to SQL
df.to_sql('reviews', engine, if_exists='replace', index=False)
print("Data loaded into SQL!")