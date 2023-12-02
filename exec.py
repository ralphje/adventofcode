import argparse
import importlib
import pathlib
import pkgutil
import sys

import solutions


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "module",
        choices=[module_name for _, module_name, _ in pkgutil.walk_packages(solutions.__path__)],
        help="The solution module to execute.",
    )
    parser.add_argument("function", help="The solution function to execute.")
    parser.add_argument("--file", type=pathlib.Path, help="The path to the input file.")

    return parser.parse_args()


def main():
    args = parse_args()
    module = importlib.import_module(f"solutions.{args.module}")
    function = getattr(module, args.function, None)

    if function is None:
        sys.stderr.write(f"{args.function} is not a function of solution module {args.module}")
        sys.exit(-1)

    arguments = []
    display_arguments = []

    if args.file:
        if not args.file.exists():
            sys.stderr.write(f"{args.file} does not exist")
            sys.exit(-1)

        arguments.append(args.file.read_text())
        display_arguments.append(arguments[-1][:5] + "...")

    sys.stderr.write(
        f"## Calling {function.__module__}.{function.__name__} "
        f"with arguments {display_arguments!r}\n"
    )
    sys.stdout.write(str(function(*arguments)))


if __name__ == "__main__":
    main()
