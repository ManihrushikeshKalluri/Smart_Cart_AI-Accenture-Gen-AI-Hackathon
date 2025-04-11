import sqlite3

conn = sqlite3.connect("smart_shopping.db")
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM interactions")
count = c.fetchone()[0]

print(f"📦 Total records in 'interactions': {count}")
conn.close()
