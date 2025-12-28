import sqlite3

conn = sqlite3.connect("data/metadata/urls.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM processed_urls")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
