from __future__ import annotations

import math


def part_1(lines: list[str]) -> int:
    """As part of signing up, you get a sheet of paper (your puzzle input) that lists the time
    allowed for each race and also the best distance ever recorded in that race. To guarantee you
    win the grand prize, you need to make sure you go farther in each race than the current record
    holder.

    The organizer brings you over to the area where the boat races are held. The boats are much
    smaller than you expected - they're actually toy boats, each with a big button on top. Holding
    down the button charges the boat, and releasing the button allows the boat to move. Boats move
    faster if their button was held longer, but time spent holding the button counts against the
    total race time. You can only hold the button at the start of the race, and boats don't move
    until the button is released.

    For example::

        Time:      7  15   30
        Distance:  9  40  200

    This document describes three races:

    * The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
    * The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
    * The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.

    Your toy boat has a starting speed of zero millimeters per millisecond. For each whole
    millisecond you spend at the beginning of the race holding down the button, the boat's speed
    increases by one millimeter per millisecond.

    [...]

    Since the current record for this race is 9 millimeters, there are actually 4 different ways
    you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the
    race.

    In the second race, you could hold the button for at least 4 milliseconds and at most 11
    milliseconds and beat the record, a total of 8 different ways to win.

    In the third race, you could hold the button for at least 11 milliseconds and no more than 19
    milliseconds and still beat the record, a total of 9 ways you could win.

    To see how much margin of error you have, determine the number of ways you can beat the record in
    each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).

    Determine the number of ways you could beat the record in each race. What do you get if you
    multiply these numbers together?
    """
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
    # To solve this, we need to make sure that we floor the lower result + 1 (and conversely for
    # the upper we need to ceil - 1), to ensure that we have values that are within range.
    #
    # Then, we can simply subtract them from each other, and add 1. In other words,
    #  (ceil(-) - 1)  -  (floor(+) + 1)
    # This is equal to:
    #  ceil(-) - floor(+) - 2
    # And finally add 1 as both are inclusive, thus
    #  ceil(-) - floor(+) - 1
    #
    # Micro-optimization: since the √(t² - 4d) part is the same, we can simply calculate it once
    # by using an assignment expression.

    return math.prod(
        math.ceil((-time - (sqrt := math.sqrt(time**2 - 4 * distance))) / -2)
        - math.floor((-time + sqrt) / -2)
        - 1
        for time, distance in zip(
            *(map(int, line.split(":")[1].split()) for line in lines),
            strict=True,
        )
    )


def part_2(document: str) -> int:
    """As the race is about to start, you realize the piece of paper with race times and record
    distances you got earlier actually just has very bad kerning. There's really only one race -
    ignore the spaces between the numbers on each line.

    So, the example from before::

        Time:      7  15   30
        Distance:  9  40  200

    ...now instead means this::

        Time:      71530
        Distance:  940200

    Now, you have to figure out how many ways there are to win this single race. In this example,
    the race lasts for 71530 milliseconds and the record distance you need to beat is 940200
    millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the
    record, a total of 71503 ways!

    How many ways can you beat the record in this one much longer race?
    """

    return part_1(document.replace(" ", "").splitlines())
