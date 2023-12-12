"""This file holds the solutions for Advent of Code 2023 day 12: Hot Springs
https://adventofcode.com/2023/day/12
"""

import functools

from solutions.common.strings import ints


@functools.cache
def _permutations(line: str, groups: tuple[int]) -> int:
    """Taken and adjusted from my nonogram solver at
    https://github.com/ralphje/nonogram-solver/blob/master/nonogram/solvers.py

    Adjustments:
    * Only return the amount of permutations, not the permutations themselves
    * Accept line as string with `#`, `.` and `?` instead of an iterable with True, False, None
      (respectively)
    * Made Python 3 compatible (xrange.. yuck)
    """

    # When there are no specs, everything in the line must be empty = one combination
    if not groups:
        return 1

    # Keep track of contiguous blocks of damaged springs
    # block, *other_blocks does not provide a tuple, this does
    block, other_blocks = groups[0], groups[1:]

    # Keep the result somewhere
    result = 0

    # Get all possible permutations of space (operational springs) before the next block:
    # - We can get at most len(line) spaces (operational springs)
    # - The amount of space needed by other blocks must be subtracted
    #   (i.e. the sum of all block lengths plus the accompanying spaces)
    # - The block length must also be subtracted
    # - We add 1 as range yields [0..n-1] and we need [0..n] spaces
    space_needed_for_other_blocks = len(other_blocks) + sum(other_blocks)
    for space in range(len(line) - space_needed_for_other_blocks - block + 1):
        # Check if this amount of space (operational springs) is actually valid.
        # Break immediately if:
        # - any of the fields in the space is currently already a `#`, so we know there's a damaged
        #   spring in this attempt, so we can simply break out here (amount of space only increases)
        if any(c == "#" for c in line[:space]):
            break

        # Continue searching if:
        # - any of the springs in the calculated block of damaged springs is known to not be damaged
        #   (i.e. any of the fields is .)
        # - the field after the calculated block is currently `#` (if the block does not touch
        #   border), i.e. there wouldn't be a separating space between two blocks
        # - this is the last block and there is still a `#` field after the calculated block
        if (
            any(c == "." for c in line[space : space + block])
            or (len(line) > (space + block) and line[space + block] == "#")
            or (not other_blocks and any(c == "#" for c in line[space + block :]))
        ):
            continue

        # Now we recurse into this method, chopping off this space + block from the line and
        # continuing with the remaining blocks in the line.
        result += _permutations(line[space + block + 1 :], other_blocks)

    return result


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 12 part 1"""
    return sum(_permutations(line.split()[0], tuple(ints(line))) for line in lines)


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 12 part 2"""
    return part_1([
        f'{"?".join([s[0]] * 5)} {",".join([s[1]] * 5)}' for line in lines if (s := line.split())
    ])
