import pandas as pd
import sqlite3
import random

# Load existing customer and product data
customers_df = pd.read_csv("customer_data_collection.csv")
products_df = pd.read_csv("product_recommendation_data.csv")

# Simulate customer-product interactions
interactions = []

for _, customer in customers_df.iterrows():
    customer_id = customer["Customer_ID"]
    sampled_products = products_df.sample(n=5)  # Simulate viewing 5 random products

    for _, product in sampled_products.iterrows():
        interactions.append({
            "Customer_ID": customer_id,
            "Product_ID": product["Product_ID"],
            "Category": product["Category"],
            "Rating": product["Product_Rating"]
        })

interactions_df = pd.DataFrame(interactions)

# Save to database
conn = sqlite3.connect("smart_shopping.db")
interactions_df.to_sql("customer_product_interactions", conn, if_exists="replace", index=False)
conn.close()

print("✅ Simulated interaction history saved to DB!")
