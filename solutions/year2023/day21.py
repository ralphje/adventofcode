"""This file holds the solutions for Advent of Code 2023 day 21: Step Counter
https://adventofcode.com/2023/day/21
"""

import collections

from solutions.common.grid import Grid, RepeatingGrid


def _count_locations(grid: Grid[str], start: complex, steps: int) -> int:
    """Count the locations reachable in the number of steps from the start location on the grid."""

    # Keep track of anything we've visited
    visited = set()
    # Anything we still need to visit
    queue = collections.deque([(start, 0)])
    # The result.
    result = 0
    while queue:
        location, distance = queue.popleft()
        # Do not visit the same node multiple times
        if location in visited:
            continue
        visited.add(location)
        # We only count the amount of steps with same parity, so if we know we have 10 steps
        # we only count those that are reachable in 2, 4, 6, 8 or 10 steps. This optimizes for
        # backtracking.
        result += int(distance % 2 == steps % 2)
        # If we've still got some to go, we continue in all orthogonal directions.
        if distance < steps:
            queue.extend((c, distance + 1) for c in grid.orthogonal(location) if grid.get(c) != "#")
    return result


def part_1(grid: Grid[str], steps: int = 64) -> int:
    """Solution for Advent of Code 2023 day 21 part 1"""
    return _count_locations(grid, next(grid.find("S")), steps)


def part_2(grid: RepeatingGrid[str], steps: int = 26501365) -> float:
    """Solution for Advent of Code 2023 day 21 part 2"""

    # The following solution is not by myself, but I couldn't figure out a better solution than
    # googling it. Apparently this is quadratic and has something to do with Lagrange. This is
    # true because S is on a line by its own in the puzzle input.
    #
    # https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/kee6vn6/
    # https://www.reddit.com/r/adventofcode/comments/18oh5f7/2023_day_21_part_2_how_does_the_solution_work/
    #
    # The Lagrange Interpolating Polynomial is defined as the unique (degree n-1) polynomial that
    # passes through the given n points. So if the data is actually a perfect quadratic (it is),
    # then that polynomial will actually be the quadratic.
    #
    # It is a fact that any input that contains one empty row and one empty column will eventually
    # settle into a quadratic every 2*boardsize steps. At some point, you'll start creeping into
    # every instance of the input in exactly the same way every boardsize steps (the 2 is to
    # maintain parity); but then if you count how many of those in each state you have, you'll
    # find it is either constant or grows linearly each boardsize steps while the "fully completed"
    # copies make up the quadratic part.
    #
    # All the inputs contain other properties to make it even nicer - there's no "eventually", so
    # that other forms of analysis will still work (said row/col is exactly on the S and you only
    # need to consider the outer border of tiles rather than there being something like massive
    # spirals that it can make a long time for the path to go through) so you can just check the
    # first three instances instead of needing to figure out when it starts having the pattern.
    #
    # We need to figure out how many garden plots can be reached after 26501365 steps.
    # Note that 26501365 = 202300 * 131 + 65, where 131 is the side length of the input grid.
    number_of_grids, remainder = divmod(steps, len(grid))

    # Store how many garden plots can be reached after 65, 65 + 131 and 65 + 2 * 131 steps, let's
    # call these numbers r₁, r₂ and r₃.

    # Our initial location is S.
    start_location = next(grid.find("S"))

    # Calculate r₁ = c, the amount of coordinates reachable after 65 steps
    # Calculate r₂ = a + b + c, the amount of coordinates reachable after 65 + 131 steps
    # Calculate r₃ = 4a + 2b + c, the amount of coordinates reachable after 65 + 2 * 131 steps
    # note: we could probably optimize by using the same result multiple times, but this works
    r = [_count_locations(grid, start_location, remainder + len(grid) * i) for i in range(3)]

    # Given:
    # r₁ = p(0) = c
    # r₂ = p(1) = a + b + c
    # r₃ = p(2) = 4a + 2b + c
    #
    # We can solve this linear system of equations as follows:
    # c = r₁  (easy)
    #
    # 4a + 2b = (4a + 2b + c) - c
    #      2a = (4a + 2b) - 2(a + b)
    #         = (r₃ - r₁) - 2(r₂ - r₁)
    #         = r₃ + r₁ - 2r₂
    #       a = (r₃ + r₁ - 2r₂) / 2
    #
    # b = (a + b + c) - a - c
    #   = r₂ - (r₃ + r₁ - 2r₂) / 2 - r₁
    #   = 2r₂ / 2 - (r₃ + r₁ - 2r₂) / 2 - 2r₁ / 2
    #   = (4r₂ - 3r₁ - r₃) / 2
    a = (r[2] + r[0] - 2 * r[1]) / 2
    b = (4 * r[1] - 3 * r[0] - r[2]) / 2
    c = r[0]

    # Now we simply calculate the polynomial (ax² + bx + c) for number_of_grids (x = 202300)
    return a * (number_of_grids**2) + b * number_of_grids + c

    # See also https://github.com/mrphlip/aoc/blob/master/2023/21.md for a different solution but
    # nice write-up
