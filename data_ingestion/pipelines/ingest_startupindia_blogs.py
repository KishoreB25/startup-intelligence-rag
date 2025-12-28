import requests

from ..utils.hashing import compute_hash
from ..utils.storage import store_article


def ingest_startupindia_blogs(page=0):
    """
    Ingest blogs from Startup India official API
    """

    api_url = (
        "https://www.startupindia.gov.in/"
        "content/sih/en/api/blogs.json"
    )

    params = {
        "page": page,
        "size": 20
    }

    resp = requests.get(api_url, params=params, timeout=15)
    if resp.status_code != 200:
        print("[StartupIndia] Blog API failed")
        return

    data = resp.json()

    for blog in data.get("blogs", []):
        title = blog.get("title", "")
        content = blog.get("content", "")
        url = blog.get("path", "")

        if not content or len(content) < 300:
            continue

        content_hash = compute_hash(content)

        store_article(
            source="startup_india_blog",
            url="https://www.startupindia.gov.in" + url,
            title=title,
            published=blog.get("publishDate", ""),
            content_hash=content_hash,
            doc_type="gov_blog",
            raw_text=content
        )
