import re
import unicodedata


def normalize_slug(text: str) -> str:
    """Return a filesystem friendly slug for ``text``."""
    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    cleaned = re.sub(r'[^A-Za-z0-9\s-]', '', ascii_text)
    underscored = re.sub(r'[\s-]+', '_', cleaned).strip('_')
    return underscored.lower()
