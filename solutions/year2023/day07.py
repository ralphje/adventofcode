"""This file holds the solutions for Advent of Code 2023 day 7: Camel Cards
https://adventofcode.com/2023/day/7
"""

import collections


def hand_strength(
    hand: str, cards: str, special_joker: bool = False
) -> tuple[list[int], list[int]]:
    """Returns the hand strength of the hand, used to sort the cards.

    :param hand: The hand string
    :param cards: All cards in order from best-worst.
    :param special_joker: If special_joker is True (part_2), then we do not count the amount of
        Jokers in the hand for  determining the hand type strength, but rather, add the amount of
        Jokers to the best part of the hand. In other words, if the hand is [2, 1] without 2
        Jokers, it is [4, 1] with 2 Jokers.
    :return: tuple:
        * list of sortable hand strength ([1,1,1,1,1] = worst, [5] = best)
        * list of individual card strengths (0 = worst)
    """

    # Count the amount of individual cards, and use that to sort the hands
    counts = collections.Counter(hand)
    # If we have a special_joker, do NOT count the amount of jokers
    joker_bonus = counts.pop("J", 0) if special_joker else 0

    # Get all card counts to get a ranking, using the fact that [1,1,1,1,1] sorts lower than
    # [2,1,1,1], ... to the best case, five-of-a-kind: [5].
    # List becomes [0] for the case that all values are Jokers (otherwise empty list)
    type_strength = sorted(counts.values(), reverse=True) or [0]
    # Add the joker bonus if we have special handling for jokers (otherwise it is 0)
    type_strength[0] += joker_bonus

    return (
        type_strength,
        # Individual lookup of cards in the hand in the cards index. Sort cards in reverse order
        # to ensure proper ordering of worst to best.
        [cards[::-1].index(card) for card in hand],
    )


def solution(lines: list[str], cards: str, special_joker: bool) -> int:
    """Provides the solution.

    The solution is the sum of all (rank*bids) for a sorted list of hands, as sorted by the
    hand_strength function.
    """
    return sum(
        (rank + 1) * int(card_bid[1])
        for rank, card_bid in enumerate(
            sorted(
                (line.split() for line in lines),
                key=lambda card_bid: hand_strength(card_bid[0], cards, special_joker),
            )
        )
    )


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 7 part 1"""

    return solution(lines, "AKQJT98765432", special_joker=False)


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 7 part 2"""

    return solution(lines, "AKQT98765432J", special_joker=True)
