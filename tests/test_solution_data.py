import importlib
import pathlib
import pkgutil

import pytest

import solutions


def _load_test_data(solution):
    """This is a method that parses data from the test_data folder for the specified solution.
    The file format consists of multiple sections, deliminated by a deliminator, and with optional
    section headers.

    The deliminator is set in the first line (excluding trailing whitespace). Every time a bare
    deliminator is found, the section is considered done and considered test input. A new section
    is started.

    Every section starts with an input block. The output blocks are indicated by the deliminator
    followed by the function name, for instance ``<deliminator> part_1``.

    If any of the blocks is a single line, the data is passed in without trailing newline. If it
    contains multiple newlines, it is passed in as-is.

    The file must end with a deliminator.

    This is a valid test file::

        ####
        input_1
        #### part_1
        output_1
        ####
    """

    test_data_file = pathlib.Path(__file__).parent / "test_data" / f"{solution}.txt"
    if not test_data_file.exists():
        return None

    with test_data_file.open("r") as f:
        deliminator = next(f).rstrip()
        collection, key = {}, "input"
        for line in f:
            if line.startswith(deliminator):
                # strip newlines if collection is only one line
                if key in collection and collection[key].count("\n") <= 1:
                    collection[key] = collection.get(key, "").strip()

                # find the instruction. if none present, start new section
                instruction = line.removeprefix(deliminator).strip()
                if not instruction:
                    if collection:
                        yield collection
                    collection, key = {}, "input"
                else:
                    key = instruction
            else:
                collection.setdefault(key, "")
                collection[key] += line


def _iter_solutions_and_test_data():
    for _, module_name, _ in pkgutil.walk_packages(solutions.__path__):
        for i, test_data in enumerate(_load_test_data(module_name)):
            test_data["__count__"] = i
            for function in test_data:
                if function not in ("input", "__count__"):
                    module = importlib.import_module(f"solutions.{module_name}")
                    yield module_name, getattr(module, function), test_data


def _idfn(val):
    if isinstance(val, dict):
        return f'test{val["__count__"]}'
    elif hasattr(val, "__module__"):
        return f"{val.__name__}"
    else:
        return val


@pytest.mark.parametrize(
    ("solution_name", "function", "test_data"), _iter_solutions_and_test_data(), ids=_idfn
)
def test_solutions(function, solution_name, test_data):
    assert str(function(test_data["input"])) == test_data[function.__name__]
