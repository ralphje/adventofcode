"""This file holds the solutions for Advent of Code 2023 day 18: Lavaduct Lagoon
https://adventofcode.com/2023/day/18
"""

import itertools
import re
from collections.abc import Iterable, Iterator

from solutions.common.grid import distance


def shoelace_and_picks(points: Iterable[complex]) -> float:
    """This is a combination of the Shoelace formula and Pick's theorem.

    1. The Shoelace formula calculates the area inside a polygon, given the points of the polygon
       with 2A = |x₁y₂ - x₂y₁ + ... + xᵢy₁ - x₁yᵢ|.
    2. Pick's theorem states that the area of a polygon is A = i + b/2 - 1, where i is the number
       of integer points in that polygon, and b the number of integer points on its boundary.

    Now, we could simply use the Shoelace formula end be done with that, but we wouldn't be taking
    the entire border into account. That's why we are also using Pick's theorem. We can simply
    assume that the Shoelace formula counts the amount of inner points within the polygon.

    We want to know the inner area (i) plus the border (b), i.e.

            A = i + b/2 - 1
            i = A - b/2 + 1
        b + i = A - b/2 + 1 + b
        b + i = A + b/2 + 1

    Since we actually calculate 2A using the Shoelace formula (S), we can simplify to:

        b + i = S/2 + b/2 + 1
        b + i = (S + b)/2 + 1

    We can further simplify in code as shown below, as we are going around in the right direction.
    """

    return (
        sum(
            pair[0].real * pair[1].imag - pair[0].imag * pair[1].real + distance(*pair)
            for pair in itertools.pairwise(itertools.chain(points))
        )
        // 2
        + 1
    )


DIG_RE = re.compile(r"([RDLU]) (\d+) \(#([0-9a-f]{6})\)")
DIRECTIONS = {"R": 1, "L": -1, "U": -1j, "D": +1j}


def _iter_coordinates_part_1(lines: list[str]) -> Iterator[complex]:
    """Iterate coordinates based on part 1 rules."""
    location = 0j
    yield location
    for line in lines:
        direction, distance, _ = DIG_RE.findall(line)[0]
        location += DIRECTIONS[direction] * int(distance)
        yield location


def part_1(lines: list[str]) -> float:
    """Solution for Advent of Code 2023 day 18 part 1"""
    return shoelace_and_picks(_iter_coordinates_part_1(lines))


PART_2_DIRECTIONS = str.maketrans("0123", "RDLU")


def _iter_coordinates_part_2(lines: list[str]) -> Iterator[complex]:
    """Iterate coordinates based on part 2 rules."""
    location = 0j
    yield location
    for line in lines:
        _, _, color = DIG_RE.findall(line)[0]
        location += DIRECTIONS[color[5].translate(PART_2_DIRECTIONS)] * int(color[:5], 16)
        yield location


def part_2(lines: list[str]) -> float:
    """Solution for Advent of Code 2023 day 18 part 2"""
    return shoelace_and_picks(_iter_coordinates_part_2(lines))
