import pytest

from solutions.run import get_solution_modules, get_test_data_for_solution, run_function_in_solution


def _iter_solutions_and_test_data():
    for solution in get_solution_modules():
        for i, test_data in enumerate(get_test_data_for_solution(solution)):
            test_data["__count__"] = i
            for function in test_data:
                if function not in ("input", "__count__"):
                    yield solution, function, test_data


def _idfn(val):
    if isinstance(val, dict):
        return f'test{val["__count__"]}'
    elif hasattr(val, "__module__"):
        return f"{val.__name__}"
    else:
        return val


@pytest.mark.parametrize(
    ("solution_module", "function_name", "test_data"), _iter_solutions_and_test_data(), ids=_idfn
)
def test_solutions(function_name, solution_module, test_data):
    assert (
        run_function_in_solution(solution_module, function_name, test_data["input"])
        == test_data[function_name]
    )
