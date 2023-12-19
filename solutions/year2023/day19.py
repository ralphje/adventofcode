"""This file holds the solutions for Advent of Code 2023 day 19: Aplenty
https://adventofcode.com/2023/day/19
"""

import math
import re
from collections.abc import Iterator
from typing import Literal

from solutions.common.strings import ints

type Condition = tuple[str, Literal[">", "<"], int]
type Rule = tuple[Condition | None, str]
type Workflow = dict[str, list[Rule]]

RULE_RE = re.compile(r"([a-z]+)\{(.*)}")


def _parse_workflow(workflow: str) -> Workflow:
    """This parses the rules to be handleable by Python.

        ex{x>10:one,m<20:two,a>30:R,A}

    Becomes::

        {'ex': [
            (('x', '>', 10), 'one'),
            (('m', '<', 20), 'two'),
            (('a', '>', 30), 'R'),
            (None, 'A')
        ]}
    """

    return {
        # rule_re[0] is the name
        rule_re[0]: [
            (
                # If the length of parts is 1, this is the catch-all condition
                (None, condition_split[0])
                if len(condition_split) == 1
                else
                # Otherwise, this is not a catch-all condition
                (
                    (condition_split[0][0], condition_split[0][1], int(condition_split[0][2:])),
                    condition_split[1],
                )
            )
            # rule_re[1] is the part between the brackets
            for condition in rule_re[1].split(",")
            if (condition_split := condition.split(":"))
        ]
        for rule in workflow.splitlines()
        if (rule_re := RULE_RE.findall(rule)[0])
    }


def _parse_parts(parts: str) -> list[dict[str, int]]:
    """Returns the parts from the input"""
    return [dict(zip("xmas", ints(part))) for part in parts.splitlines()]


def _parse_input(lines: str) -> tuple[Workflow, list[dict[str, int]]]:
    """Parses the input from today's puzzle"""
    w, p = lines.split("\n\n")
    return _parse_workflow(w), _parse_parts(p)


def _compare_rule(part: dict[str, int], rule: Rule) -> str | None:
    """Compares a single rule against the part. Returns str for next target, or None if
    not matched.
    """
    condition, destination = rule

    if condition is None:
        return destination
    else:
        key, operation, value = condition
        if (operation == "<" and part[key] < value) or (operation == ">" and part[key] > value):
            return destination

    return None


def accept_part(part: dict[str, int], workflow: Workflow) -> bool:
    """Returns True or False for a given part and workflow."""

    rules = workflow["in"]
    while True:
        for rule in rules:
            if result := _compare_rule(part, rule):
                if result in ("A", "R"):
                    return result == "A"
                rules = workflow[result]
                break  # stop checking rules, continue the while loop


def part_1(lines: str) -> int:
    """Solution for Advent of Code 2023 day 19 part 1"""
    workflow, parts = _parse_input(lines)

    return sum(sum(part.values()) for part in parts if accept_part(part, workflow))


def add_range(ranges: dict[str, range], condition: Condition) -> dict[str, range]:
    """Applies the given condition to the provided ranges, and returns a new dict
    We consider the range as far as we have it now, and limit it further down to what is possible.
    """

    key, operation, value = condition
    # Note that the stop is exclusive, and the start is inclusive.
    if operation == "<":
        return ranges | {key: range(ranges[key].start, value)}
    elif operation == ">":
        return ranges | {key: range(value + 1, ranges[key].stop)}


def remove_range(ranges: dict[str, range], condition: Condition) -> dict[str, range]:
    """Removes the given condition to the provided ranges, and returns a new dict"""

    key, operation, value = condition
    # Note that the stop is exclusive, and the start is inclusive.
    if operation == "<":
        return ranges | {key: range(value, ranges[key].stop)}
    elif operation == ">":
        return ranges | {key: range(ranges[key].start, value + 1)}


# We start with a state of: consider rule 'IN' and everything is possible
# (4000 + 1 as its including)
_INITIAL_STATE = {r: range(1, 4001) for r in "xmas"}


def possible_paths(
    workflow: Workflow,
    rule_name: str = "in",
    ranges: dict[str, range] = _INITIAL_STATE,
) -> Iterator[dict[str, range]]:
    """Consider all possible paths from the given state.

    The state represents the workflow rule we are currently parsing, and the range limitations
    we currently have.
    """
    for condition, destination in workflow[rule_name]:
        if condition is None:
            # We have reached a final state in this workflow rule. We keep the ranges as-is
            # and consider the rules as if they are in a positive state -- there is no negative
            # state.
            rules_true = ranges
        else:
            # If we hit a condition, we consider both what happens when the condition is true
            # (see below with rules_true) and what happens when the condition is false, and iterate
            # further down the line.
            rules_true = add_range(ranges, condition)
            ranges = remove_range(ranges, condition)

        # Now we consider the positive state, the negative state will be handled by the for-loop.
        if destination == "A":
            # If we reach destination "A", we are in luck, as we now have a valid path
            yield rules_true
        elif destination != "R":
            # If we reach destination "R", this is an invalid path and ignore.
            # Otherwise, we now continue to the next destination with our positive path.
            yield from possible_paths(workflow, destination, rules_true)


def part_2(lines: str) -> int:
    """Solution for Advent of Code 2023 day 19 part 2"""
    workflow, parts = _parse_input(lines)

    # Now simply take the product of all ranges in all positive paths
    return sum(math.prod(map(len, path.values())) for path in possible_paths(workflow))
