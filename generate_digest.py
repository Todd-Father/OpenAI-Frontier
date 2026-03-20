import hashlib


def generate_digest(data):
    """Generates SHA-256 digest for the given data."""
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()