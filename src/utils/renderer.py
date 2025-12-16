"""
Render a Hashiwokakero solution state into a grid.
"""

from typing import Dict, List
from core.puzzle import Puzzle


H_SINGLE = '-'
H_DOUBLE = '='
V_SINGLE = '|'
V_DOUBLE = '$'


def render_solution(puzzle: Puzzle, state: Dict[int, int]) -> List[List[str]]:
    """
    Convert a solution state into a printable grid.

    Parameters
    ----------
    puzzle : Puzzle
        The puzzle instance
    state : Dict[int, int]
        Mapping from edge_id to number of bridges

    Returns
    -------
    List[List[str]]
        Rendered solution grid
    """
    # Start from original grid
    grid = [
        [str(puzzle.grid[r, c]) if puzzle.grid[r, c] > 0 else '0'
        for c in range(puzzle.cols)]
        for r in range(puzzle.rows)
    ]

    for edge in puzzle.edges:
        bridges = state.get(edge.id, 0)
        if bridges == 0:
            continue

        if edge.direction == 'H':
            char = H_SINGLE if bridges == 1 else H_DOUBLE
        else:
            char = V_SINGLE if bridges == 1 else V_DOUBLE

        for (r, c) in edge.cells:
            grid[r][c] = char

    return grid
