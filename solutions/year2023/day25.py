"""This file holds the solutions for Advent of Code 2023 day 25: Snowverload
https://adventofcode.com/2023/day/25
"""

import collections


def _make_graph(lines: list[str]) -> dict[str, set[str]]:
    """Build a graph, with nodes going to other nodes."""
    graph = collections.defaultdict(set)
    for line in lines:
        node_from, rest = line.split(": ")
        for node_to in rest.split(" "):
            graph[node_from].add(node_to)
            graph[node_to].add(node_from)
    return graph


def make_subgraph(graph: dict[str, set[str]], start: str) -> set[str]:
    """Creates a subgraph by adding nodes from a random starting node, and stopping as soon as
    we only have 3 edges to the rest of the graph.

    This problem asks for the Stoer-Wagner algorithm, but this works. Note that this may result in
    an error, but at least one starting node should work.
    """

    # We start with the subgraph from a random starting node
    subgraph = {start}
    while True:
        # Calculate all outgoing edges from the subgraph to the rest of the graph
        edges = {(start, end) for start in subgraph for end in graph[start] if end not in subgraph}

        # If we have 3 or fewer edges with the rest of the graph, we are done.
        if len(edges) <= 3:
            break

        # Add new node, choosing from the current subgraph's neighbours the one with the highest
        # amount of edges inside the subgraph, to prioritize the addition of nodes that are most
        # connected inside the subgraph.
        subgraph.add(
            max(
                {edge[1] for edge in edges},
                key=lambda node: sum(int(n in subgraph) for n in graph[node]),
            )
        )

    if len(subgraph) == len(graph):
        raise ValueError("Could not determine subgraph from this starting node!")

    return subgraph


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 25 part 1"""
    graph = _make_graph(lines)

    # Grab any starting point, and check if we can make a subgraph from there.
    for start in graph:
        try:
            subgraph = make_subgraph(graph, start)
        except ValueError:
            continue
        break
    else:
        raise AssertionError("unreachable")

    return len(subgraph) * (len(graph) - len(subgraph))
