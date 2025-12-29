import sqlite3

conn = sqlite3.connect(r"ingestion.db")
cursor = conn.cursor()

rows = cursor.execute(
    
    
    """CREATE TABLE IF NOT EXISTS intelligence_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT,
    source_url TEXT,
    entity_type TEXT,
    published_date TEXT,
    last_updated TEXT,
    startup_name TEXT,
    investor_name TEXT,
    funding_stage TEXT,
    preferred_stage TEXT,
    sector_focus TEXT,
    market_focus TEXT,
    location_startup TEXT,
    location_investor TEXT,
    location_vc TEXT,
    confidence_score REAL,
    evidence_snippet TEXT
);
"""
    
).fetchall()

for r in rows:
    print(r)
#"SELECT source, title, url FROM documents LIMIT 10"
#"SELECT source, doc_type, LENGTH(raw_text) FROM documents;"


#"SELECT source, doc_type, title FROM documents  WHERE source LIKE 'startup_india%' LIMIT 10;"