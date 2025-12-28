import feedparser
import requests
from ..utils.hashing import compute_hash
from ..utils.storage import store_article

def ingest_rss_feed(source_name, feed_url):
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        url = entry.link
        title = entry.title
        published = entry.get("published", "")

        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            continue

        text = response.text
        content_hash = compute_hash(text)

        store_article(
            source=source_name,
            url=url,
            title=title,
            published=published,
            raw_text=text,
            content_hash=content_hash,
            doc_type="funding_news"
        )

# url = entry.link

# response = requests.get(url)
# raw_html = response.text

# from ..utils.text_cleaning import clean_html

# raw_html = response.text
# clean_text = clean_html(raw_html)

# content_hash = compute_hash(clean_text)

# store_article(
#     source=source_name,
#     url=url,
#     title=title,
#     published=published,
#     content_hash=content_hash,
#     doc_type="funding_news",
#     raw_text=clean_text
# )


import feedparser
import requests

from ..utils.hashing import compute_hash
from ..utils.text_cleaning import clean_html
from ..utils.storage import store_article


def ingest_rss_feed(source_name: str, feed_url: str):
    """
    Ingest articles from an RSS feed:
    - Fetch article URLs
    - Download HTML
    - Clean text
    - Hash cleaned content
    - Store in database
    """

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        try:
            url = entry.get("link")
            title = entry.get("title", "")
            published = entry.get("published", "")

            if not url:
                continue

            # Fetch article HTML
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            raw_html = response.text

            # Clean HTML → plain text
            clean_text = clean_html(raw_html)

            # Skip very small / empty content
            if not clean_text or len(clean_text) < 300:
                continue

            # Hash cleaned content (NOT raw HTML)
            content_hash = compute_hash(clean_text)

            # Store cleaned article
            store_article(
                source=source_name,
                url=url,
                title=title,
                published=published,
                content_hash=content_hash,
                doc_type="funding_news",
                raw_text=clean_text
            )

        except Exception as e:
            # Never crash ingestion for one bad article
            print(f"[RSS ERROR] {source_name} | {url} | {e}")

