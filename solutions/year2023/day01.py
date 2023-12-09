"""This file holds the solutions for Advent of Code 2023 day 1: Trebuchet?!
https://adventofcode.com/2023/day/1
"""


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 1 part 1"""

    # Bit of abuse of the walrus operator here, but it works ;)
    return sum(
        int(f"{line_digits[0]}{line_digits[-1]}")
        for line in lines
        if (line_digits := [c for c in line if c.isdigit()])
    )


TEXT_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 1 part 2"""

    all_digits = []
    for line in lines:
        line_digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                line_digits.append(int(c))
            else:
                for text_digit, value in TEXT_DIGITS.items():
                    if line[i:].startswith(text_digit):
                        line_digits.append(value)
                        break

        all_digits.append(int(f"{line_digits[0]}{line_digits[-1]}"))
    return sum(all_digits)
