import math
from collections.abc import Iterable


def quadratic_formula(a: int, b: int, c: int) -> tuple[float, float]:
    """Apply the quadratic formula, and return the solutions for x, if ``0 = ax² + bx + c``

    Solutions are defined as::

        x = (-b ± √(b² - 4ac)) / 2a
    """
    return (
        (-b - (sqrt := math.sqrt(b**2 - 4 * a * c))) / (2 * a),
        (-b + sqrt) / (2 * a),
    )


def prime_factors(n: int) -> Iterable[int]:
    """Given a number n, will yield all ints that are prime factors of the number. The same number
    may repeat. The output is sorted.
    """

    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            yield i
    if n > 1:
        yield n


def factors(n: int) -> Iterable[int]:
    """Given a number n, will yield all ints that are factors of the number. The numbers will
    not repeat, i.e. the same primes are all combined into one factor. The output is not sorted.
    """

    prev_factor, prod = None, 1
    for factor in prime_factors(n):
        if prev_factor == factor:
            prod *= factor
            continue
        if prev_factor is not None:
            yield prod
        prev_factor = prod = factor
    yield prod


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Given two integers ``a`` and ``b``, returns ``gcd(a, b), x, y`` such that
    ``a*x + b*y == gcd(a, b)``.

    If you only need the ``gcd(a, b)``, use ``math.gcd(a, b)``.

    If you need the modular multiplicative inverse of ``a`` modulo ``m`` such that
    ``a*x ≡ 1 (mod m)``, use ``pow(a, -1, m)``
    """

    if not b:
        return a, 1, 0
    q, r = divmod(a, b)
    gcd, s, t = extended_gcd(b, r)
    return gcd, t, s - q * t


def chinese_remainder(n: list[int] | tuple[int], a: list[int] | tuple[int]) -> int:
    """Given two lists of integers, ``nᵢ`` and ``aᵢ``, return ``x`` such that for each ``i``
    ``x ≡ aᵢ (mod nᵢ)``, where ``nᵢ`` is required to be coprime
    """
    n_prod = math.prod(n)
    return (
        sum(a_i * (p := n_prod // n_i) * pow(p, -1, n_i) for n_i, a_i in zip(n, a)) % n_prod
    ) or n_prod  # return n_prod when result would be 0


def _coprime_congruences(
    n: list[int] | tuple[int], a: list[int] | tuple[int]
) -> tuple[tuple[int], tuple[int]]:
    """Given two lists of integers, ``nᵢ`` and ``aᵢ``, return two new lists of integers, that are
    congruent in the Chinese Remainder Theorem, and are co-prime. Any ``nᵢ`` is separated into its
    factors, and any remaining ``nᵢ`` that is a factor of any other ``nⱼ``, is discarded.

    So, [2, 3, 4, 5, 6] will result in [3, 4, 5], as 2 is a factor of 4, and 6 is 2x3.

    See https://math.stackexchange.com/questions/120070/
    and https://math.stackexchange.com/questions/1095442/
    """

    new = set()
    # Transform all elements in their own factors
    for n_i, a_i in zip(n, a):
        for factor in factors(n_i):
            new.add((factor, a_i))

    # Remove duplicate factors, keep only the highest.
    for f, _ in sorted(new, reverse=True):
        for n_i, a_i in list(new):
            if f % n_i == 0 and f != n_i:
                new.discard((n_i, a_i))

    return tuple(zip(*new))


def chinese_remainder_generic(n: list[int] | tuple[int], a: list[int] | tuple[int]) -> int:
    """Given two lists of integers, ``nᵢ`` and ``aᵢ``, return ``x`` such that for each ``i``
    ``x ≡ aᵢ (mod nᵢ)``, where ``nᵢ`` is not required to be coprime. This does not check whether
    any solution exists or is valid.
    """

    return chinese_remainder(*_coprime_congruences(n, a))
