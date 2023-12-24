"""This file holds the solutions for Advent of Code 2023 day 22: Sand Slabs
https://adventofcode.com/2023/day/22
"""

import collections
import itertools

from solutions.common.strings import ints


def _bricks(lines: list[str]) -> list[set[tuple[int, int, int]]]:
    """Return a list of sets of coordinates for each brick in the input."""
    return sorted(
        [
            {
                (x, y, z)
                for x in range(i[0], i[3] + 1)
                for y in range(i[1], i[4] + 1)
                for z in range(i[2], i[5] + 1)
            }
            for line in lines
            # Note: line = x1 y1 z1 x2 y2 z2, so this works
            if (i := ints(line))
        ],
        # we sort by the lowest part of the brick
        key=lambda brick: min(c[2] for c in brick),
    )


def _supports_supported(
    bricks: list[set[tuple[int, int, int]]]
) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    """Given a list of bricks, will return for each brick, which bricks it supports, and which
    bricks are supporting it.

    Result is:
    - dict of bricks, id to the brick ids it supports
    - dict of bricks, id to the brick ids it is supporting
    """

    # Keep track of coordinates and which block occupies it
    occupied = {}
    # Keep track of each of the bricks
    supports = {i: set() for i in range(len(bricks))}
    supported = {i: set() for i in range(len(bricks))}

    for i, brick in enumerate(bricks):
        # Try lowering the brick in increasing intervals
        for tolerance in itertools.count():
            lowered_brick = {(x, y, z - tolerance) for x, y, z in brick}
            # Check which bricks are supported by it (if any)
            supporting_bricks = {
                occupied[(x, y, z - 1)] for x, y, z in lowered_brick if (x, y, z - 1) in occupied
            }
            # If any brick supports it now, or we reach the ground, we know we are done
            if supporting_bricks or any(pos[-1] == 1 for pos in lowered_brick):
                break
        else:
            raise AssertionError("unreachable")

        # Add the lowered brick to the occupied region
        occupied |= {p: i for p in lowered_brick}

        # Add the supporting brick to the supported, and vice versa
        for supporting_brick in supporting_bricks:
            supports[supporting_brick].add(i)
            supported[i].add(supporting_brick)

    return supports, supported


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 22 part 1"""
    bricks = _bricks(lines)
    supports, supported = _supports_supported(bricks)

    return sum(
        # count the amount of bricks, where each brick it supports, is at least supported by
        # 2 bricks
        int(all(len(supported[brick]) >= 2 for brick in supporting_bricks))
        for supporting_bricks in supports.values()
    )


def _chain(supports: dict[int, set[int]], supported: dict[int, set[int]], brick: int) -> int:
    """Calculate the chain that would result when the provided brick is removed."""

    # Keep track of the bricks we are going to remove, and the bricks we have removed
    visited = set()
    queue = collections.deque([brick])
    # This is going to be the result
    result = 0
    while queue:
        brick = queue.popleft()
        visited.add(brick)

        # Now try to iterate deeper by checking which bricks are supported by this brick
        for supported_brick in supports[brick]:
            # If there's no brick left to support this brick, we visit it next
            if not supported[supported_brick] - visited:
                queue.append(supported_brick)
                result += 1
    return result


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 22 part 2"""
    bricks = _bricks(lines)
    supports, supported = _supports_supported(bricks)
    return sum(_chain(supports, supported, brick) for brick in range(len(bricks)))
