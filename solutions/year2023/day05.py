"""This file holds the solutions for Advent of Code 2023 day 5: If You Give A Seed A Fertilizer
https://adventofcode.com/2023/day/5
"""

from __future__ import annotations

import functools
import itertools
from collections.abc import Iterable
from typing import Self

from solutions.common.strings import ints


class Range:
    """A range with some additional options."""

    __slots__ = ["start", "stop"]

    def __init__(self, start: int, size: int) -> None:
        """Note, this constructor is different from range(start, stop)"""

        self.start = start
        self.stop = start + size

    def __len__(self) -> int:
        """Return the length of this range."""
        return self.stop - self.start

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.start!r}, {len(self)})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.start!r}..{self.stop!r})"

    def __hash__(self) -> int:
        return hash((self.start, self.stop))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.stop == other.stop
            and (self.start == other.start or self.stop == 0)
        )

    def __contains__(self, item: int) -> bool:
        return self.start <= item < self.stop

    def __and__(self, other: Range) -> Range:
        """Returns the intersection of both ranges."""
        start = max(self.start, other.start)
        end = min(self.stop, other.stop)
        length = end - start
        if length > 0:
            return Range(start, length)
        return Range(0, 0)

    def __add__(self, other: int) -> Range:
        """Adds the integer to this range."""
        return Range(self.start + other, len(self))

    def __sub__(self, other: int) -> Range:
        """Subtracts the integer to this range."""
        return Range(self.start - other, len(self))

    def cut(self, other: Self) -> list[Range]:
        """Cuts away the provided range, and returns 0, 1 or 2 ranges at either end of the cut."""
        difference = []
        if self.start < other.start:
            difference.append(Range(self.start, other.start - self.start))
        if self.stop > other.stop:
            difference.append(Range(other.stop, self.stop - other.stop))
        return difference


class MappingItem:
    """A mapping of a certain range to a different range."""

    __slots__ = ["range", "difference"]

    def __init__(self, range: Range, difference: int = 0) -> None:
        self.range = range
        self.difference = difference

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.range!r}, {self.difference!r})"

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.range} =={self.difference!r}=> {self.target_range})"
        )

    def __hash__(self) -> int:
        return hash((self.range, self.difference))

    @property
    def source_range(self) -> Range:
        return self.range

    @property
    def target_range(self) -> Range:
        return self.range + self.difference


def _parse_mappings(sections: list[str]) -> list[list[MappingItem]]:
    """Parse the provided mapping sections (including seeds and including section titles)
    and convert it into a list of lists of mappings.

    Mappings take the form of (range, difference) tuples.
    The list of mappings is guaranteed to be sorted by range.
    """
    return [
        [
            # (range(source, source + size), destination - size)
            MappingItem(Range(split[1], split[2]), split[0] - split[1])
            # And add the ranges to the Mapping object, skipping the mapping title.
            for line in section.splitlines()[1:]
            # Line is "destination source size"
            if (split := ints(line))
        ]
        # Split on each section, skipping the first one (the seeds)
        for section in sections[1:]
    ]


def _convert_value(value: int, mapping: list[MappingItem]) -> int:
    """Naively convert the provided value to the correct value, by stepping through all
    mappings and checking whether it is in the source range.
    """
    for mapping_item in mapping:
        if value in mapping_item.source_range:
            return value + mapping_item.difference
    # Return raw value if no range is found
    return value


def _convert_range(range: MappingItem, mapping: list[MappingItem]) -> Iterable[MappingItem]:
    """Given a mapping and a provided range (mapping), will provide an iterable of all ranges and
    their targets.

    In other words:
        in:  MappingItem(x -> y)
        out: [MappingItem(x -> a), MappingItem(x -> b)]
    """

    for mapping_item in mapping:
        # This will calculate a range with the overlap of the two ranges in the mapping and the
        # provided range.
        overlap = range.target_range & mapping_item.source_range

        if overlap:
            # For the overlap, we can simply yield it with the new difference
            # Note that the overlap is in target_range, and we work with source_ranges
            # so we adjust by subtracting the difference
            yield MappingItem(
                overlap - range.difference, range.difference + mapping_item.difference
            )

            # Now we need to see what we do about the remainder of the items if we cut away this
            # overlap. Note again, we cut away from the target_range, but we need to work with
            # source ranges.
            for remainder in range.target_range.cut(mapping_item.source_range):
                yield from _convert_range(
                    MappingItem(remainder - range.difference, range.difference), mapping
                )
            return

    # Found nothing that would change this mapping
    yield range


def part_1(document: str) -> int:
    """Solution for Advent of Code 2023 day 5 part 1"""

    # Simply start by collection all sections by splitting on double newline.
    sections = document.split("\n\n")

    # Make use of the fact that all mappings in the document appear in order.
    mappings = _parse_mappings(sections)

    # Grab the seeds from the first section (split on ": ", then on all numbers) and find the
    # minimum value if we apply all mappings.
    return min(
        functools.reduce(
            _convert_value,
            mappings,
            seed,
        )
        for seed in ints(sections[0])
    )


def part_2(document: str) -> int:
    """Solution for Advent of Code 2023 day 5 part 2"""

    # Simply start by collection all sections by splitting on double newline.
    sections = document.split("\n\n")

    # Make use of the fact that all mappings in the document appear in order.
    mappings = _parse_mappings(sections)

    # Collect seed ranges as if they are mapping items, with an offset of 0.
    seed_ranges = [
        MappingItem(Range(seed_start, seed_size))
        for seed_start, seed_size in itertools.batched(ints(sections[0]), 2)
    ]

    # Iterate over each mapping and calculate our source/target ranges, generating a new
    # list of seed_ranges every time.
    for mapping in mappings:
        new_values: list[MappingItem] = []
        for seed_range in seed_ranges:
            new_values.extend(_convert_range(seed_range, mapping))
        seed_ranges = new_values

    return min(seed_range.target_range.start for seed_range in seed_ranges)


def part_2_naive(document: str) -> int:
    """Naive brute-force method for part 2. Does work, although extremely slowly."""

    # Simply start by collection all sections by splitting on double newline.
    sections = document.split("\n\n")

    # Make use of the fact that all mappings in the document appear in order.
    mappings = _parse_mappings(sections)

    return min(
        functools.reduce(
            _convert_value,
            mappings,
            seed,
        )
        for seed_start, seed_size in itertools.batched(ints(sections[0]), 2)
        for seed in range(seed_start, seed_start + seed_size)
    )
