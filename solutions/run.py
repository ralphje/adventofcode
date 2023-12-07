import importlib
import inspect
import pathlib
import pkgutil
from collections.abc import Callable, Iterable
from types import ModuleType
from typing import Any, cast

import yaml

import solutions


def get_solution_modules(
    year: str | int | None = None, day: str | int | None = None
) -> Iterable[ModuleType]:
    """Returns all solution modules for the given year and/or day."""

    for _, year_module_name, is_package in pkgutil.walk_packages(solutions.__path__):
        if not is_package:
            continue
        if year is not None and str(year) not in year_module_name:
            continue
        package = importlib.import_module(f"solutions.{year_module_name}")
        for _, day_module_name, _ in pkgutil.walk_packages(package.__path__):
            if day is not None and f"{day:02}" not in day_module_name:
                continue
            yield importlib.import_module(f"solutions.{year_module_name}.{day_module_name}")


def get_year_day_from_module(solution_module: ModuleType) -> tuple[str, str]:
    """Returns the year and day from the provided solution module."""

    if not solution_module.__name__.startswith("solutions."):
        raise Exception(f"Not a solution module: {solution_module.__name__}")

    _, year, day, *_ = solution_module.__name__.split(".")
    return year, day


def get_test_data_for_solution(solution_module: ModuleType) -> list[dict[str, Any]] | None:
    """Loads the provided test data for the provided solution module"""

    year, day = get_year_day_from_module(solution_module)

    path = pathlib.Path(__file__).parent.parent / "tests" / "test_data" / year / f"{day}.yaml"
    if not path.exists():
        return None

    return cast(list[dict[str, Any]], yaml.safe_load(path.open("rb")))


def run_function_in_solution(
    solution_module: ModuleType, function_name: str, data: str, *args: Any, **kwargs: Any
) -> Any:
    """Executes the named function in the provided module with the provided data."""
    function = getattr(solution_module, function_name)
    return run_function(function, data, *args, **kwargs)


def run_function(function: Callable[..., Any], data: str, *args: Any, **kwargs: Any) -> Any:
    """Executes the function with the provided data."""

    # Get the annotation of the first argument
    parameter = next(iter(inspect.signature(function).parameters.values()))
    annotation = inspect.get_annotations(function, eval_str=True)[parameter.name]

    # Execute with correct annotation
    if annotation == list[str]:
        return function(data.splitlines(), *args, **kwargs)
    elif annotation == str:
        return function(data, *args, **kwargs)
    else:
        raise Exception(f"Unknown how to execute with annotation {annotation!r}")


def aoc_entrypoint(year: int, day: int, data: str) -> tuple[Any, Any]:
    for solution_module in get_solution_modules(year, day):
        part_a = run_function_in_solution(solution_module, "part_1", data)
        part_b = run_function_in_solution(solution_module, "part_2", data)
        return part_a, part_b
    return None, None
