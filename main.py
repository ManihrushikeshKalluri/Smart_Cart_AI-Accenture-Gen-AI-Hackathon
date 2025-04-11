import sqlite3
import pandas as pd
from agents.customer_agent import CustomerAgent
from agents.product_agent import ProductAgent
from agents.recommendation_agent import RecommendationAgent

# Connect to SQLite DB
conn = sqlite3.connect("smart_shopping.db")

# ✅ Use correct table names
interactions_df = pd.read_sql_query("SELECT * FROM interactions", conn)
customers_df = pd.read_sql_query("SELECT * FROM customers", conn)

# Pick a test customer
customer_id = "C1000"

# Get this customer's past interactions
customer_interactions = interactions_df[interactions_df["Product_ID"].notnull()]
customer_row = customers_df[customers_df["Customer_ID"] == customer_id].iloc[0]

# 🔍 Extract top 2 preferred categories
top_categories = customer_interactions["Category"].value_counts().head(2).index.tolist()
preferences = top_categories if top_categories else ["Electronics", "Books"]

# 🎯 Create CustomerAgent
customer = CustomerAgent(customer_id=customer_id, preferences=preferences)

# 🛍️ Create ProductAgents from interaction table (as product catalog)
product_agents = []
for _, row in interactions_df.iterrows():
    product = ProductAgent(
        product_id=row["Product_ID"],
        name=row["Subcategory"],  # Using Subcategory as product name
        category=row["Category"],
        rating=row["Product_Rating"]
    )
    product_agents.append(product)

# 🔮 Generate Recommendations
recommender = RecommendationAgent()
recommendations = recommender.recommend(customer, product_agents)

# 📢 Output Results
print(f"\n👤 Customer: {customer.customer_id}")
print(f"🎯 Preferences: {', '.join(customer.preferences)}")
print("📦 Recommended Products:")
for p in recommendations:
    print(f"🛒 {p.name} (ID: {p.product_id}) | Category: {p.category} | Rating: {p.rating}")
