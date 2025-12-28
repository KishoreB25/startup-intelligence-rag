import hashlib

def compute_hash(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def compute_file_hash(data: bytes):
    return hashlib.sha256(data).hexdigest()
