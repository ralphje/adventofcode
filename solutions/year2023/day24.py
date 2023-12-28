"""This file holds the solutions for Advent of Code 2023 day 24: Never Tell Me The Odds
https://adventofcode.com/2023/day/24
"""

# ruff: noqa: E501

import itertools

from sympy.matrices import Matrix

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
        for pair in itertools.combinations([ints(line) for line in lines], 2)
        if (intersect := pair_intersect(*pair))  # could be None if no solution is found
    )


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 24 part 2"""

    # ᵢ  ᵣ
    # We are searching for coordinates of a rock, (xᵣ, yᵣ, zᵣ) such that for some velocity
    # (vxᵣ, vyᵣ, vzᵣ), we intersect with any hailstone i starting at (xᵢ, yᵢ, zᵢ) and travelling at
    # (vxᵢ, vyᵢ, vzᵢ) such that at time tᵢ we intersect at the same location, i.e.:
    #
    #   xᵢ + vxᵢtᵢ = xᵣ + vxᵣtᵢ
    #   yᵢ + vyᵢtᵢ = yᵣ + vyᵣtᵢ
    #   zᵢ + vzᵢtᵢ = zᵣ + vzᵣtᵢ
    #
    # Rearranging the first equation to cancel out the tᵢ factor:
    #
    #    xᵢ + vxᵢtᵢ         =  xᵣ + vxᵣtᵢ
    #         vxᵢtᵢ - vxᵣtᵢ =  xᵣ - xᵢ
    #     tᵢ (vxᵢ   - vxᵣ ) =  xᵣ - xᵢ
    #     tᵢ                = (xᵣ - xᵢ) / (vxᵢ - vxᵣ)
    #
    # =>  tᵢ = (xᵣ - xᵢ) / (vxᵢ - vxᵣ)
    #     tᵢ = (yᵣ - yᵢ) / (vyᵢ - vyᵣ)    by symmetry
    #     tᵢ = (zᵣ - zᵢ) / (vzᵢ - vzᵣ)    by symmetry
    #
    # => (xᵣ - xᵢ) / (vxᵢ - vxᵣ) = (yᵣ - yᵢ) / (vyᵢ - vyᵣ) = (zᵣ - zᵢ) / (vzᵢ - vzᵣ)
    #
    # We can rearrange the first equation to make sure that the same term does not depend on the
    # chosen hailstone i:
    #
    #          (xᵣ - xᵢ) / (vxᵢ - vxᵣ) = (yᵣ - yᵢ) / (vyᵢ - vyᵣ)
    #          (xᵣ - xᵢ) * (vyᵢ - vyᵣ) = (yᵣ - yᵢ) * (vxᵢ - vxᵣ)
    #    xᵣvyᵢ - xᵣvyᵣ - xᵢvyᵢ + xᵢvyᵣ = yᵣvxᵢ - yᵣvxᵣ - yᵢvxᵢ + yᵢvxᵣ
    #          - xᵣvyᵣ                 = yᵣvxᵢ - yᵣvxᵣ - yᵢvxᵢ + yᵢvxᵣ + xᵢvyᵢ - xᵢvyᵣ - xᵣvyᵢ
    #    yᵣvxᵣ - xᵣvyᵣ                 = yᵣvxᵢ         - yᵢvxᵢ + yᵢvxᵣ + xᵢvyᵢ - xᵢvyᵣ - xᵣvyᵢ
    #    yᵣvxᵣ - xᵣvyᵣ                 = yᵣvxᵢ - xᵣvyᵢ + yᵢvxᵣ - xᵢvyᵣ + xᵢvyᵢ - yᵢvxᵢ
    #
    # By symmetry, we can apply this to (x, z) and (y, z) as well:
    #
    #   yᵣvxᵣ - xᵣvyᵣ = yᵣvxᵢ - xᵣvyᵢ + yᵢvxᵣ - xᵢvyᵣ + xᵢvyᵢ - yᵢvxᵢ
    #   zᵣvxᵣ - xᵣvzᵣ = zᵣvxᵢ - xᵣvzᵢ + zᵢvxᵣ - xᵢvzᵣ + xᵢvzᵢ - zᵢvxᵢ
    #   zᵣvyᵣ - yᵣvzᵣ = zᵣvyᵢ - yᵣvzᵢ + zᵢvyᵣ - yᵢvzᵣ + yᵢvzᵢ - zᵢvyᵢ
    #
    # Since we have chosen random hailstone i, and we know that all stones must intersect at
    # the same point, we can equate these with any hailstones, to create a
    # system of 6 equations with 6 unknowns (xᵣ, yᵣ, zᵣ, vxᵣ, vyᵣ, vzᵣ):
    #
    #    (xᵣ - x₁) / (vx₁ - vxᵣ) = (yᵣ - y₁) / (vy₁ - vyᵣ) = (zᵣ - z₁) / (vz₁ - vzᵣ)
    #    (xᵣ - x₂) / (vx₂ - vxᵣ) = (yᵣ - y₂) / (vy₂ - vyᵣ) = (zᵣ - z₂) / (vz₂ - vzᵣ)
    #    (xᵣ - x₃) / (vx₃ - vxᵣ) = (yᵣ - y₃) / (vy₃ - vyᵣ) = (zᵣ - z₃) / (vz₃ - vzᵣ)
    #
    # This gives us the following set of 9 equations (multiplied by -1 on each side):
    #
    #   xᵣvyᵣ - yᵣvxᵣ = xᵣvy₁ - yᵣvx₁ + y₁vx₁ - x₁vy₁ + x₁vyᵣ - y₁vxᵣ
    #   xᵣvyᵣ - yᵣvxᵣ = xᵣvy₂ - yᵣvx₂ + y₂vx₂ - x₂vy₂ + x₂vyᵣ - y₂vxᵣ
    #   xᵣvyᵣ - yᵣvxᵣ = xᵣvy₃ - yᵣvx₃ + y₃vx₃ - x₃vy₃ + x₃vyᵣ - y₃vxᵣ
    #
    #   xᵣvzᵣ - zᵣvxᵣ = xᵣvz₁ - zᵣvx₁ + z₁vx₁ - x₁vz₁ + x₁vzᵣ - z₁vxᵣ
    #   xᵣvzᵣ - zᵣvxᵣ = xᵣvz₂ - zᵣvx₂ + z₂vx₂ - x₂vz₂ + x₂vzᵣ - z₂vxᵣ
    #   xᵣvzᵣ - zᵣvxᵣ = xᵣvz₃ - zᵣvx₃ + z₃vx₃ - x₃vz₃ + x₃vzᵣ - z₃vxᵣ
    #
    #   yᵣvzᵣ - zᵣvyᵣ = yᵣvz₁ - zᵣvy₁ + z₁vy₁ - y₁vz₁ + y₁vzᵣ - z₁vyᵣ
    #   yᵣvzᵣ - zᵣvyᵣ = yᵣvz₂ - zᵣvy₂ + z₂vy₂ - y₂vz₂ + y₂vzᵣ - z₂vyᵣ
    #   yᵣvzᵣ - zᵣvyᵣ = yᵣvz₃ - zᵣvy₃ + z₃vy₃ - y₃vz₃ + y₃vzᵣ - z₃vyᵣ
    #
    # We can now cancel out the first terms (i.e. equation 1 = equation 2, equation 1 = equation 3,
    # and so on for the other 6) to result in a set of 6 linear equations. The first one, we can
    # simplify and rearrange as follows, to make sure that the unknowns are on one side:
    #
    #  xᵣvy₁ - yᵣvx₁ + y₁vx₁ - x₁vy₁ + x₁vyᵣ - y₁vxᵣ = xᵣvy₂ - yᵣvx₂ + y₂vx₂ - x₂vy₂ + x₂vyᵣ - y₂vxᵣ
    #  xᵣvy₁ - xᵣvy₂ + yᵣvx₁ - yᵣvx₂ + x₁vyᵣ - x₂vyᵣ + y₂vxᵣ - y₁vxᵣ = y₂vx₂ - x₂vy₂ - y₁vx₁ + x₁vy₁
    #  xᵣ(vy₁ - vy₂) + yᵣ(vx₂ - vx₁) + vxᵣ(y₂ - y₁) + vyᵣ(x₁ - x₂) = (y₂vx₂ - x₂vy₂) - (y₁vx₁ - x₁vy₁)
    #
    # By symmetry:
    #
    #  xᵣ(vy₁ - vy₂) + yᵣ(vx₂ - vx₁) +                 vxᵣ(y₂ - y₁) + vyᵣ(x₁ - x₂)                = (y₂vx₂ - x₂vy₂) - (y₁vx₁ - x₁vy₁)
    #  xᵣ(vy₁ - vy₃) + yᵣ(vx₃ - vx₁) +                 vxᵣ(y₃ - y₁) + vyᵣ(x₁ - x₃)                = (y₃vx₂ - x₃vy₃) - (y₁vx₁ - x₁vy₁)
    #  xᵣ(vz₂ - vz₁) +                 zᵣ(vx₁ - vx₂) + vxᵣ(z₁ - z₂) +                vzᵣ(x₂ - x₁) = (x₂vz₂ - z₂vx₂) - (x₁vz₁ - z₁vx₁)
    #  xᵣ(vz₃ - vz₁) +                 zᵣ(vx₁ - vx₃) + vxᵣ(z₁ - z₃) +                vzᵣ(x₃ - x₁) = (x₃vz₂ - z₃vx₃) - (x₁vz₁ - z₁vx₁)
    #                  yᵣ(vz₁ - vz₂) + zᵣ(vy₂ - vy₁) +                vyᵣ(z₂ - z₁) + vzᵣ(y₁ - y₂) = (z₂vy₂ - y₂vz₂) - (z₁vy₁ - y₁vz₁)
    #                  yᵣ(vz₁ - vz₃) + zᵣ(vy₃ - vy₁) +                vyᵣ(z₃ - z₁) + vzᵣ(y₁ - y₃) = (z₃vy₂ - y₃vz₃) - (z₁vy₁ - y₁vz₁)
    #
    # We can now use linear algebra to solve this system of linear equations:
    #
    # if we have M * h = s, where we know M and s, and h is unknown, we can simply use the
    # mathematical inverse of M to get h = M^-1 * s = (xᵣ, yᵣ, zᵣ, vxᵣ, vyᵣ, vzᵣ)

    hails = iter(ints(line) for line in lines)
    (
        (x1, y1, z1, vx1, vy1, vz1),
        (x2, y2, z2, vx2, vy2, vz2),
        (x3, y3, z3, vx3, vy3, vz3),
    ) = (
        next(hails),
        next(hails),
        next(hails),
    )

    matrix = Matrix([
        [vy1 - vy2, vx2 - vx1, 0, y2 - y1, x1 - x2, 0],
        [vy1 - vy3, vx3 - vx1, 0, y3 - y1, x1 - x3, 0],
        [vz2 - vz1, 0, vx1 - vx2, z1 - z2, 0, x2 - x1],
        [vz3 - vz1, 0, vx1 - vx3, z1 - z3, 0, x3 - x1],
        [0, vz1 - vz2, vy2 - vy1, 0, z2 - z1, y1 - y2],
        [0, vz1 - vz3, vy3 - vy1, 0, z3 - z1, y1 - y3],
    ])
    vector = Matrix([
        (y2 * vx2 - x2 * vy2) - (y1 * vx1 - x1 * vy1),
        (y3 * vx3 - x3 * vy3) - (y1 * vx1 - x1 * vy1),
        (x2 * vz2 - z2 * vx2) - (x1 * vz1 - z1 * vx1),
        (x3 * vz3 - z3 * vx3) - (x1 * vz1 - z1 * vx1),
        (z2 * vy2 - y2 * vz2) - (z1 * vy1 - y1 * vz1),
        (z3 * vy3 - y3 * vz3) - (z1 * vy1 - y1 * vz1),
    ])
    # Using sympy for infinite-precision vectors. I'm 100% completely done with this challenge, so
    # implementing my own Gaussian reduction is beyond what I want to do.
    result = matrix.inv() * vector
    return sum(result[:3])  # x + y + z
