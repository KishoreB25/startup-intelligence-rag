import os
import json
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


# -------- CONFIG --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw", "news")
DATA_DIR = os.path.join(DATA_DIR, "processed")
CHROMA_DIR = "chroma_db"
EMBED_MODEL = "llama3"

# ------------------------

def load_documents():
    documents = []

    for file in os.listdir(DATA_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(DATA_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Combine summary + evidence for embedding
        content = (
            f"Summary: {data.get('state_summary','')}\n\n"
            f"Evidence:\n" + "\n".join(data.get("evidence", []))
        )

        metadata = {
            "source_file": file,
            "startup_name": data.get("metadata", {}).get("startup_name", ""),
            "investor_name": data.get("metadata", {}).get("investor_name", ""),
            "funding_stage": data.get("metadata", {}).get("funding_stage", ""),
        }

        documents.append(
            Document(page_content=content, metadata=metadata)
        )

    return documents


def build_chroma():
    docs = load_documents()
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vectordb.persist()
    print(f"✅ Stored {len(docs)} documents in ChromaDB")
    return vectordb


if __name__ == "__main__":
    vectordb=build_chroma()
