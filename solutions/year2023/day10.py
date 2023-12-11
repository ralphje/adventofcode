"""This file holds the solutions for Advent of Code 2023 day 10: Pipe Maze
https://adventofcode.com/2023/day/10
"""

from collections.abc import Iterable

from solutions.common.iter import count

type Direction = tuple[int, int]
type Coordinate = tuple[int, int]

N = (0, -1)
S = (0, +1)
E = (+1, 0)
W = (-1, 0)

PIPES = {
    "|": (N, S),
    "-": (E, W),
    "L": (N, E),
    "J": (N, W),
    "7": (S, W),
    "F": (S, E),
    "S": (N, W, S, E),
}


def _start_node(board: list[str]) -> Coordinate:
    """Returns the starting node on the board"""
    for y, row in enumerate(board):
        if (x := row.find("S")) != -1:
            return x, y
    raise AssertionError("unreachable")


def _possible_directions(
    board: list[str], position: Coordinate
) -> Iterable[tuple[Direction, Coordinate]]:
    """Returns the possible directions from a given position."""

    # The bounds of the board (exclusive)
    max_x, max_y = len(board[0]), len(board)

    # The board[position[1]][position[0]] returns the current pipe piece
    # The PIPES map returns the possible directions you can go from the given pipe piece.
    for direction in PIPES[board[position[1]][position[0]]]:
        # Direction is a possible direction offset, so dir_x, dir_y will
        # be the coordinates of the direction from our current position
        dir_x, dir_y = (
            position[0] + direction[0],
            position[1] + direction[1],
        )
        # Bounds check
        if not (0 <= dir_x < max_x and 0 <= dir_y < max_y):
            continue

        # Check that the possible coordinate allows us to get back to the current node as well.
        # This is mostly necessary for the start node (only), but it works any way.
        if (-direction[0], -direction[1]) in PIPES.get(board[dir_y][dir_x], ()):
            yield direction, (dir_x, dir_y)


def _walk(board: list[str], start_node: Coordinate) -> Iterable[Coordinate]:
    """Walk across the board in a circle, starting from the given node, stopping as soon as
    we've hit the same node again.
    """

    current_node, previous_node = start_node, None
    while True:
        for _, next_node in _possible_directions(board, current_node):
            if next_node != previous_node:
                yield next_node
                previous_node, current_node = current_node, next_node
                break  # break the possible directions loop, not the outer loop

        # stop the cycle when we've reached the start_node again
        if start_node == current_node:
            break


def part_1(board: list[str]) -> int:
    """Solution for Advent of Code 2023 day 10 part 1"""

    # Divide by two to get the point furthest from start
    return count(_walk(board, _start_node(board))) // 2


def _correct_pipe(board: list[str], position: Coordinate) -> str:
    """Determines the pipe for the given position. Used to correct the starting node."""
    return next(
        pipe
        for pipe, pipe_dirs in PIPES.items()
        if all(d in pipe_dirs for d, _ in _possible_directions(board, position))
    )


def part_2(board: list[str]) -> int:
    """Solution for Advent of Code 2023 day 10 part 2"""

    # Note, in this file 3 lines have been commented out with ###. These can be uncommented for a
    # visual solution.

    loop = list(_walk(board, _start_node(board)))
    result = 0
    # We start outside the pipe loop
    outside = True
    for y, row in enumerate(board):
        for x, pipe in enumerate(row):
            # If we are not on the loop, we can simply replace whatever is here with a O or I
            if (x, y) not in loop:
                if not outside:
                    result += 1
                ### board[y] = offset_replace(board[y], x, "O" if outside else "I")
                continue

            if pipe == "S":
                # Ensure that we use the correct pipe on the starting location
                pipe = _correct_pipe(board, (x, y))

            # We can simply check whether we encounter any N (or, similarly, any S) in the
            # pipe's directions. If we meet a | (N->S) we are always passing from the outside to
            # the inside, or vice versa. If we encounter two corner pieces, with an odd number of
            # N's, such as L7 or FJ, we effectively passed a pipe, so we also flip. Conversely,
            # when we encounter two corner pieces with 0 or 2 N's, we have not passed beyond the
            # pipe and do not enter/exit the inside of the loop (even number of flips == no flips).
            if N in PIPES[pipe]:
                outside = not outside

    ### [print(b) for b in board]

    return result  ### sum(b.count("I") for b in board)
