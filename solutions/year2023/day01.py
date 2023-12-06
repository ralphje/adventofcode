def part_1(lines: list[str]) -> int:
    """The newly-improved calibration document consists of lines of text; each line originally
    contained a specific calibration value that the Elves now need to recover. On each line, the
    calibration value can be found by combining the first digit and the last digit (in that order)
    to form a single two-digit number.

    For example::

        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet

    In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding
    these together produces 142.

    Consider your entire calibration document. What is the sum of all of the calibration values?
    """

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
    """Your calculation isn't quite right. It looks like some of the digits are actually spelled
    out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid
    "digits".

    Equipped with this new information, you now need to find the real first and last digit on each
    line. For example::

        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen

    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these
    together produces 281.

    What is the sum of all of the calibration values?
    """

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
