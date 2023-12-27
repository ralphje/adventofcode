"""This file holds the solutions for Advent of Code 2023 day 24: Never Tell Me The Odds
https://adventofcode.com/2023/day/24
"""

import itertools

from solutions.common.strings import ints


def pair_intersect(
    hail_1: tuple[int, int, int, int, int, int],
    hail_2: tuple[int, int, int, int, int, int],
) -> tuple[float, float, float, float] | None:
    """We solve the two hailstones whether they will intersect, and return the (x,y) coordinates,
    and times t1 and t2 when that happens.
    """

    # We need to make sure that both paths of the provided pair will be at the same location at
    # one point in time. This means solving these equations, where t₁ and t₂ represent the time
    # of intersection (which does not need to be the same):
    #   x₁ + vx₁t₁ =  x₂ + vx₂t₂
    #   y₁ + vy₁t₁ =  y₂ + vy₂t₂
    #
    # Let's solve for t₂:
    #   x₁ + vx₁t₁ =  x₂ + vx₂t₂                                       (given)
    #        vx₁t₁ =  x₂ + vx₂t₂ - x₁
    #           t₁ = (x₂ + vx₂t₂ - x₁) / vx₁
    #
    #  y₁ +  vy₁t₁                            =    y₂ +    vy₂t₂       (given)
    #  y₁ +  vy₁((x₂ +  vx₂t₂ -    x₁) / vx₁) =    y₂ +    vy₂t₂       (substituting t₁)
    #  y₁ + (vy₁x₂ + vy₁vx₂t₂ - vy₁x₁) / vx₁) =    y₂ +    vy₂t₂
    #       (vy₁x₂ + vy₁vx₂t₂ - vy₁x₁) / vx₁  =    y₂ +    vy₂t₂ -    y₁
    #        vy₁x₂ + vy₁vx₂t₂ - vy₁x₁         = vx₁y₂ + vx₁vy₂t₂ - vx₁y₁   (for vx₁ ≠ 0)
    #                vy₁vx₂t₂ - vy₁x₁         = vx₁y₂ + vx₁vy₂t₂ - vx₁y₁ - vy₁x₂
    #                vy₁vx₂t₂                 = vx₁y₂ + vx₁vy₂t₂ - vx₁y₁ - vy₁x₂ + vy₁x₁
    #                vy₁vx₂t₂ - vx₁vy₂t₂      = vx₁y₂            - vx₁y₁ - vy₁x₂ + vy₁x₁
    #            t₂( vy₁vx₂   - vx₁vy₂ )      = vx₁y₂            - vx₁y₁ - vy₁x₂ + vy₁x₁
    #            t₂                           = (vx₁y₂ - vx₁y₁ - vy₁x₂ + vy₁x₁) / ( vy₁vx₂ - vx₁vy₂)
    #                                            (for vy₁vx₂ ≠ vx₁vy₂)
    #            t₂                           = (vx₁ (y₂ - y₁) - vy₁ (x₂ - x₁)) / ( vy₁vx₂ - vx₁vy₂)
    #
    #
    # By symmetry, the same also holds for t₁, therefore:
    #
    # t₁ = (vx₂(y₁ - y₂) - vy₂(x₁ - x₂)) / (vy₂vx₁ - vx₂vy₁)
    # t₂ = (vx₁(y₂ - y₁) - vy₁(x₂ - x₁)) / (vy₁vx₂ - vx₁vy₂)

    (x1, y1, _, vx1, vy1, _), (x2, y2, _, vx2, vy2, _) = hail_1, hail_2

    # Cannot have the same value, i.e. vy₁vx₂ ≠ vx₁vy₂
    if vy1 * vx2 == vx1 * vy2:
        return None

    # See derivation above
    t1 = (vx2 * (y1 - y2) - vy2 * (x1 - x2)) / (vy2 * vx1 - vx2 * vy1)
    t2 = (vx1 * (y2 - y1) - vy1 * (x2 - x1)) / (vy1 * vx2 - vx1 * vy2)

    # The X and Y positions can calculate be calculated by using the just calculated t₁ (or t₂)
    # and substituting it in the formula above
    x, y = x1 + t1 * vx1, y1 + t1 * vy1
    return x, y, t1, t2


def part_1(
    lines: list[str],
    x_range: tuple[float, float] = (200000000000000, 400000000000000),
    y_range: tuple[float, float] = (200000000000000, 400000000000000),
) -> int:
    """Solution for Advent of Code 2023 day 24 part 1"""
    return sum(
        (
            x_range[0] < intersect[0] < x_range[1]  # x
            and y_range[0] < intersect[1] < y_range[1]  # y
            and intersect[2] > 0  # t1
            and intersect[3] > 0  # t2
        )
        for pair in itertools.combinations([ints(l) for l in lines], 2)
        if (intersect := pair_intersect(*pair))  # could be None if no solution is found
    )


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 24 part 2"""
    pass
