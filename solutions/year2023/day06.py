"""This file holds the solutions for Advent of Code 2023 day 6: Wait For It
https://adventofcode.com/2023/day/6
"""

import math


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 6 part 1"""

    # This challenge basically boils down to:
    #  t = time of race (fixed for race)
    #  b = time of button press (what we need to optimize)
    #  d = distance travelled (what we need to achieve)
    #
    #  d = (t - b) * b, solve for b
    #  d = -b² + tb
    #  0 = -b² + tb - d
    #
    # Now we can use the quadratic formula:
    #  x = (-b ± √(b² - 4ac)) / 2a, a = -1, b = t, c = -d
    #  b = (-t ± √(t² - 4d)) / -2
    #
    # These equations provide the lower (-) and upper (+) bounds (exclusive) of the acceptable
    # values for b. Since it is exclusive, we cannot simply ceil and floor the results, as that
    # would be incorrect if the value is already rounded to an integer value. To solve this, we
    # need to make sure that we floor the lower bound and add 1 (and conversely for the upper bound
    # we need to ceil and subtract 1), to ensure that we have values that are within range.
    #
    # Then, we can simply subtract them from each other to get the amount of acceptable values,
    # adding one as both ranges are now inclusive:
    #  (ceil(-) - 1)  -  (floor(+) + 1) + 1
    #  = ceil(-) - floor(+) - 2 + 1
    #  = ceil(-) - floor(+) - 1
    #
    # Micro-optimization: since the √(t² - 4d) part is the same, we can simply calculate it once
    # by using an assignment expression.

    return math.prod(
        math.ceil((-time - (sqrt := math.sqrt(time**2 - 4 * distance))) / -2)
        - math.floor((-time + sqrt) / -2)
        - 1
        for time, distance in zip(*(map(int, line.split(":")[1].split()) for line in lines))
    )


def part_2(document: str) -> int:
    """Solution for Advent of Code 2023 day 6 part 2"""

    return part_1(document.replace(" ", "").splitlines())
