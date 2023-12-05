from __future__ import annotations

import functools
import itertools
from collections.abc import Iterable
from typing import Self


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

    def __and__(self, other: Self) -> Self:
        """Returns the intersection of both ranges."""
        start = max(self.start, other.start)
        end = min(self.stop, other.stop)
        length = end - start
        if length > 0:
            return Range(start, length)
        return Range(0, 0)

    def __add__(self, other: int) -> Self:
        """Adds the integer to this range."""
        return Range(self.start + other, len(self))

    def __sub__(self, other: int) -> Self:
        """Subtracts the integer to this range."""
        return Range(self.start - other, len(self))

    def cut(self, other: Self) -> list[Self]:
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
            if (split := tuple(map(int, line.split())))
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
    """The almanac (your puzzle input) lists all of the seeds that need to be planted. It also
    lists what type of soil to use with each kind of seed, what type of fertilizer to use with
    each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every
    type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused
    by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each
    other.

    For example::

        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4

    The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

    The rest of the almanac contains a list of maps which describe how to convert numbers from a
    source category into numbers in a destination category. That is, the section that starts with
    seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the
    destination). This lets the gardener and his team know which soil to use with which seeds,
    which water to use with which fertilizer, and so on.

    Rather than list every source number and its corresponding destination number one by one, the
    maps describe entire ranges of numbers that can be converted. Each line within a map contains
    three numbers: the destination range start, the source range start, and the range length.

    Consider again the example seed-to-soil map::

        50 98 2
        52 50 48
    The first line has a destination range start of 50, a source range start of 98, and a range
    length of 2. This line means that the source range starts at 98 and contains two values: 98
    and 99. The destination range is the same length, but it starts at 50, so its two values are
    50 and 51. With this information, you know that seed number 98 corresponds to soil number 50
    and that seed number 99 corresponds to soil number 51.

    The second line means that the source range starts at 50 and contains 48 values: 50, 51, ...,
    96, 97. This corresponds to a destination range starting at 52 and also containing 48 values:
    52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

    Any source numbers that aren't mapped correspond to the same destination number. So, seed
    number 10 corresponds to soil number 10.

    So, the entire list of seed numbers and their corresponding soil numbers looks like this::

        seed  soil
        0     0
        1     1
        ...   ...
        48    48
        49    49
        50    52
        51    53
        ...   ...
        96    98
        97    99
        98    50
        99    51

    With this map, you can look up the soil number required for each initial seed number::

        Seed number 79 corresponds to soil number 81.
        Seed number 14 corresponds to soil number 14.
        Seed number 55 corresponds to soil number 57.
        Seed number 13 corresponds to soil number 13.

    The gardener and his team want to get started as soon as possible, so they'd like to know the
    closest location that needs a seed. Using these maps, find the lowest location number that
    corresponds to any of the initial seeds. To do this, you'll need to convert each seed number
    through other categories until you can find its corresponding location number. In this example
    the corresponding types are:

    * Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    * Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    * Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    * Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

    So, the lowest location number in this example is 35.

    What is the lowest location number that corresponds to any of the initial seed numbers?
    """

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
        for seed in map(int, sections[0].split(": ")[1].split())
    )


def part_2(document: str) -> int:
    """Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac,
    it looks like the seeds: line actually describes ranges of seed numbers.

    The values on the initial seeds: line come in pairs. Within each pair, the first value is the
    start of the range and the second value is the length of the range. So, in the first line of
    the example above::

        seeds: 79 14 55 13

    This line describes two ranges of seed numbers to be planted in the garden. The first range
    starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts
    with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

    Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

    In the above example, the lowest location number can be obtained from seed number 82, which
    corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and
    location 46. So, the lowest location number is 46.

    Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
    What is the lowest location number that corresponds to any of the initial seed numbers?
    """

    # Simply start by collection all sections by splitting on double newline.
    sections = document.split("\n\n")

    # Make use of the fact that all mappings in the document appear in order.
    mappings = _parse_mappings(sections)

    # Collect seed ranges as if they are mapping items, with an offset of 0.
    seed_ranges = [
        MappingItem(Range(seed_start, seed_size))
        for seed_start, seed_size in itertools.batched(
            map(int, sections[0].split(": ")[1].split()), 2
        )
    ]

    # Iterate over each mapping and calculate our source/target ranges, generating a new
    # list of seed_ranges every time.
    for mapping in mappings:
        new_values = []
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
        for seed_start, seed_size in itertools.batched(
            map(int, sections[0].split(": ")[1].split()), 2
        )
        for seed in range(seed_start, seed_start + seed_size)
    )
