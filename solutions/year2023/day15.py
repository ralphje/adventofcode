"""This file holds the solutions for Advent of Code 2023 day 15: Lens Library
https://adventofcode.com/2023/day/15
"""

import functools
import math
import re


def _hash(s: str) -> int:
    """Hash the input string using the provided hash algorithm"""
    # Iterate using reduce, using the hash algorithm to keep adding a value.
    return functools.reduce(lambda base, add: (base + ord(add)) * 17 % 256, s, 0)


def part_1(puzzle: str) -> int:
    """Solution for Advent of Code 2023 day 15 part 1"""
    return sum(_hash(step) for step in puzzle.split(","))


STEP_RE = re.compile(r"^([^-=]+)([-=])(\d*)$")


def part_2(puzzle: str) -> float:
    """Solution for Advent of Code 2023 day 15 part 2"""
    # Create a new list with new boxes. Each box will be of the form {label: focal_length}
    # We make use of the fact that since Python 3.7, dicts are sorted in their insertion order
    boxes: list[dict[str, int]] = [{} for _ in range(256)]

    # Move through each step
    for step in puzzle.split(","):
        # Parse the step, using regex
        label, operation, focal_length = STEP_RE.findall(step)[0]
        # Find the appropriate box
        box = boxes[_hash(label)]

        if operation == "-":
            # Remove the label from the box if it exists
            box.pop(label, None)
        else:
            # Otherwise, insert/update the focal length. Updates are always in-place.
            box[label] = int(focal_length)

    # We basically now do:
    #   sum(
    #        1..256 *                    (box ID)
    #        sum(focal_lengths * 1..n)   (focal lengths * position)
    #   )
    return math.sumprod(
        (math.sumprod(box.values(), range(1, len(box) + 1)) for box in boxes),
        range(1, 257),
    )
