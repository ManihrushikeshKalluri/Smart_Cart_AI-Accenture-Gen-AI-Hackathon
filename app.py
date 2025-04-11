import streamlit as st
import pandas as pd
import pickle

# Load the trained regression model and encoder
with open("recommender_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# Load product recommendation data
df = pd.read_csv("product_recommendation_data.csv")

# Sidebar
st.sidebar.title("🔍 Smart Shopping Recommender")
categories = df["Category"].unique().tolist()
selected_category = st.sidebar.selectbox("Select a category", categories)

# Filter products by category
filtered_df = df[df["Category"] == selected_category].copy()

# Feature selection
features = filtered_df[["Price", "Product_Rating"]].copy()

# Encode category
encoded = encoder.transform(filtered_df[["Category"]])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(["Category"]))
final_features = pd.concat([features.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)

# Make predictions using regression model
filtered_df["Predicted_Score"] = model.predict(final_features)

# Sort and show top recommendations
top_products = filtered_df.sort_values(by="Predicted_Score", ascending=False).head(10)

# Display recommendations
st.subheader("🎯 Top Product Recommendations")
for _, row in top_products.iterrows():
    st.write(f"🛍️ **{row['Subcategory']}** (ID: {row['Product_ID']}) | "
             f"💵 Price: {row['Price']} | ⭐ Rating: {row['Product_Rating']} | "
             f"📊 Predicted Score: {row['Predicted_Score']:.2f}")
