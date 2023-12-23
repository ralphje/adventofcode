"""This file holds the solutions for Advent of Code 2023 day 21: Step Counter
https://adventofcode.com/2023/day/21
"""

from collections.abc import Collection

from solutions.common.grid import Grid, RepeatingGrid


def _all_directions(grid: Grid[str], locations: Collection[complex]) -> Collection[complex]:
    """Given a set of locations, return all reachable locations from this set."""

    # This saves 50% of time, by only checking the grid for # after selecting unique directions
    directions = {direction for location in locations for direction in grid.orthogonal(location)}
    return [d for d in directions if grid.get(d) != "#"]


def _repeat_all_directions(
    grid: Grid[str], locations: Collection[complex], steps: int
) -> Collection[complex]:
    """Try to reach all directions, a number of times.

    This is extremely naive, as we could simply use the fact that the amount of steps must be even,
    so we could just choose to ever expand into new directions, but whatever.
    """
    for _ in range(steps):
        locations = _all_directions(grid, locations)
    return locations


def part_1(grid: Grid[str], steps: int = 64) -> int:
    """Solution for Advent of Code 2023 day 21 part 1"""
    return len(_repeat_all_directions(grid, {next(grid.find("S"))}, steps))


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
    locations = {next(grid.find("S"))}

    # Calculate r₁ = c, the amount of coordinates reachable after 65 steps
    locations = _repeat_all_directions(grid, locations, remainder)
    r_1 = len(locations)

    # Calculate r₂ = a + b + c, the amount of coordinates reachable after 65 + 131 steps
    locations = _repeat_all_directions(grid, locations, len(grid))
    r_2 = len(locations)

    # Calculate r₃ = 4a + 2b + c, the amount of coordinates reachable after 65 + 2 * 131 steps
    locations = _repeat_all_directions(grid, locations, len(grid))
    r_3 = len(locations)

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
    a = (r_3 + r_1 - 2 * r_2) / 2
    b = (4 * r_2 - 3 * r_1 - r_3) / 2
    c = r_1

    # Now we simply calculate the polynomial (ax² + bx + c) for number_of_grids (x = 202300)
    return a * (number_of_grids**2) + b * number_of_grids + c

    # See also https://github.com/mrphlip/aoc/blob/master/2023/21.md for a different solution but
    # nice write-up
