from collections.abc import Iterable
from typing import Any


def count(i: Iterable[Any]) -> int:
    """Counts the amount of items in the provided iterable. Less efficient than ``len``, possibly
    stupid if you need the result of the iteration as well.
    """
    return sum(1 for _ in i)
