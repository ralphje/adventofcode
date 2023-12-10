import re

_ALL_INTS_RE = re.compile(r"-?\d+")


def ints(s: str) -> list[int]:
    """Return all integers in provided string, e.g. ``"a 3 -1" -> [3, -1]``"""
    return [int(v) for v in _ALL_INTS_RE.findall(s)]


def offset_replace(s: str, offset: int, new: str) -> str:
    """Replaces a string at a certain offset in another string."""
    return s[:offset] + new + s[offset + len(new) :]
