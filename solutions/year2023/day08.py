"""This file holds the solutions for Advent of Code 2023 day 8: Haunted Wasteland
https://adventofcode.com/2023/day/8
"""

import contextlib
import itertools
import math
import re

from solutions.common.math import chinese_remainder_generic


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
    to end up at a node ending with Z. Returns the number of moves and the ending node.

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


def _cycle_detect(
    node: str, directions: str, nodes: dict[str, tuple[str, str]]
) -> tuple[int, int, list[int]]:
    """Given directions and nodes, will determine when the directions start to loop in nodes, and
    returns:

    * The length of the tail before the loop starts
    * The size of the loop
    * The positions relative to the start (not the loop start) of valid end nodes.

    """

    loop_start, seen = 0, []
    for i, direction in enumerate(itertools.cycle(directions)):
        curr = (i % len(directions), node)
        if curr in seen:
            loop_start = seen.index(curr)
            break
        seen.append(curr)
        node = nodes[node][int(direction == "R")]

    return (
        loop_start,  # the length of the first tail
        len(seen) - loop_start,  # the length of the loop
        [seen.index(i) for i in seen if i[1].endswith("Z")],
    )


def part_2_crt(lines: list[str]) -> int:
    """Alternative solution to part 2 that uses the Chinese Remainder Theorem.

    Note: this has not been properly tested, but it seems to work.
    """

    directions, nodes = _parse_map(lines)

    # Gather all options of n (the loop length) and a (the end node) for the equations used
    # in the CRT. Note that any one of each element must hold, but it does not matter which one.
    n_a_options = []
    for node in (node for node in nodes if node.endswith("A")):
        loop_start, loop_length, end_nodes = _cycle_detect(node, directions, nodes)
        n_a_options.append([(loop_length, end_node) for end_node in end_nodes])

    # Gather results, using the CRT to resolve the equations, ignoring any errors the CRT may throw
    results = []
    for n_a_i in itertools.product(*n_a_options):
        with contextlib.suppress(Exception):
            results.append(chinese_remainder_generic(*zip(*n_a_i)))

    # The minimum length is the valid solution.
    return min(results)
