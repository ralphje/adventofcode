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
    type_strength = list(sorted(counts.values(), reverse=True)) or [0]
    # Add the joker bonus if we have special handling for jokers (otherwise it is 0)
    type_strength[0] += joker_bonus

    return (
        type_strength,
        # Individual lookup of cards in the hand in the cards index. Sort cards in reverse order
        # to ensure proper ordering of worst to best.
        list(cards[::-1].index(card) for card in hand),
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
    """In Camel Cards, you get a list of hands, and your goal is to order them based on the
    strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8,
    7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the
    highest and 2 is the lowest.

    Every hand is exactly one type. From strongest to weakest, they are:

    * Five of a kind, where all five cards have the same label: AAAAA
    * Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    * Full house, where three cards have the same label, and the remaining two cards share a
      different label: 23332
    * Three of a kind, where three cards have the same label, and the remaining two cards are each
      different from any other card in the hand: TTT98
    * Two pair, where two cards share one label, two other cards share a second label, and the
      remaining card has a third label: 23432
    * One pair, where two cards share one label, and the other three cards have a different label
      from the pair and each other: A23A4
    * High card, where all cards' labels are distinct: 23456

    Hands are primarily ordered based on type; for example, every full house is stronger than any
    three of a kind.

    If two hands have the same type, a second ordering rule takes effect. Start by comparing the
    first card in each hand. If these cards are different, the hand with the stronger first card
    is considered stronger. If the first card in each hand have the same label, however, then move
    on to considering the second card in each hand. If they differ, the hand with the higher second
    card wins; otherwise, continue with the third card in each hand, then the fourth, then the
    fifth.

    Now, you can determine the total winnings of this set of hands by adding up the result of
    multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
    So the total winnings in this example are 6440.

    Find the rank of every hand in your set. What are the total winnings?
    """
    return solution(lines, "AKQJT98765432", special_joker=False)


def part_2(lines: list[str]) -> int:
    """To make things a little more interesting, the Elf introduces one additional rule. Now,
    J cards are jokers - wildcards that can act like whatever card would make the hand the strongest
    type possible.

    To balance this, J cards are now the weakest individual cards, weaker even than 2. The other
    cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

    J cards can pretend to be whatever card is best for the purpose of determining hand type;
    for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties
    between two hands of the same type, J is always treated as J, not the card it's pretending to
    be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

    Using the new joker rule, find the rank of every hand in your set. What are the new total
    winnings?
    """
    return solution(lines, "AKQT98765432J", special_joker=True)
