import sqlite3
import os
os.makedirs("data/metadata", exist_ok=True)
conn = sqlite3.connect("data/metadata/urls.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS processed_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("Database initialized successfully.")

