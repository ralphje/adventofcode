# adventofcode

These are my solutions to some Advent of Code challenges. See https://adventofcode.com/
for more information.

My goal is to create concise, yet readable solutions.

## Solutions
Solutions are present in the `solutions/` folder. Solutions take the form of functions with either
the name ``part_1`` or ``part_2`` and take a single argument. The argument must be annotated with
either ``str`` to get the full input document, or ``list[str]`` to get the input document split by
line.


## Automation
The `manage.py` script takes care of preparing, executing, testing and submitting solutions.

It is best to first set up [advent-code-of-data](https://github.com/wimglenn/advent-of-code-data)
with appriopriate session cookies to ensure that everything works as intended.

Creation of solution template and test data:
```shell
python manage.py [year] [day] create
```

Testing and executing the script (based on provided test data):
```shell
python manage.py [year] [day] run [part_1/part_2]
```

Submitting the solution (will test the result using the test data first):
```shell
python manage.py [year] [day] submit [part_1/part_2]
```


## Testing
Typically, AoC challenges will include a small verification test. Test data is provided in the
`tests/test_data/` folder in YAML files, e.g.:

```yaml
- input: test input
  part_1: result for part 1
  part_2: result for part 2
```

For executing individual challenges, see `manage.py` above.

Additional tests may be provided in the `tests/` folder. You can run this, and *all* challenge
verifications with:

```yaml
pytest
```

## AoC-data integration
You can also use the integration with [advent-code-of-data](https://github.com/wimglenn/advent-of-code-data)'s `aoc` command:

```
pip install .
aoc -y 2023 --no-submit
```

Note that you must probably reinstall after a solution change.

## Linting
You can run `black solutions tests manage.py` and `ruff check ...` for linting.
