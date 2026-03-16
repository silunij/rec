import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://siluni:SiluAbc@localhost:5432/amazon_rec")

st.title("Product Recommendation System")

# load recommendations
df = pd.read_csv("data/processed/recommendations.csv")

# unique users
users = df["user_id"].unique()


user_id = st.sidebar.selectbox("Select User", users)

st.sidebar.markdown("### Dataset Stats")

st.sidebar.metric("Total Users", df["user_id"].nunique())
st.sidebar.metric("Total Products", df["product_id"].nunique())


user_recs = df[df["user_id"] == user_id]

st.subheader("Top Recommended Products")


for _, row in user_recs.iterrows():
    st.write(f"Product ID: {row['product_id']}")

top_products = df["product_id"].value_counts().head(10)

st.subheader("Most Recommended Products")

query = """
SELECT product_id, AVG(rating) as avg_rating
FROM reviews
GROUP BY product_id
ORDER BY avg_rating DESC
LIMIT 10
"""
top_products = pd.read_sql(query, engine)

st.subheader("Top Rated Products")

st.bar_chart(top_products)

num_recs = st.sidebar.slider("Number of Recommendations", 3, 10, 5)

user_recs = df[df["user_id"] == user_id].head(num_recs)

st.set_page_config(
    page_title="Product Recommender",
    page_icon="🛒",
    layout="wide"
)

st.caption("Built with Python, PostgreSQL, Scikit-learn, and Streamlit")