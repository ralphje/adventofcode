import argparse
import datetime
import os
import pathlib
import platform
import sys
import textwrap
from typing import Any

from aocd.models import Puzzle  # type: ignore[import-untyped]

from solutions.run import get_solution_modules, get_test_data_for_solution, run_function_in_solution


def error(msg: str) -> None:
    sys.stderr.write(colored(f"{msg}\n", "red"))
    sys.stderr.flush()


if platform.system() == "Windows":
    os.system("color")  # hack - makes ANSI colors work in the windows cmd window


def colored(txt, color):
    if color is None:
        return txt
    code = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ].index(color.casefold())
    reset = "\x1b[0m"
    return f"\x1b[{code + 30}m{txt}{reset}"


def create(args: Any) -> None:
    create_solution_file(args)
    create_test_data(args)


def create_solution_file(args: Any) -> None:
    year, day = args.year_day
    solutions_dir = pathlib.Path(__file__).parent / "solutions"

    year_dir = solutions_dir / f"year{year:04}"
    if not year_dir.exists():
        year_dir.mkdir()
        (year_dir / "__init__.py").touch()

    day_file = year_dir / f"day{day:02}.py"
    if day_file.exists():
        error(
            f"{day_file} already exists, not overwriting to"
            " prevent data loss (even if --force is present)"
        )
        return

    with day_file.open("w") as f:
        f.write(
            "def part_1(document: str) -> int:\n    pass\n\n\n"
            "def part_2(document: str) -> int:\n    pass\n"
        )
    print(colored(f"Created challenge file in {day_file}", "green"))


def create_test_data(args: Any) -> None:
    year, day = args.year_day
    test_dir = pathlib.Path(__file__).parent / "tests" / "test_data"

    year_dir = test_dir / f"year{year:04}"
    if not year_dir.exists():
        year_dir.mkdir()

    day_file = year_dir / f"day{day:02}.yaml"
    if day_file.exists() and not args.force:
        error(f"{day_file} with test data already exists, use --force to fetch again")
        return

    try:
        puzzle = Puzzle(year=year, day=day)
    except Exception as e:
        error(f"Could not fetch test data for {year:04}/{day:02}: {e}")
        day_file.touch()
    else:
        with day_file.open("w") as f:
            for example in puzzle.examples:
                f.write(f"- input: |\n{textwrap.indent(example.input_data, '    ')}\n")
                if example.answer_a:
                    f.write(f"  part_1: {example.answer_a}\n")
                if example.answer_b:
                    f.write(f"  part_2: {example.answer_b}\n")
                if example.extra:
                    f.write(textwrap.indent(example.extra, "  # ") + "\n")
    print(colored(f"Created test data in {day_file}", "green"))


def run_test(solution_module: Any, function_name: str) -> bool:
    total_result = True
    test_datas = get_test_data_for_solution(solution_module)
    if not test_datas:
        return True

    for i, test_data in enumerate(test_datas):
        if args.challenge not in test_data:
            continue
        print(f"Running test data {i} in {solution_module.__name__}.{function_name}:")
        expect = test_data[args.challenge]
        result = run_function_in_solution(solution_module, args.challenge, test_data["input"])
        if expect == result:
            print(f"{colored('✔', 'green')} {expect}")
        else:
            print(f"{colored('✖', 'red')} {result} (expected: {expect})")
            total_result = False

    return total_result


def run_challenge(args: Any, solution_module: Any, function_name: str) -> Any:
    year, day = args.year_day
    try:
        puzzle = Puzzle(year=year, day=day)
    except Exception as e:
        error(f"could not fetch test data for {year:04}/{day:02}: {e}")
        return
    else:
        print(f"Running challenge data in {solution_module.__name__}.{args.challenge}:")
        if function_name == "part_1" and puzzle.answered_a:
            expect = puzzle.answer_a
        elif function_name == "part_2" and puzzle.answered_b:
            expect = puzzle.answer_b
        else:
            expect = None

        result = run_function_in_solution(solution_module, function_name, puzzle.input_data)
        if expect is None:
            print(f"{colored('?', 'magenta')} {result}")
        elif expect == str(result):
            print(f"{colored('✔', 'green')} {expect}")
        else:
            print(f"{colored('✖', 'red')} {result} (expected: {expect})")

    return result


def run(args: Any) -> None:
    solution_modules = get_solution_modules(*args.year_day)
    for solution_module in solution_modules:
        if args.input == "test":
            run_test(solution_module, args.challenge)
        elif args.input == "challenge":
            run_challenge(args, solution_module, args.challenge)


def submit(args: Any) -> None:
    year, day = args.year_day
    solution_modules = get_solution_modules(year, day)
    for solution_module in solution_modules:
        result = run_test(solution_module, args.challenge)
        if not result and not args.force:
            error("Test did not succeed. Cannot submit!")
            return

        result = run_challenge(args, solution_module, args.challenge)

        # submit result?
        puzzle = Puzzle(year=year, day=day)
        if args.challenge == "part_1":
            puzzle.answer_a = result
        elif args.challenge == "part_2":
            puzzle.answer_b = result


PARTS_1 = ["part_1", "1", "a"]
PARTS_2 = ["part_2", "2", "b"]
VALID_PARTS = PARTS_1 + PARTS_2


def _convert_part(input: str) -> str:
    if input in PARTS_1:
        return "part_1"
    if input in PARTS_2:
        return "part_2"
    return input


def _convert_year_day(input: str) -> tuple[int, int]:
    if input == "today":
        today = datetime.date.today()
        if today.month != 12 or today.day >= 26:
            raise ValueError("Invalid date format")
        return today.year, today.day

    year, day = map(int, input.split("/", 1))
    return year, day


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Helper for setting up and managing AoC solutions."
    )
    parser.add_argument(
        "year_day",
        type=_convert_year_day,
        help="The year/day for the challenge. Can also be the string 'today'.",
    )
    subparsers = parser.add_subparsers(required=True)

    parser_create = subparsers.add_parser("create", help="Creates the challenge files")
    parser_create.add_argument("--force", action="store_true")
    parser_create.set_defaults(func=create)

    parser_run = subparsers.add_parser("run", help="Execute challenge")
    parser_run.add_argument("challenge", choices=VALID_PARTS, type=_convert_part)
    parser_run.add_argument("input", choices=["test", "challenge"], default="test", nargs="?")
    parser_run.set_defaults(func=run)

    parser_submit = subparsers.add_parser("submit", help="Submit challenge")
    parser_submit.add_argument("challenge", choices=VALID_PARTS, type=_convert_part)
    parser_submit.add_argument("--force", action="store_true")
    parser_submit.set_defaults(func=submit)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.func(args)
