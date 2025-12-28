# import requests
# from ..utils.hashing import compute_file_hash
# from ..utils.storage import store_pdf

# def ingest_pdf(source_name, pdf_url):
#     pdf_bytes = requests.get(pdf_url, timeout=15).content
#     file_hash = compute_file_hash(pdf_bytes)

#     store_pdf(
#         source=source_name,
#         url=pdf_url,
#         file_bytes=pdf_bytes,
#         file_hash=file_hash,
#         doc_type="policy_pdf"
#     )
import requests
import pdfplumber
import io

from ..utils.hashing import compute_hash
from ..utils.storage import store_article


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def ingest_pdf(source_name: str, pdf_url: str):
    """
    Download PDF, extract text, hash, store in DB
    """

    try:
        response = requests.get(pdf_url, timeout=15)
        if response.status_code != 200:
            print(f"[PDF ERROR] Cannot fetch {pdf_url}")
            return

        pdf_bytes = response.content
        text = extract_text_from_pdf(pdf_bytes)

        if not text or len(text) < 500:
            return

        content_hash = compute_hash(text)

        store_article(
            source=source_name,
            url=pdf_url,
            title="Policy / Report PDF",
            published="",
            content_hash=content_hash,
            doc_type="policy_pdf",
            raw_text=text
        )

    except Exception as e:
        print(f"[PDF INGEST ERROR] {source_name} | {e}")
