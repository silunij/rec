from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

engine = create_engine("postgresql+psycopg2://siluni:SiluAbc@localhost:5432/amazon_rec")

query = """
SELECT user_id, product_id, rating
FROM reviews
"""


df = pd.read_sql(query, engine)

# making the dataset smaller for speed
df = df.sample(n=5000, random_state=42)

#split the data 80%-20% to train and test setss
train, test = train_test_split(df, test_size=0.2, random_state=42)

# create matrix: rows=users, columns=products, values=ratings
user_product_train = train.groupby(['user_id', 'product_id'])['rating'].mean().unstack(fill_value=0)

# compute cosine similarity between users on training data
user_similarity = cosine_similarity(user_product_train)
user_similarity_df = pd.DataFrame(user_similarity, index=user_product_train.index, columns=user_product_train.index)

def predict_rating(user_id, product_id):
    if product_id not in user_product_train.columns or user_id not in user_product_train.index:
        return 0  # unknown product or user

    # similarities of current user to all other users
    sims = user_similarity_df[user_id]
    
    # ratings of other users for the product
    product_ratings = user_product_train[product_id]
    
    # weighted sum
    weighted_sum = np.dot(sims, product_ratings)
    sim_sum = sims.sum()
    if sim_sum == 0:
        return 0
    return weighted_sum / sim_sum

# apply to test set
test['predicted_rating'] = test.apply(lambda x: predict_rating(x['user_id'], x['product_id']), axis=1)

from sklearn.metrics import mean_squared_error

rmse = mean_squared_error(test['rating'], test['predicted_rating'], squared=False)
print(f"RMSE: {rmse:.4f}")

# top 5 recommendations per user
top_k = 5
recommendations = {}
for user in user_product_train.index:
    # predicted ratings for all products
    pred_ratings = {}
    for product in user_product_train.columns:
        pred_ratings[product] = predict_rating(user, product)
    # sort and pick top k
    top_products = sorted(pred_ratings.items(), key=lambda x: x[1], reverse=True)[:top_k]
    recommendations[user] = [p[0] for p in top_products]

# Example: print recommendations for first 5 users
for user, recs in list(recommendations.items())[:5]:
    print(f"User {user}: Top-{top_k} recommendations -> {recs}")