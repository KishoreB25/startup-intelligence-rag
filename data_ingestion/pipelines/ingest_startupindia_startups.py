import requests

from ..utils.hashing import compute_hash
from ..utils.storage import store_article


def ingest_startupindia_startups(page=0):
    """
    Ingest startup profiles from Startup India official API
    """

    api_url = (
        "https://www.startupindia.gov.in/"
        "content/sih/en/api/search/startups.json"
    )

    params = {
        "roles": "Startup",
        "page": page,
        "size": 20
    }

    resp = requests.get(api_url, params=params, timeout=15)
    if resp.status_code != 200:
        print("[StartupIndia] Startup search API failed")
        return

    data = resp.json()

    for startup in data.get("content", []):
        name = startup.get("entityName", "")
        sector = startup.get("sector", "")
        location = startup.get("location", "")

        text_blob = f"""
        Startup Name: {name}
        Sector: {sector}
        Location: {location}
        DPIIT Recognized: Yes
        """

        content_hash = compute_hash(text_blob)

        store_article(
            source="startup_india_registry",
            url="startupindia:" + name,
            title=name,
            published="",
            content_hash=content_hash,
            doc_type="gov_startup_profile",
            raw_text=text_blob
        )
