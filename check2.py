import sqlite3

conn = sqlite3.connect("data/metadata/urls.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM processed_urls WHERE source = 'founder_blog'")
conn.commit()

print("✅ All founder blog URLs deleted successfully")

conn.close()
