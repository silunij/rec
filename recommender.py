import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity

engine = create_engine("postgresql+psycopg2://siluni:SiluAbc@localhost:5432/amazon_rec")

query = """
SELECT user_id, product_id, rating
FROM reviews
"""
#read from the query.
df = pd.read_sql(query, engine)

print(df.head())
print(df.shape)

#reduce data size to make it process faster
df = df.sample(3000, random_state=42)

# create user product matrix
user_product_matrix = df.pivot_table(
    index="user_id",
    columns="product_id",
    values="rating"
)

print(user_product_matrix.shape)

#fill missing values
user_product_matrix = user_product_matrix.fillna(0)



similarity = cosine_similarity(user_product_matrix)

print(similarity)

similarity_df = pd.DataFrame(
    similarity,
    index=user_product_matrix.index,
    columns=user_product_matrix.index
)

print(similarity_df.head())


recommendations = []

for user in user_product_matrix.index:

    # find similar users
    similar_users = similarity_df[user].sort_values(ascending=False)[1:6]

    # get products the user hasn't rated
    user_ratings = user_product_matrix.loc[user]
    unrated_products = user_ratings[user_ratings == 0].index

    # score products
    scores = {}

    for sim_user, sim_score in similar_users.items():
        sim_user_ratings = user_product_matrix.loc[sim_user]

        for product in unrated_products:
            rating = sim_user_ratings[product]

            if rating > 0:
                scores[product] = scores.get(product, 0) + sim_score * rating

    # top 5 products
    top_products = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    for product, score in top_products:
        recommendations.append({
            "user_id": user,
            "product_id": product,
            "score": score
        })

recommendations_df = pd.DataFrame(recommendations)

print(recommendations_df.head())

recommendations_df.to_csv(
    "data/processed/recommendations.csv",
    index=False
)

print("Recommendations saved!")

