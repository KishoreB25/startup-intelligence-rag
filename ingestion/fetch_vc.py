import os
import requests
import sqlite3
import hashlib
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urljoin

# ---------------- CONFIG ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw", "vc_thesis")
DB_PATH = os.path.join(DATA_DIR, "metadata", "vc_thesis.db")

BASE_URL = "https://www.peakxv.com/insights/"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS thesis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            content_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def is_seen(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM thesis WHERE url=?", (url,))
    return cur.fetchone() is not None


def save_entry(conn, url, content_hash):
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO thesis (url, content_hash) VALUES (?, ?)",
        (url, content_hash),
    )
    conn.commit()


# ---------------- SCRAPING ---------------- #

def get_article_links():
    print("🔍 Fetching article links...")
    res = requests.get(BASE_URL, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/insights/" in href:
            full_url = urljoin(BASE_URL, href)
            links.add(full_url)

    return list(links)


def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text.strip()


def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------- MAIN PIPELINE ---------------- #

def run():
    init_db()
    conn = sqlite3.connect(DB_PATH)

    article_links = get_article_links()
    print(f"🧠 Found {len(article_links)} potential articles")

    for url in article_links:
        if is_seen(conn, url):
            continue

        try:
            text = extract_article_text(url)

           

            content_hash = hash_text(text)

            filename = url.replace("https://", "").replace("/", "_") + ".txt"
            with open(os.path.join(RAW_DIR, filename), "w", encoding="utf-8") as f:
                f.write(text)

            save_entry(conn, url, content_hash)
            print(f"✅ Stored: {url}")

        except Exception as e:
            print(f"⚠️ Failed: {url} | {e}")

    conn.close()


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    run()


