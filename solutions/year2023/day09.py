"""This file holds the solutions for Advent of Code 2023 day 9: Mirage Maintenance
https://adventofcode.com/2023/day/9
"""

import itertools

from solutions.common.strings import ints


def extrapolate(values: list[int], back: bool = False) -> int:
    if not any(values):  # same as: if all(v == 0 for v in values)
        return 0

    # go one deeper, so calculate the extrapolated value from the next level
    extrapolated = extrapolate([y - x for x, y in itertools.pairwise(values)], back=back)
    # if forwards,  return the last  value of the input list + the extrapolated value
    # if backwards, return the first value of the input list - the extrapolated value
    return (values[-1] + extrapolated) if not back else (values[0] - extrapolated)


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 9 part 1"""
    return sum(extrapolate(ints(line)) for line in lines)


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 9 part 2"""
    return sum(extrapolate(ints(line), back=True) for line in lines)
