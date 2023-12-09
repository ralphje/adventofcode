"""This file holds the solutions for Advent of Code 2023 day 2: Cube Conundrum
https://adventofcode.com/2023/day/2
"""

import math
from collections.abc import Iterable

type ColorCount = dict[str, int]


def _parse_document(lines: list[str]) -> Iterable[tuple[int, list[ColorCount]]]:
    """Parses the document, and returns iterable with pairs of::

    game_id, [{color: count}, ...]
    """

    return (
        (
            # Game ID
            int(game_line[0].split()[-1]),
            # List of dict of game sets, iterating over '; '
            [
                # Dict of game sets, each item is seperated by ', '
                {
                    # Each set color is separated by ' ', e.g. '3 blue'
                    game_set_color[1]: int(game_set_color[0])
                    for g in game_set.split(", ")
                    if (game_set_color := g.split())
                }
                for game_set in game_line[1].split("; ")
            ],
        )
        # Iterate over every line in the document, split on ': '.
        # game_line[0] is the game info, the game sets are in game_line[1]
        for line in lines
        if (game_line := line.split(": "))
    )


def part_1(document: list[str], thresholds: ColorCount | None = None) -> int:
    """Solution for Advent of Code 2023 day 2 part 1"""

    # Not a one-liner, but this is only here to prevent mutable default arguments
    if thresholds is None:
        thresholds = {"red": 12, "green": 13, "blue": 14}

    # Sum of all game_ids for which the condition holds
    return sum(
        game_id
        for game_id, game_sets in _parse_document(document)
        # All color counts in the set must be lower than the defined threshold
        # So we iterate over all colors and all game_sets, and check every color in every game_set
        if all(
            color_counts.get(cube_color, 0) <= thresholds[cube_color]
            for color_counts in game_sets
            for cube_color in thresholds
        )
    )


COLORS = ("red", "green", "blue")


def part_2(document: list[str]) -> int:
    """Solution for Advent of Code 2023 day 2 part 2"""

    # Produce a sum of...
    return sum(
        # ... all products of ...
        math.prod(
            # ... the maximum count ...
            max(
                # ... of each color in each game set ...
                game_set.get(color, 0)
                for game_set in game_sets
            )
            for color in COLORS
        )
        # ... in all game sets
        for _, game_sets in _parse_document(document)
    )
