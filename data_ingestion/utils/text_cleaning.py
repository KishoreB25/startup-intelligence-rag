# from bs4 import BeautifulSoup

# def clean_html(html: str) -> str:
#     soup = BeautifulSoup(html, "html.parser")

#     # remove scripts & styles
#     for tag in soup(["script", "style", "noscript"]):
#         tag.decompose()

#     text = soup.get_text(separator=" ")
#     return " ".join(text.split())

from bs4 import BeautifulSoup
import re

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # 1. Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    # 2. Get text
    text = soup.get_text(separator=" ")

    # 3. Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()
