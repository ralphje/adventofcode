"""This file holds the solutions for Advent of Code 2023 day 14: Parabolic Reflector Dish
https://adventofcode.com/2023/day/14
"""

import functools
import itertools
import math
from collections.abc import Sequence, Iterable


@functools.cache
def _tilt_row(input: str | Sequence[str]) -> str:
    """Resolve the row, shifting everything as far left in the list as possible."""

    empty = 0
    # Make the row editable
    row = list(input)
    for i, char in enumerate(row):
        if char == "O":
            # We know that this may roll to the empty row now
            row[i], row[empty] = ".", "O"
            empty += 1
        elif char == "#":
            # Stuck block, so the next empty spot is next to it
            empty = i + 1
    # Return a str again
    return "".join(row)


def _tilt_grid(rows: Iterable[str | Sequence[str]]) -> tuple[str, ...]:
    return tuple(_tilt_row(row) for row in rows)


def _rotate_grid(grid: Sequence[str], clockwise: bool = True) -> tuple[Sequence[str], ...]:
    return tuple(zip(*grid[::-1])) if clockwise else tuple(zip(*grid))[::-1]


def _weigh_grid(rows: Iterable[str | Sequence[str]]) -> int:
    """Weighs each row, with index 0 counting the heaviest, and sums it."""
    return sum(
        math.sumprod(  # type: ignore[misc]
            (c == "O" for c in row),
            range(len(row), 0, -1),
        )
        for row in rows
    )


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 14 part 1"""
    # We assume north is left, so we turn one time anti-clockwise to ensure that we have that
    return _weigh_grid(_tilt_grid(_rotate_grid(lines, clockwise=False)))


def part_2(lines: list[str], total_cycles: int = 1_000_000_000) -> int:
    """Solution for Advent of Code 2023 day 14 part 2"""

    # We assume north is left, so we turn one time anti-clockwise to ensure that we have that
    grid = _rotate_grid(lines, clockwise=False)

    # Cycle through all grids and see when we encounter a known one
    known_grids, cycle_end = {}, 0
    for cycle_end in itertools.count():
        if grid in known_grids:
            break
        known_grids[grid] = cycle_end

        # Perform four grid cycles, one in each direction.
        for _ in range(4):
            grid = _rotate_grid(_tilt_grid(grid))

    # Calculate when we will have the total_cycles reached, and return the known_grid
    # from our cache.
    return _weigh_grid(
        next(
            k
            for k, v in known_grids.items()
            if (
                # known_grids[grid] is the start of the cycle
                known_grids[grid]
                # plus the total amount we need to do within the cycle
                # - the amount of cycles we still need to do
                + (total_cycles - cycle_end)
                # - modulus the size of the cycle
                % (cycle_end - known_grids[grid])
            )
            == v
        )
    )
