"""This file holds the solutions for Advent of Code 2023 day 17: Clumsy Crucible
https://adventofcode.com/2023/day/17
"""

import collections
import heapq
import math

# directions (x, y)
S = (0, +1)
E = (+1, 0)


def directional_dijkstra(grid: list[str], min_dist: int = 1, max_dist: int = 3) -> int:
    """This adjusted Dijkstra algorithm takes each node and the direction we've used to get there,
    to consider every node it can reach with the limitations in the challenge (not going in the
    same direction we used to get here and the min/max_dist).

    Basically, each node is unique for its coordinates AND the direction-to-get-there, as it
    depends on this direction which nodes are reachable.
    """

    max_x, max_y = len(grid[0]), len(grid)
    costs: dict[tuple[tuple[int, int], tuple[int, int]], float] = collections.defaultdict(
        lambda: math.inf
    )

    # Create a heap, that keeps track of the cost to get here, the coordinates we are currently,
    # and the direction we used to get here. We start in the upper right corner. Assume we came
    # from S or E, so we consider W and N, respectively.
    heap = [(0, (0, 0), S), (0, (0, 0), E)]
    while heap:
        # Pop something off the heap. Since this is a heap operation, so we always fetch the
        # smallest element first. That ensures that we have the cheapest position to get here.
        cost, coordinate, direction = heapq.heappop(heap)
        # If we are where we need to be, simply return the cost. Since heapq ensures that this is
        # the smallest cost, this is true!
        if coordinate == (max_x - 1, max_y - 1):
            return cost
        # Once we pop from the heap, the costs dict may have changed, so by checking here we can
        # short-circuit if a new option has arisen
        if cost > costs[coordinate, direction]:
            continue

        # Assume we are going in a new direction. This ensures that N/S -> E/W, and E/W -> N/S
        for new_direction in ((-direction[1], direction[0]), (direction[1], -direction[0])):
            # new_cost keep track on the cost it takes to get into our new direction
            new_cost = cost
            # Iterate up to the acceptable distances to go into this direction. This includes
            # min_dist, as we need to add up the cost to get there as well.
            for distance in range(1, max_dist + 1):
                # Get the next coordinate in this direction
                next_x, next_y = (
                    coordinate[0] + new_direction[0] * distance,
                    coordinate[1] + new_direction[1] * distance,
                )
                # Some bounds checking. We can simply break here, since we know we will be
                # checking only further out of bounds.
                if not (0 <= next_x < max_x and 0 <= next_y < max_y):
                    break

                # Calculate the new_cost
                new_cost += int(grid[next_y][next_x])

                # Assert min_dist (after new_cost addition)
                if distance < min_dist:
                    continue

                # If the calculated cost is higher than the cost we have already seen, consider
                # this an invalid move. Doing this here (and not just at the start) saves a
                # bit of time.
                if new_cost >= costs[(next_x, next_y), new_direction]:
                    continue
                # Otherwise, we know for sure that this is a cheaper option. Store the cost and
                # consider it in the next phase.
                costs[(next_x, next_y), new_direction] = new_cost
                heapq.heappush(heap, (new_cost, (next_x, next_y), new_direction))

    raise AssertionError("unreachable")


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 17 part 1"""
    return directional_dijkstra(lines)


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 17 part 2"""
    return directional_dijkstra(lines, 4, 10)
