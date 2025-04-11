import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load and clean data
df = pd.read_csv("product_recommendation_data.csv")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.dropna(subset=["Probability_of_Recommendation"])

# 2. Select features and target
features = ['Category', 'Subcategory', 'Brand', 'Price', 
            'Product_Rating', 'Customer_Review_Sentiment_Score', 
            'Average_Rating_of_Similar_Products']
target = 'Probability_of_Recommendation'

# 3. One-hot encode categorical features
cat_features = ['Category', 'Subcategory', 'Brand']
num_features = list(set(features) - set(cat_features))

df_cat = pd.get_dummies(df[cat_features], drop_first=True)
df_num = df[num_features]

# 4. Combine and scale features
X = pd.concat([df_num, df_cat], axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

y = df[target]

# 5. Train/test split and model training
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Predict on all products
df['Predicted_Probability'] = model.predict(X_scaled)

# 7. Create product embeddings (content-based vectors)
cos_sim = cosine_similarity(X_scaled)
similarity_df = pd.DataFrame(cos_sim, index=df['Product_ID'], columns=df['Product_ID'])

# 8. Recommend top products for a sample product
def recommend_similar_products(product_id, top_n=5):
    if product_id not in similarity_df.index:
        return []
    similar_scores = similarity_df[product_id].sort_values(ascending=False)
    top_ids = similar_scores.iloc[1:top_n+1].index.tolist()  # skip the same product
    return df[df['Product_ID'].isin(top_ids)][['Product_ID', 'Subcategory', 'Category', 'Predicted_Probability']]

# 🔍 Recommend top products with highest predicted probability
def top_recommended_products(n=5):
    return df.sort_values(by='Predicted_Probability', ascending=False).head(n)[['Product_ID', 'Subcategory', 'Category', 'Predicted_Probability']]

# -----------------------------
# 🔽 Example Usage
print("🔮 Top ML Predicted Recommended Products:")
print(top_recommended_products())

print("\n🔁 Similar Products to P2002:")
print(recommend_similar_products("P2002"))
