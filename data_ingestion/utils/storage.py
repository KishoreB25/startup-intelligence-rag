import sqlite3

conn = sqlite3.connect("ingestion.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    url TEXT PRIMARY KEY,
    source TEXT,
    title TEXT,
    published TEXT,
    content_hash TEXT,
    doc_type TEXT,
    raw_text TEXT
)
""")

def store_article(**data):
    cursor.execute("""
    INSERT OR IGNORE INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["url"],
        data["source"],
        data["title"],
        data["published"],
        data["content_hash"],
        data["doc_type"],
        data["raw_text"]
    ))
    conn.commit()

def store_pdf(source, url, file_bytes, file_hash, doc_type):
    cursor.execute("""
    INSERT OR IGNORE INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        url,
        source,
        "PDF Document",
        "",
        file_hash,
        doc_type,
        file_bytes.decode("latin1", errors="ignore")
    ))
    conn.commit()
