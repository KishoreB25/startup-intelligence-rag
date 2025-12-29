# import sqlite3

# conn = sqlite3.connect("ingestion.db")
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS documents (
#     url TEXT PRIMARY KEY,
#     source TEXT,
#     title TEXT,
#     published TEXT,
#     content_hash TEXT,
#     doc_type TEXT,
#     raw_text TEXT
# )
# """)

# def store_article(**data):
#     cursor.execute("""
#     INSERT OR IGNORE INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (
#         data["url"],
#         data["source"],
#         data["title"],
#         data["published"],
#         data["content_hash"],
#         data["doc_type"],
#         data["raw_text"]
#     ))
#     conn.commit()

# def store_pdf(source, url, file_bytes, file_hash, doc_type):
#     cursor.execute("""
#     INSERT OR IGNORE INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (
#         url,
#         source,
#         "PDF Document",
#         "",
#         file_hash,
#         doc_type,
#         file_bytes.decode("latin1", errors="ignore")
#     ))
#     conn.commit()

# def store_signal(
#     source_type,
#     source_url,
#     entity_type,
#     published_date,
#     extracted_signals,
#     last_updated
# ):
#     """
#     Stores ONLY structured metadata (not full text)
#     """
#     record = {
#         "source_type": source_type,
#         "source_url": source_url,
#         "entity_type": entity_type,
#         "published_date": published_date,
#         "last_updated": last_updated,
#         **extracted_signals
#     }

#     # Store in SQLite / JSON / Vector DB metadata
#     save_to_db(record)


import sqlite3
import json
from datetime import datetime

DB_PATH = "data/ingestion.db"


def store_signal(record: dict):
    """
    Stores a structured intelligence record.
    """

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""

        CREATE TABLE IF NOT EXISTS intelligence_records (
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

                """)

    cur.execute("""
        INSERT INTO intelligence_records (
            source_type,
            source_url,
            entity_type,
            published_date,
            last_updated,
            startup_name,
            investor_name,
            funding_stage,
            preferred_stage,
            sector_focus,
            market_focus,
            location_startup,
            location_investor,
            location_vc,
            confidence_score,
            evidence_snippet
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["source_type"],
        record["source_url"],
        record["entity_type"],
        record["published_date"],
        record["last_updated"],
        record.get("startup_name"),
        record.get("investor_name"),
        record.get("funding_stage"),
        record.get("preferred_stage"),
        json.dumps(record.get("sector_focus", [])),
        json.dumps(record.get("market_focus", [])),
        record.get("location_startup"),
        record.get("location_investor"),
        record.get("location_vc"),
        record.get("confidence_score", 0.5),
        record.get("evidence_snippet", "")
    ))

    conn.commit()
    conn.close()
