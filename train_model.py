import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder

# Load the data
df = pd.read_csv("product_recommendation_data.csv")

# Features and target
features = df[["Price", "Product_Rating"]]
categories = df[["Category"]]

# Encode the category column
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
encoded = encoder.fit_transform(categories)
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(["Category"]))

# Combine features
X = pd.concat([features.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
y = df["Product_Rating"]  # Use Product_Rating as target for scoring

# Train regression model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model and encoder
with open("recommender_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("✅ Model and encoder saved as recommender_model.pkl and encoder.pkl")
