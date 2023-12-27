"""This file holds the solutions for Advent of Code 2023 day 23: A Long Walk
https://adventofcode.com/2023/day/23
"""

from collections.abc import Iterator

from solutions.common.grid import Grid

# Mapping of possible single steps and the acceptable characters at that location
POSSIBLE_STEPS = {
    ".": (-1, +1, -1j, +1j),
    "<": (-1,),
    ">": (+1,),
    "^": (-1j,),
    "v": (+1j,),
}


def walk(
    grid: Grid[str],
    start: complex,
    ends: list[complex],
    prefix: tuple[complex, ...] = (),
) -> Iterator[tuple[complex, ...]]:
    """Walk on the grid, from start to a possible list of ends, and return the path. Does not
    accept the trivial path. Will yield the start and end points of the path, so the path cost is
    length - 1.
    """
    if start in ends and prefix:
        yield *prefix, start
    else:
        # Iterate in each possible direction
        for direction in POSSIBLE_STEPS[grid.get(start)]:
            next_step = start + direction
            # Check if the next_step is already visited, not in the grid, or a #.
            if next_step not in grid or grid.get(next_step) == "#" or next_step in prefix:
                continue
            yield from walk(grid, next_step, ends, (*prefix, start))


def calculate_graph(grid: Grid[str]) -> dict[complex, dict[complex, int]]:
    """Calculate the graph of all junctions to all junctions."""
    # Find all possible junctions, including the start and end nodes.
    junctions = [
        next(grid.find(".")),  # start node
        *(
            # All coordinates
            coordinate
            for coordinate in grid.coordinates
            # Where the coordinate is not #, and there are more than 2 orthogonal neighbours that
            # are also not #.
            if (
                grid.get(coordinate) != "#"
                and sum(int(grid.get(d) != "#") for d in grid.orthogonal(coordinate)) > 2
            )
        ),
        next(grid.rfind(".")),  # end node
    ]

    # Find all path lengths to each junction.
    return {
        junction: {j[-1]: len(j) - 1 for j in walk(grid, junction, junctions)}
        for junction in junctions
    }


def path_cost(
    junctions: dict[complex, dict[complex, int]],
    start: complex,
    end: complex,
    path: tuple[complex, ...] = (),
) -> Iterator[int]:
    """Iterate over the path costs of possible paths to take."""

    if start == end:
        # Base case: cost = 0
        yield 0
    else:
        for next_step, cost in junctions[start].items():
            # Ignore steps we've already taken, we can't go back
            if next_step not in path:
                # Recurse, adding the cost of this step to the total cost
                yield from (
                    s + cost
                    # Add the current start to the full path
                    for s in path_cost(junctions, next_step, end, (*path, start))
                )


def part_1(grid: Grid[str]) -> int:
    """Solution for Advent of Code 2023 day 23 part 1"""
    # Calculate the graph
    graph = calculate_graph(grid)

    # Get the start and end nodes from the graph
    start, *_, end = graph

    return max(path_cost(graph, start, end))


def part_2(challenge: str) -> int:
    """Solution for Advent of Code 2023 day 23 part 2"""
    return part_1(Grid(challenge.translate(str.maketrans("<>^v", "....")).splitlines()))
