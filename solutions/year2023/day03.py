"""This file holds the solutions for Advent of Code 2023 day 3: Gear Ratios
https://adventofcode.com/2023/day/3
"""

import math
import re
from collections.abc import Iterable

NUMBERS_RE = re.compile(r"\d+")
type Coordinate = tuple[int, int]


def _symbol_locations_in_document(
    document: list[str], pattern: re.Pattern[str]
) -> Iterable[Coordinate]:
    """Gather all symbol locations in the document as defined in pattern, in an iterable of (y,x)
    tuples
    """
    return (
        (i, symbol.start()) for i, line in enumerate(document) for symbol in pattern.finditer(line)
    )


def _vicinity(match: re.Match[str], line: int) -> Iterable[Coordinate]:
    """Returns all coordinates in the vicinity of the recorded match on recorded line.

    Note: it will produce numbers that overshoot the boundaries of the document, but that's fine. It
    will not produce coordinates that are below 0.
    """
    return (
        (y, x)
        for y in range(max(line - 1, 0), line + 2)
        for x in range(max(match.start() - 1, 0), match.end() + 1)
    )


def part_1(document: list[str]) -> int:
    """Solution for Advent of Code 2023 day 3 part 1"""

    # We don't care about the symbol locations, only about their positions
    symbols = list(_symbol_locations_in_document(document, pattern=re.compile(r"[^.\d]")))

    # Sum ...
    return sum(
        # ... number group ...
        int(number.group())
        # ... in every line in the document ...
        for i, line in enumerate(document)
        # ... every re number ...
        for number in NUMBERS_RE.finditer(line)
        # ... for which we've got a symbol around it
        if any(coordinate in symbols for coordinate in _vicinity(number, i))
    )


def part_2(document: list[str]) -> int:
    """Solution for Advent of Code 2023 day 3 part 2"""

    # Construct a dict of all gear locations, with a list that will be used to contain part numbers
    gears: dict[Coordinate, list[int]] = {
        coordinate: []
        for coordinate in _symbol_locations_in_document(document, pattern=re.compile(r"\*"))
    }

    # Iterate over all numbers and check their vicinity to any of the gears. If so, put it in
    # a list with that gear.
    for i, line in enumerate(document):
        for number in NUMBERS_RE.finditer(line):
            for coordinate in _vicinity(number, i):
                if coordinate in gears:
                    gears[coordinate].append(int(number.group()))

    # Now that we have all gears, we simply calculate the gear ratios.
    return sum(math.prod(gear) for gear in gears.values() if len(gear) == 2)
