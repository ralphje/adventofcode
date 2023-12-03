import math
from collections.abc import Iterable

type ColorCount = dict[str, int]


def _parse_document(document: str) -> Iterable[tuple[int, list[ColorCount]]]:
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
        for line in document.splitlines()
        if (game_line := line.split(": "))
    )


def part_1(document: str, thresholds: ColorCount | None = None) -> int:
    """You play several games and record the information from each game (your puzzle input). Each
    game is listed with its ID number (like the 11 in Game 11: ...) followed by a
    semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red,
    5 green, 4 blue).

    For example, the record of a few games might look like this::

        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    In game 1, three sets of cubes are revealed from the bag (and then put back again). The first
    set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue
    cubes; the third set is only 2 green cubes.

    The Elf would first like to know which games would have been possible if the bag contained only
    12 red cubes, 13 green cubes, and 14 blue cubes?

    In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded
    with that configuration. However, game 3 would have been impossible because at one point the
    Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because
    the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have
    been possible, you get 8.
    """

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


def part_2(document: str) -> int:
    """As you continue your walk, the Elf poses a second question: in each game you played, what is
    the fewest number of cubes of each color that could have been in the bag to make the game
    possible?

    Again consider the example games from earlier::

        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    * In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes.
      If any color had even one fewer cube, the game would have been impossible.
    * Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
    * Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
    * Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    * Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied
    together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12,
    1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

    For each game, find the minimum set of cubes that must have been present. What is the sum of
    the power of these sets?
    """

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
