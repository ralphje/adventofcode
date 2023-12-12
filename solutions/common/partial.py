from collections.abc import Callable
from typing import Any


def lt(a: Any) -> Callable[[Any], bool]:
    """Partial method. E.g. lt(3)(2) == True"""
    return lambda b: b < a


def lte(a: Any) -> Callable[[Any], bool]:
    """Partial method. E.g. lte(3)(2) == True"""
    return lambda b: b <= a


def gt(a: Any) -> Callable[[Any], bool]:
    """Partial method. E.g. gt(2)(3) == True"""
    return lambda b: b > a


def gte(a: Any) -> Callable[[Any], bool]:
    """Partial method. E.g. gte(2)(3) == True"""
    return lambda b: b >= a


def eq(a: Any) -> Callable[[Any], bool]:
    """Partial method. E.g. eq(2)(2) == True"""
    return lambda b: b == a


def neq(a: Any) -> Callable[[Any], bool]:
    """Partial method. E.g. neq(2)(3) == True"""
    return lambda b: b != a
