import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect("smart_shopping.db")

# Load existing customers table
customers_df = pd.read_sql("SELECT * FROM customers", conn)

# Print columns to confirm existing structure (for debugging)
print("Existing columns:", customers_df.columns.tolist())

# --- Add a new column with dummy preference data ---
# You can later replace this with dynamic logic based on past purchases

# Simple default preference (same for all for now)
customers_df["Preferred_Categories"] = ["Books, Home Decor"] * len(customers_df)

# Overwrite the table with the updated DataFrame
customers_df.to_sql("customers", conn, if_exists="replace", index=False)

# Done
print("✅ 'Preferred_Categories' column added to customers table.")
conn.close()
