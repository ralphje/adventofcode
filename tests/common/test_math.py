import math

import pytest

from solutions.common.math import (
    chinese_remainder,
    chinese_remainder_generic,
    extended_gcd,
    factors,
    prime_factors,
    quadratic_formula,
)


@pytest.mark.parametrize(
    ("a", "b", "c"),
    [
        (1, 50, 50),
        (50, 100, 50),
        (50, 50, 0),
        (50, 50, 1),
    ],
)
def test_quadratic_formula(a, b, c):
    result = quadratic_formula(a, b, c)
    for x in result:
        assert a * x**2 + b * x + c == pytest.approx(0)


@pytest.mark.parametrize("n", [1, 2, 3, 16, 100, 5000, 47])
def test_prime_factors(n):
    assert math.prod(prime_factors(n)) == n
    for factor in prime_factors(n):
        assert len(list(prime_factors(factor))) == 1


@pytest.mark.parametrize("n", [1, 2, 3, 16, 100, 5000, 47])
def test_factors(n):
    assert math.prod(factors(n)) == n


@pytest.mark.parametrize(
    ("a", "b", "c"),
    [
        (0, 50, 50),
        (50, 50, 50),
    ],
)
def test_quadratic_formula_error(a, b, c):
    with pytest.raises((ZeroDivisionError, ValueError)):
        quadratic_formula(a, b, c)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (1, 1),
        (12, 8),
        (23894798501898, 23948178468116),
        (pow(2, 50), pow(3, 50)),
        (1398, 324),
        (161, 28),
    ],
)
def test_extended_gcd(a, b):
    result = extended_gcd(a, b)
    assert result[0] == math.gcd(a, b)
    assert a * result[1] + b * result[2] == result[0]

    result = extended_gcd(b, a)
    assert result[0] == math.gcd(b, a)
    assert a * result[2] + b * result[1] == result[0]


@pytest.mark.parametrize(
    ("n", "a"),
    [
        ([3, 4, 5], [0, 3, 4]),
        ([5, 7, 11], [2, 3, 10]),
        ([7, 5, 12], [3, 3, 4]),
        ([2, 3], [0, 0]),
    ],
)
def test_chinese_remainder(n, a):
    result = chinese_remainder(n, a)
    for n_i, a_i in zip(n, a):
        assert a_i % n_i == result % n_i


@pytest.mark.parametrize(
    ("n", "a"),
    [
        ([4, 6], [3, 0]),
    ],
)
def test_chinese_remainder_error(n, a):
    with pytest.raises(ValueError):  # noqa
        chinese_remainder(n, a)


@pytest.mark.parametrize(
    ("n", "a"),
    [
        ([2, 3, 4, 5, 6], [1, 1, 1, 1, 1]),
        ([24, 64], [10, 18]),
    ],
)
def test_chinese_remainder_generic(n, a):
    result = chinese_remainder_generic(n, a)
    for n_i, a_i in zip(n, a):
        assert a_i % n_i == result % n_i


@pytest.mark.parametrize(
    ("n", "a"),
    [
        ([2, 2], [1, 2]),
        ([2, 4], [1, 2]),
        ([3, 12], [1, 3]),
    ],
)
def test_chinese_remainder_generic_error(n, a):
    with pytest.raises(ValueError):  # noqa
        chinese_remainder_generic(n, a)
