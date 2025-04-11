import pandas as pd
import random

# Load the product data
df = pd.read_csv("product_recommendation_data.csv")

# Generate random Customer_IDs if not present
if 'Customer_ID' not in df.columns:
    df["Customer_ID"] = [f"C{random.randint(1, 10)}" for _ in range(len(df))]

# Save the updated CSV
df.to_csv("product_recommendation_data.csv", index=False)
print("✅ Customer_ID column added and data saved.")
