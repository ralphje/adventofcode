"""This file holds the solutions for Advent of Code 2023 day 8: Haunted Wasteland
https://adventofcode.com/2023/day/8
"""

import itertools
import math
import re


def _parse_map(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    """Parses the map in seperate directions and nodes parts, respectively."""

    return (
        lines[0],
        {
            items[0]: (items[1], items[2])
            for line in lines[2:]
            if (items := re.findall(r"[A-Z0-9]{3}", line))
        },
    )


def _number_of_moves(node: str, directions: str, nodes: dict[str, tuple[str, str]]) -> int:
    """Determines the number of moves needed for the starting node with given directions and nodes
    to end up at a node ending with Z.

    .. note::

       Ending up at a Z-node does not mean that the cycle must always repeat itself after this node.
       In practice, it does.
    """

    for i, direction in enumerate(itertools.cycle(directions)):
        if node.endswith("Z"):
            return i
        node = nodes[node][int(direction == "R")]


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 8 part 1"""

    return _number_of_moves("AAA", *_parse_map(lines))


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 8 part 2"""

    directions, nodes = _parse_map(lines)

    # LCM should not work by definition. In theory, this is *a* solution iff the ghosts cycle after
    # their first encounter with a Z node. If there are multiple Z nodes, it would also break,, etc.
    # But it works for this puzzle, so I'm satisfied ;).
    return math.lcm(
        *(
            _number_of_moves(start_node, directions, nodes)
            for start_node in nodes
            if start_node.endswith("A")
        )
    )
