import sqlite3
import feedparser
import requests
from bs4 import BeautifulSoup

DB_PATH = "data/metadata/processed_urls.db"

def url_exists(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM processed_urls WHERE url = ?", (url,))
    return cur.fetchone() is not None

def save_url(conn, url):
    cur = conn.cursor()
    cur.execute("INSERT INTO processed_urls (url) VALUES (?)", (url,))
    conn.commit()

def fetch_news():
    conn = sqlite3.connect(DB_PATH)
    feed = feedparser.parse("https://techcrunch.com/tag/startups/feed/")

    for entry in feed.entries:
        url = entry.link

        if url_exists(conn, url):
            print("Skipping existing:", url)
            continue

        # Fetch article
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        article_text = " ".join(p.text for p in soup.find_all("p"))

        # Save article text (for later processing)
        with open("data/raw/news/article.txt", "w", encoding="utf-8") as f:
            f.write(article_text)

        save_url(conn, url)
        print("Saved new article:", url)

    conn.close()
