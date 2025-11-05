import hashlib

def hash_text(text: str) -> str:
    """
    Calcula el hash SHA-256 de un texto dado.
    """
    sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return sha256_hash