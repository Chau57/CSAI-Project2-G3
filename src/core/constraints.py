"""
constraints.py

Constraint checking utilities for the Hashiwokakero puzzle.
These constraints are independent of the solving strategy and can be reused
for brute-force search, backtracking, A*, and SAT-based solvers.

State representation:
    state[edge_id] = number of bridges on that edge (0, 1, or 2).
    Missing edge_id means the edge is unassigned (partial state).

Two types of constraints are provided:
    - Exact constraints: used to validate a complete solution.
    - Partial constraints: used for early pruning during search.
"""

from typing import Dict
from collections import deque

from .puzzle import Puzzle


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _get_current_degrees(puzzle: Puzzle, state: Dict[int, int]) -> Dict[int, int]:
    """
    Compute the current degree of each island.

    The degree of an island is the total number of bridges connected to it.
    """
    degrees = {island.id: 0 for island in puzzle.islands}

    for edge in puzzle.edges:
        bridges = state.get(edge.id, 0)
        if bridges > 0:
            degrees[edge.u] += bridges
            degrees[edge.v] += bridges

    return degrees


def _is_connected_bfs(
    puzzle: Puzzle,
    state: Dict[int, int],
    strict_mode: bool
) -> bool:
    """
    Check island connectivity using BFS.

    strict_mode = True:
        Only edges with bridges (> 0) are considered connected.
        Used for final solution validation.

    strict_mode = False:
        Edges with bridges (> 0) or unassigned edges are considered connectable.
        Used for pruning partial states.
    """
    num_islands = len(puzzle.islands)
    if num_islands == 0:
        return False
    if num_islands == 1:
        return True

    adjacency = {island.id: [] for island in puzzle.islands}
    has_active_edge = False

    for edge in puzzle.edges:
        val = state.get(edge.id, 0 if strict_mode else -1)
        is_link = (val > 0) if strict_mode else (val != 0)

        if is_link:
            adjacency[edge.u].append(edge.v)
            adjacency[edge.v].append(edge.u)
            if val > 0:
                has_active_edge = True

    if strict_mode and not has_active_edge:
        return False

    start = puzzle.islands[0].id
    visited = {start}
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return len(visited) == num_islands


# =============================================================================
# PUBLIC CONSTRAINT CHECKS
# =============================================================================

def check_degree_exact(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Exact degree constraint.

    Each island must have exactly the number of bridges specified on it.
    This check is applied only to fully assigned states.
    """
    degrees = _get_current_degrees(puzzle, state)
    return all(degrees[i.id] == i.value for i in puzzle.islands)


def check_degree_partial(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Partial degree constraint for pruning.

    No island is allowed to exceed its required number of bridges.
    """
    degrees = _get_current_degrees(puzzle, state)
    return all(degrees[i.id] <= i.value for i in puzzle.islands)


def check_crossing(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Crossing constraint.

    Ensures that no two geometrically intersecting edges both contain bridges.
    """
    for e1, e2 in puzzle.intersections:
        if state.get(e1, 0) > 0 and state.get(e2, 0) > 0:
            return False
    return True


def check_connected(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Exact connectivity constraint.

    All islands must form a single connected component via active bridges.
    """
    return _is_connected_bfs(puzzle, state, strict_mode=True)


def check_connected_partial(puzzle: Puzzle, state: Dict[int, int]) -> bool:
    """
    Partial connectivity constraint for pruning.

    The current partial state must still have the potential
    to become fully connected.
    """
    return _is_connected_bfs(puzzle, state, strict_mode=False)
