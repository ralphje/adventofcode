import re

_ALL_INTS_RE = re.compile(r"-?\d+")


def ints(s: str) -> list[int]:
    """Return all integers in provided string, e.g. ``"a 3 -1" -> [3, -1]``"""
    return [int(v) for v in _ALL_INTS_RE.findall(s)]
