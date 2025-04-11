import pandas as pd

# Load your main product interaction data
df = pd.read_csv("product_recommendation_data.csv")

# Check if required columns exist
if 'Customer_ID' not in df.columns or 'Category' not in df.columns:
    raise ValueError("The dataset must contain 'Customer_ID' and 'Category' columns.")

# Group by Customer_ID and aggregate their preferred categories
customer_prefs = df.groupby('Customer_ID')['Category'].apply(
    lambda cats: ','.join(cats.dropna().unique())
).reset_index()

# Rename column to match the expected format
customer_prefs.columns = ['Customer_ID', 'Preferred_Categories']

# Save to CSV
customer_prefs.to_csv("customers.csv", index=False)

print("✅ customers.csv generated successfully!")
