from solutions.day02 import _parse_document


def test_parse_document():
    assert (
        dict(
            _parse_document(
                """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
            )
        )
        == {
            1: [{"blue": 3, "red": 4}, {"blue": 6, "green": 2, "red": 1}, {"green": 2}],
            2: [
                {"blue": 1, "green": 2},
                {"blue": 4, "green": 3, "red": 1},
                {"blue": 1, "green": 1},
            ],
            3: [
                {"blue": 6, "green": 8, "red": 20},
                {"blue": 5, "green": 13, "red": 4},
                {"green": 5, "red": 1},
            ],
            4: [
                {"blue": 6, "green": 1, "red": 3},
                {"green": 3, "red": 6},
                {"blue": 15, "green": 3, "red": 14},
            ],
            5: [{"blue": 1, "green": 3, "red": 6}, {"blue": 2, "green": 2, "red": 1}],
        }
    )
