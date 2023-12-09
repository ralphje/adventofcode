"""This file holds the solutions for Advent of Code 2023 day 4: Scratchcards
https://adventofcode.com/2023/day/4
"""

import collections
from collections.abc import Iterable

type Game = list[set[str]]


def _parse_cards(document: list[str]) -> Iterable[Game]:
    return ([set(g.split()) for g in line.split(":")[1].split("|")] for line in document)


def part_1(document: list[str]) -> int:
    """Solution for Advent of Code 2023 day 4 part 1"""

    # int(2 ** ...) works because:
    # 2 ** 0-1 = 2 ** -1 = 0.5 -> int(0.5) = 0
    # 2 ** 1-1 = 2 **  0 = 1

    return sum(int(2 ** (len(game[0] & game[1]) - 1)) for game in _parse_cards(document))


def part_2(document: list[str]) -> int:
    """Solution for Advent of Code 2023 day 4 part 2"""

    card_counts: collections.Counter[int] = collections.Counter()
    for i, game in enumerate(_parse_cards(document)):
        card_counts.update({
            i: 1,  # increase the card count for the current game
            **{
                j: card_counts[i] + 1  # add the amount of current cards + 1
                for j in range(i + 1, i + len(game[0] & game[1]) + 1)
            },
        })
    return card_counts.total()
