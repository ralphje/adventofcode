import math
import re
from collections.abc import Iterable

NUMBERS_RE = re.compile(r"\d+")
type Coordinate = tuple[int, int]


def _symbol_locations_in_document(document: str, pattern: re.Pattern[str]) -> Iterable[Coordinate]:
    """Gather all symbol locations in the document as defined in pattern, in an iterable of (y,x)
    tuples
    """
    return (
        (i, symbol.start())
        for i, line in enumerate(document.splitlines())
        for symbol in pattern.finditer(line)
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


def part_1(document: str) -> int:
    """The engine schematic (your puzzle input) consists of a visual representation of the engine.
    There are lots of numbers and symbols you don't really understand, but apparently any number
    adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum.
    (Periods (.) do not count as a symbol.)

    Here is an example engine schematic::

        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..

    In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
    114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a
    part number; their sum is 4361.
    """

    # We don't care about the symbol locations, only about their positions
    symbols = list(_symbol_locations_in_document(document, pattern=re.compile(r"[^.\d]")))

    # Sum ...
    return sum(
        # ... number group ...
        int(number.group())
        # ... in every line in the document ...
        for i, line in enumerate(document.splitlines())
        # ... every re number ...
        for number in NUMBERS_RE.finditer(line)
        # ... for which we've got a symbol around it
        if any(coordinate in symbols for coordinate in _vicinity(number, i))
    )


def part_2(document: str) -> int:
    """The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is
    any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of
    multiplying those two numbers together.

    This time, you need to find the gear ratio of every gear and add them all up so that the
    engineer can figure out which gear needs to be replaced.

    Consider the same engine schematic again::

        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..

    In this schematic, there are two gears. The first is in the top left; it has part numbers 467
    and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is
    451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.)
    Adding up all of the gear ratios produces 467835.
    """

    # Construct a dict of all gear locations, with a list that will be used to contain part numbers
    gears: dict[Coordinate, list[int]] = {
        coordinate: []
        for coordinate in _symbol_locations_in_document(document, pattern=re.compile(r"\*"))
    }

    # Iterate over all numbers and check their vicinity to any of the gears. If so, put it in
    # a list with that gear.
    for i, line in enumerate(document.splitlines()):
        for number in NUMBERS_RE.finditer(line):
            for coordinate in _vicinity(number, i):
                if coordinate in gears:
                    gears[coordinate].append(int(number.group()))

    # Now that we have all gears, we simply calculate the gear ratios.
    return sum(math.prod(gear) for gear in gears.values() if len(gear) == 2)
