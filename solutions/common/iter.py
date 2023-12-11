from collections.abc import Iterable
from typing import Any


def count(i: Iterable[Any], value: int = 1) -> int:
    """Counts the amount of items in the provided iterable. Less efficient than ``len``, possibly
    stupid if you need the result of the iteration as well.
    """
    return sum(value for _ in i)
