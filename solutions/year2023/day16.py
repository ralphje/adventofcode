"""This file holds the solutions for Advent of Code 2023 day 16: The Floor Will Be Lava
https://adventofcode.com/2023/day/16
"""

from collections.abc import Iterator

type Direction = tuple[int, int]
type Coordinate = tuple[int, int]


# directions (x, y)
N = (0, -1)
S = (0, +1)
E = (+1, 0)
W = (-1, 0)

# mapping of encountered mirror, and the direction we encounter it in, to the direction we will
# travel to after the encountered mirror
MIRRORS: dict[str, dict[Direction, tuple[Direction]]] = {
    # continue through in same direction when . is encountered
    ".": {N: (N,), S: (S,), E: (E,), W: (W,)},
    # continue through in same direction for N/S, split to N and S when E/W
    "|": {N: (N,), S: (S,), E: (N, S), W: (N, S)},
    # continue through in same direction for E/W, split to E and W when N/S
    "-": {N: (E, W), S: (E, W), E: (E,), W: (W,)},
    # mirror N/E and S/W
    "/": {N: (E,), S: (W,), E: (N,), W: (S,)},
    # mirror N/W and S/E
    "\\": {N: (W,), S: (E,), E: (S,), W: (N,)},
}


def part_1(grid: list[str], start: tuple[Coordinate, Direction] = ((0, 0), E)) -> int:
    """Solution for Advent of Code 2023 day 16 part 1"""
    max_x, max_y = len(grid[0]), len(grid)

    # Keep track of the steps that we still need to check, and the steps we've visited
    steps: list[tuple[Coordinate, Direction]] = [start]
    visited: set[tuple[Coordinate, Direction]] = set()

    while steps and (step := steps.pop(0)):
        # Ignore anything we've visited before
        if step in visited:
            continue
        visited.add(step)

        coordinate, direction = step
        # The contraption in 'in' simply gets the correct item from the grid, and then from the
        # MIRRORS dict
        for next_direction in MIRRORS[grid[coordinate[1]][coordinate[0]]][direction]:
            next_x, next_y = (
                coordinate[0] + next_direction[0],
                coordinate[1] + next_direction[1],
            )
            # Some bounds checking
            if not (0 <= next_x < max_x and 0 <= next_y < max_y):
                continue

            # Add next steps to check
            steps.append(((next_x, next_y), next_direction))

    # Make a set of all visited coordinates, and count them
    return len({coordinate for coordinate, _ in visited})


def _iter_steps(grid: list[str]) -> Iterator[tuple[Coordinate, Direction]]:
    """Creates an iterator of all border steps. This simplifies part_2's iterator a lot."""
    max_x, max_y = len(grid[0]), len(grid)
    for y in range(0, max_y):
        yield (0, y), E
        yield (max_x - 1, y), W
    for x in range(0, max_x):
        yield (x, 0), S
        yield (x, max_y - 1), N


def part_2(grid: list[str]) -> int:
    """Solution for Advent of Code 2023 day 16 part 2"""
    return max(part_1(grid, step) for step in _iter_steps(grid))
