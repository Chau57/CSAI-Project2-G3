"""
constraints.py

This module defines constraint-checking utilities for the Hashiwokakero puzzle.
These constraints are independent of any specific solving strategy and can be
shared across brute-force, backtracking, A*, and SAT-based solvers.

Each solver represents a state as:
    state: Dict[int, int]
where:
    - key   : edge_id
    - value : number of bridges on that edge (0, 1, or 2)
"""

from typing import Dict
from collections import defaultdict, deque

from .variables import Island, Edge
from .puzzle import Puzzle


def check_degree(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Check whether each island has exactly the required number of bridges.

    Args:
        puzzle (Puzzle): The Hashiwokakero puzzle instance.
        state (Dict[int, int]): Mapping from edge_id to number of bridges.

    Returns:
        bool: True if all islands satisfy their degree constraints, False otherwise.
    """
    degree = {island.id: 0 for island in puzzle.islands}

    for edge in puzzle.edges:
        bridges = state.get(edge.id, 0)
        degree[edge.u] += bridges
        degree[edge.v] += bridges

    for island in puzzle.islands:
        if degree[island.id] != island.value:
            return False

    return True


def check_crossing(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Check whether any two bridges cross each other.

    Two bridges are considered crossing if:
        - They occupy the same grid cell
        - They have different directions (horizontal vs vertical)
        - Both have at least one bridge present

    Args:
        puzzle (Puzzle): The Hashiwokakero puzzle instance.
        state (Dict[int, int]): Mapping from edge_id to number of bridges.

    Returns:
        bool: True if no crossings occur, False otherwise.
    """
    occupied = {}  # (row, col) -> direction

    for edge in puzzle.edges:
        bridges = state.get(edge.id, 0)
        if bridges == 0:
            continue

        for cell in edge.cells:
            if cell in occupied:
                if occupied[cell] != edge.direction:
                    return False
            else:
                occupied[cell] = edge.direction

    return True


def check_connected(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Check whether all islands are connected into a single connected component.

    This is done by constructing an undirected graph from the active bridges
    and performing a BFS traversal.

    Args:
        puzzle (Puzzle): The Hashiwokakero puzzle instance.
        state (Dict[int, int]): Mapping from edge_id to number of bridges.

    Returns:
        bool: True if the puzzle graph is fully connected, False otherwise.
    """
    graph = defaultdict(list)

    for edge in puzzle.edges:
        if state.get(edge.id, 0) > 0:
            graph[edge.u].append(edge.v)
            graph[edge.v].append(edge.u)

    if not graph:
        return False

    visited = set()
    queue = deque()

    start = puzzle.islands[0].id
    visited.add(start)
    queue.append(start)

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == len(puzzle.islands)
