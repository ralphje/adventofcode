import argparse
import pathlib
import sys
import textwrap
from typing import Any

from aocd.models import Puzzle  # type: ignore[import-untyped]

from solutions.run import get_solution_modules, get_test_data_for_solution, run_function_in_solution


def error(msg: str) -> None:
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


def create(args: Any) -> None:
    create_solution_file(args)
    create_test_data(args)


def create_solution_file(args: Any) -> None:
    solutions_dir = pathlib.Path(__file__).parent / "solutions"

    year_dir = solutions_dir / f"year{args.year:04}"
    if not year_dir.exists():
        year_dir.mkdir()
        (year_dir / "__init__.py").touch()

    day_file = year_dir / f"day{args.day:02}.py"
    if day_file.exists():
        error(
            f"solution file for {args.year:04} - {args.day:02} already exists, not overwriting to"
            " prevent data loss (even if --force is present)"
        )
        return

    with day_file.open("w") as f:
        f.write(
            "def part_1(document: str) -> int:\n    pass\n\n"
            "def part_2(document: str) -> int:\n    pass\n"
        )


def create_test_data(args: Any) -> None:
    test_dir = pathlib.Path(__file__).parent / "tests" / "test_data"

    year_dir = test_dir / f"year{args.year:04}"
    if not year_dir.exists():
        year_dir.mkdir()

    day_file = year_dir / f"day{args.day:02}.yaml"
    if day_file.exists() and not args.force:
        error(
            f"test data for {args.year:04} - {args.day:02} already exists, use --force to fetch"
            " again"
        )
        return

    try:
        puzzle = Puzzle(year=args.year, day=args.day)
    except Exception as e:
        error(f"could not fetch test data for {args.year:04} - {args.day:02}: {e}")
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


def run_test(solution_module: Any, function_name: str) -> bool:
    result = True
    test_datas = get_test_data_for_solution(solution_module)
    if not test_datas:
        return True

    for i, test_data in enumerate(test_datas):
        if args.challenge not in test_data:
            continue
        print(f"Running test data {i} in {function_name}:")
        expect = test_data[args.challenge]
        result = run_function_in_solution(solution_module, args.challenge, test_data["input"])
        print("Expect:", expect)
        print("Result:", result)
        if expect != result:
            result = False

    return result


def run_challenge(args: Any, solution_module: Any, function_name: str) -> Any:
    try:
        puzzle = Puzzle(year=args.year, day=args.day)
    except Exception as e:
        error(f"could not fetch test data for {args.year:04} - {args.day:02}: {e}")
        return
    else:
        print(f"Running challenge data in {args.challenge}:")
        if function_name == "part_1" and puzzle.answered_a:
            print("Answer:", puzzle.answer_a)
        elif function_name == "part_2" and puzzle.answered_b:
            print("Answer:", puzzle.answer_b)

        result = run_function_in_solution(solution_module, function_name, puzzle.input_data)
        print("Result:", result)

    return result


def run(args: Any) -> None:
    solution_modules = get_solution_modules(args.year, args.day)
    for solution_module in solution_modules:
        if args.input == "test":
            result = run_test(solution_module, args.challenge)
            if not result:
                print("Test FAILED")
            else:
                print("Test SUCCEEDED")

        elif args.input == "challenge":
            run_challenge(args, solution_module, args.challenge)


def submit(args: Any) -> None:
    solution_modules = get_solution_modules(args.year, args.day)
    for solution_module in solution_modules:
        result = run_test(solution_module, args.challenge)
        if not result and not args.force:
            error("Test did not succeed. Cannot submit!")
            return

        result = run_challenge(args, solution_module, args.challenge)

        # submit result?
        puzzle = Puzzle(year=args.year, day=args.day)
        if args.challenge == "part_1":
            puzzle.answer_a = result
        elif args.challenge == "part_2":
            puzzle.answer_b = result


VALID_PARTS = ["part_1", "part_2", "1", "2", "a", "b"]


def _convert_part(input: str) -> str:
    if input in ["part_1", "1", "a"]:
        return "part_1"
    if input in ["part_2", "2", "b"]:
        return "part_2"
    return input


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Helper for setting up and managing AoC solutions."
    )
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
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
