import sqlite3

conn = sqlite3.connect(r"ingestion.db")
cursor = conn.cursor()

rows = cursor.execute(
    
    "SELECT source, doc_type, LENGTH(raw_text) FROM documents;"
    
).fetchall()

for r in rows:
    print(r)
#"SELECT source, title, url FROM documents LIMIT 10"



#"SELECT source, doc_type, title FROM documents  WHERE source LIKE 'startup_india%' LIMIT 10;"