# # import requests
# # from bs4 import BeautifulSoup
# # from ..utils.hashing import compute_hash
# # from ..utils.storage import store_article

# # def ingest_vc_blog(vc_name, base_url):
# #     resp = requests.get(base_url, timeout=10)
# #     soup = BeautifulSoup(resp.text, "html.parser")

# #     links = set(a["href"] for a in soup.find_all("a", href=True) if "blog" in a["href"])

# #     for link in links:
# #         if not link.startswith("http"):
# #             link = base_url.rstrip("/") + "/" + link.lstrip("/")

# #         article = requests.get(link, timeout=10)
# #         if article.status_code != 200:
# #             continue

# #         text = article.text
# #         content_hash = compute_hash(text)

# #         store_article(
# #             source=vc_name,
# #             url=link,
# #             title="VC Blog",
# #             published="",
# #             raw_text=text,
# #             content_hash=content_hash,
# #             doc_type="vc_blog"
# #         )
# import requests
# from bs4 import BeautifulSoup

# from ..utils.hashing import compute_hash
# from ..utils.text_cleaning import clean_html
# from ..utils.storage import store_signal
# from ..utils.signal_extractor import extract_signals


# def ingest_vc_blog(vc_name: str, base_url: str):
#     """
#     Ingest VC blog / insight pages:
#     - Fetch page
#     - Extract article links
#     - Clean HTML
#     - Store clean text
#     """

#     try:
#         response = requests.get(base_url, timeout=10)
#         if response.status_code != 200:
#             return

#         soup = BeautifulSoup(response.text, "html.parser")

#         links = set()
#         for a in soup.find_all("a", href=True):
#             href = a["href"]
#             if "blog" in href or "insight" in href:
#                 if href.startswith("/"):
#                     href = base_url.rstrip("/") + href
#                 if href.startswith("http"):
#                     links.add(href)

#         for link in links:
#             try:
#                 article = requests.get(link, timeout=10)
#                 if article.status_code != 200:
#                     continue

#                 clean_text = clean_html(article.text)

#                 if not clean_text or len(clean_text) < 300:
#                     continue

#                 content_hash = compute_hash(clean_text)

#                 store_article(
#                     source=vc_name,
#                     url=link,
#                     title="VC Insight",
#                     published="",
#                     content_hash=content_hash,
#                     doc_type="vc_blog",
#                     raw_text=clean_text
#                 )

#             except Exception as e:
#                 print(f"[VC BLOG ERROR] {vc_name} | {link} | {e}")

#     except Exception as e:
#         print(f"[VC SOURCE ERROR] {vc_name} | {e}")

import requests
from bs4 import BeautifulSoup

from ..utils.text_cleaning import clean_html
from ..utils.signal_extractor import extract_signals
from ..utils.storage import store_signal


def ingest_blog(source_name: str, blog_url: str):
    """
    Ingest VC / investor blogs and extract investment intent signals.
    """

    try:
        resp = requests.get(blog_url, timeout=10)
        if resp.status_code != 200:
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]

            if href.startswith("/"):
                href = blog_url.rstrip("/") + href

            if href.startswith("http") and "blog" in href:
                links.add(href)

        for link in links:
            try:
                article = requests.get(link, timeout=10)
                if article.status_code != 200:
                    continue

                clean_text = clean_html(article.text)
                if not clean_text or len(clean_text) < 300:
                    continue

                signals = extract_signals(clean_text, source_type="blog")

                record = {
                    "source_type": "blog",
                    "source_url": link,
                    "entity_type": "investor",
                    "published_date": "",
                    "last_updated": "",
                    "evidence_snippet": clean_text[:300],
                    **signals
                }

                store_signal(record)

            except Exception as e:
                print(f"[BLOG ARTICLE ERROR] {link} | {e}")

    except Exception as e:
        print(f"[BLOG SOURCE ERROR] {source_name} | {e}")
