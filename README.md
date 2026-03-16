# Customer product recommendation system

End-to-end recommendation system built with Python, PostgreSQL, and Streamlit, implementing collaborative filtering to generate personalized product recommendations.

The system analyzes user-product rating data, computes user similarity using cosine similarity, and recommends products that similar users liked.

The project also includes a Streamlit dashboard that allows users to interactively view recommendations.

## Dataset

Amazon Reviews Dataset

The dataset contains:
user IDs
product IDs
product ratings
review text

The recommendation system uses User-Based Collaborative Filtering.

## Steps

Build a user-product rating matrix
Compute cosine similarity between users
Identify the most similar users
Recommend products liked by similar users that the target user has not rated.

## The Streamlit dashboard allows users to

Select a user ID
View top recommended products
Adjust number of recommendations
Explore dataset statistics

## project structure

product-recommender/
│
├── data/
    ├── raw/
│       └── Reviews.csv
    ├── processed/
│       └── recommendations.csv
|       └── Reviews_cleaned.csv
│
├── load_data.py
├── recommender.py
├── evaluation.py
├── app.py
└── README.md
