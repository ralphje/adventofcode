# adventofcode2023

These are my solutions to some Advent of Code 2023 challenges. See https://adventofcode.com/2023
for more information.

My goal is to create concise, yet readable solutions.

## Solutions
Solutions are present in the `solutions/` folder. They can simply be executed by using the `exec.py`
script included in the root. Example execution is as follows:

```
python exec.py day01 part_1 --file input.txt
```

## Testing
Typically, AoC challenges will include a small verification test. These are present in the
`tests/` folder. Tests are typically written into the `test_data` folder.

The structure in this folder is described in `tests/test_solution_data.py`. In summary, the files
have this structure:

```
####
first test data
for both functions
#### part_1
result data for part_1
#### part_2
result data for part_2
####
second test data
#### part_2
result data for part_2
####
```

Additional tests may be provided in the `tests/` folder, for instance if this format does not
suffice.

Executing these tests can be done with:

```
pytest
```

## Linting
You can run `black solutions tests exec.py` and `ruff check ...` for linting.
