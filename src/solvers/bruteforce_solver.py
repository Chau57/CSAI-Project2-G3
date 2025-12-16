"""
Brute-force solver for Hashiwokakero.

This solver enumerates all possible bridge assignments
and checks them against the problem constraints.
"""

from typing import Dict, Optional
from itertools import product

from core.puzzle import Puzzle
from core.constraints import (
    check_degree_exact as check_degree,
    check_crossing,
    check_connected
)
from .base_solver import BaseSolver


class BruteForceSolver(BaseSolver):
    """
    Solve Hashiwokakero using brute-force search.
    """

    def solve(self, puzzle: Puzzle) -> Optional[Dict[int, int]]:
        """
        Attempt to solve the puzzle by enumerating all states.

        Parameters
        ----------
        puzzle : Puzzle
            The puzzle instance

        Returns
        -------
        Optional[Dict[int, int]]
            A valid state if found, otherwise None
        """
        num_edges = len(puzzle.edges)

        # Each edge can have 0, 1, or 2 bridges
        for assignment in product([0, 1, 2], repeat=num_edges):
            state = {i: assignment[i] for i in range(num_edges)}

            # Constraint checking
            if not check_crossing(puzzle, state):
                continue
            if not check_degree(puzzle, state):
                continue
            if not check_connected(puzzle, state):
                continue

            return state

        return None
