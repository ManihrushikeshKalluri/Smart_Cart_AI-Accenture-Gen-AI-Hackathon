import sqlite3
import pandas as pd

def get_top_product_categories():

    conn = sqlite3.connect("smart_shopping.db")
    c = conn.cursor()
    
    print("✅ Connected to DB!")  # Debug print
    
    c.execute('''
        SELECT Category, COUNT(*) as count
        FROM interactions
        GROUP BY Category
        ORDER BY count DESC
        LIMIT 5
    ''')
    
    top_categories = c.fetchall()
    conn.close()
    
    print(f"🔍 Found {len(top_categories)} categories")  # Debug print
    return top_categories
