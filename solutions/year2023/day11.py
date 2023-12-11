"""This file holds the solutions for Advent of Code 2023 day 11: Cosmic Expansion
https://adventofcode.com/2023/day/11
"""

import itertools

from solutions.common.iter import count


def _stars(universe: list[str], expansion_factor: int = 2) -> set[tuple[int, int]]:
    """Returns the star coordinates, adjusted for the expansion factor."""

    # Determine all empty rows and column numbers
    empty_rows = [r for r, row in enumerate(universe) if all(chr != "#" for chr in row)]
    empty_cols = [c for c, col in enumerate(zip(*universe)) if all(chr != "#" for chr in col)]

    return {
        (
            # Take the amount of columns before this column, and multiply that with
            # expansion_factor - 1 (because 1 is already in the data), add that to the coordinate
            x + count(itertools.takewhile(lambda c: c < x, empty_cols), expansion_factor - 1),
            # Same for y and its rows
            y + count(itertools.takewhile(lambda r: r < y, empty_rows), expansion_factor - 1),
        )
        for y, line in enumerate(universe)
        for x, star in enumerate(line)
        if star == "#"
    }


def part_1(lines: list[str], expansion_factor: int = 2) -> int:
    """Solution for Advent of Code 2023 day 11 part 1"""
    return sum(
        # Distance calculation: just the absolute differences between two points. Nothing
        # Pythagorean here.
        abs(star_1[0] - star_2[0]) + abs(star_1[1] - star_2[1])
        for star_1, star_2 in itertools.combinations(_stars(lines, expansion_factor), 2)
    )


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 11 part 2"""
    return part_1(lines, expansion_factor=1_000_000)
