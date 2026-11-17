"""Text helpers for URLs and listings."""

import re


def slugify(text: str, max_len: int = 40) -> str:
    """Turn a product name into a URL slug.

    - Lower-case. Accented Latin letters become their base letter
      ('Crème Brûlée' -> 'creme-brulee').
    - Every run of characters other than a-z and 0-9 becomes one '-'.
    - No leading or trailing '-'.
    - At most `max_len` characters, cut after the other steps; a cut never
      leaves a trailing '-'.
    - If nothing is left, the slug is 'n-a'.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = slug[:max_len].rstrip("-")
    return slug or "n-a"


def truncate(text: str, max_len: int) -> str:
    """Shorten `text` to at most `max_len` characters, ending in '...' if cut."""
    if max_len < 3:
        raise ValueError("max_len must be at least 3")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."
