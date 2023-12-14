"""This file holds the solutions for Advent of Code 2023 day 13: Point of Incidence
https://adventofcode.com/2023/day/13
"""


def _find_mirror_point(lines: list[str], smudges: int = 0) -> int:
    return next(
        (
            # Return the first valid mirror point
            i
            # Iterated over all possible mirror points
            for i in range(1, len(lines))
            # Where...
            if sum(
                # Count the amount of times the character pairs do not match
                # (Note: True == 1)
                c1 != c2
                # Iterated over line pairs, as split on line i, first part reversed
                for l1, l2 in zip(lines[i - 1 :: -1], lines[i:])
                # Iterated over each character pair in each line pair
                for c1, c2 in zip(l1, l2)
            )
            # This must equal the amount of smudges
            == smudges
        ),
        # Return 0 if no mirror point was found
        0,
    )


def part_1(blocks: str, smudges: int = 0) -> int:
    """Solution for Advent of Code 2023 day 13 part 1"""
    return sum(
        # amount of horizontal mirror points
        _find_mirror_point(block, smudges) * 100  # type: ignore  # seems to be a bug???
        # amount of vertical mirror points
        + _find_mirror_point(list(zip(*block)), smudges)  # type: ignore[arg-type]  # list cast
        for s in blocks.split("\n\n")
        if (block := s.splitlines())
    )


def part_2(blocks: str) -> int:
    """Solution for Advent of Code 2023 day 13 part 2"""
    return part_1(blocks, smudges=1)
