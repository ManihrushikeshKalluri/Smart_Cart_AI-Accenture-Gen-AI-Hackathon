import sqlite3
from datetime import datetime

DB_NAME = "recommendation_logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            product_id TEXT,
            category TEXT,
            subcategory TEXT,
            recommended_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_recommendation(customer_id, product_id, category, subcategory):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO recommendations (customer_id, product_id, category, subcategory, recommended_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, product_id, category, subcategory, datetime.now()))
    conn.commit()
    conn.close()
