import pandas as pd
import sqlite3

# Load CSV files
interactions_df = pd.read_csv("product_recommendation_data.csv")
customers_df = pd.read_csv("customer_data_collection.csv")

# Clean column names
interactions_df.columns = interactions_df.columns.str.strip()
customers_df.columns = customers_df.columns.str.strip()

# Remove 'Unnamed' columns if they exist
interactions_df = interactions_df.loc[:, ~interactions_df.columns.str.contains('^Unnamed')]
customers_df = customers_df.loc[:, ~customers_df.columns.str.contains('^Unnamed')]

# Drop rows with missing Product_ID (just in case)
interactions_df = interactions_df[interactions_df["Product_ID"].notnull()]

# ✅ Debug previews
print("🧪 RAW Interactions Preview:")
print(interactions_df.head())
print("\n🧪 RAW Customers Preview:")
print(customers_df.head())

# Connect to SQLite database
conn = sqlite3.connect("smart_shopping.db")

# Save cleaned data to tables
interactions_df.to_sql("interactions", conn, if_exists="replace", index=False)
customers_df.to_sql("customers", conn, if_exists="replace", index=False)

# Confirm records saved
inter_count = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
cust_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

print(f"\n✅ Saved {inter_count} interaction records to 'interactions' table.")
print(f"✅ Saved {cust_count} customer records to 'customers' table.")

conn.close()
