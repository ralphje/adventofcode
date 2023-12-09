import pytest

from solutions.common.strings import ints


@pytest.mark.parametrize(
    ("input", "output"),
    [
        ("", []),
        ("123", [123]),
        ("-123", [-123]),
        ("test1.3", [1, 3]),
        ("-test 1 2 test-", [1, 2]),
    ],
)
def test_ints(input, output):
    assert ints(input) == output
