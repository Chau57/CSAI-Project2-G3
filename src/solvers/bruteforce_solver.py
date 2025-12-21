from typing import List, Optional, Dict
from itertools import product
from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import (
    check_degree_exact,
    check_crossing,
    check_connected
)

class BruteForceSolver(BaseSolver):
    """
    Solve Hashiwokakero using brute-force search.
    Enumerates all possible bridge assignments.
    """

    def __init__(self):
        super().__init__()
        self.name = "BruteForceSolver" # Required for creating output directory

    def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
        """
        Solve the puzzle by enumerating all possible bridge assignments.
        
        Args:
            grid_or_puzzle: Either a Puzzle object or a 2D list/array representing the grid
            
        Returns:
            2D list of strings representing the solution, or None if no solution exists
        """
        # 1. NORMALIZE INPUT (List -> Puzzle)
        if isinstance(grid_or_puzzle, Puzzle):
            puzzle = grid_or_puzzle
        else:
            puzzle = Puzzle(grid_or_puzzle)

        num_edges = len(puzzle.edges)
        
        # Warning if number of edges is too large (since 3^N grows exponentially)
        if num_edges > 15:
            print(f"  [Warning] BruteForce: {num_edges} edges -> 3^{num_edges} states. This will be slow!")

        # 2. BRUTE FORCE SEARCH
        # Each edge can have 0, 1, or 2 bridges
        for assignment in product([0, 1, 2], repeat=num_edges):
            # Create state dict: {edge_id: num_bridges}
            state = {i: assignment[i] for i in range(num_edges)}

            # Constraint checking
            # Check crossing first as it violates basic physical rules
            if not check_crossing(puzzle, state):
                continue
            
            # Check correct number of bridges on each island
            if not check_degree_exact(puzzle, state):
                continue
            
            # Check connectivity (if problem requires strict validation)
            if not check_connected(puzzle, state):
                continue

            # 3. RENDER OUTPUT (Dict -> Grid String)
            return self._render_solution(puzzle, state)

        return None

    def _render_solution(self, puzzle: Puzzle, state: Dict[int, int]) -> List[List[str]]:
        """
        Convert numeric state to character grid representation.
        
        Args:
            puzzle: The Puzzle object containing grid and edge information
            state: Dictionary mapping edge_id to number of bridges (0, 1, or 2)
            
        Returns:
            2D list of strings representing the solution grid
        """
        # Copy original grid
        result = [[str(cell) for cell in row] for row in puzzle.grid]
        
        for edge in puzzle.edges:
            bridges = state.get(edge.id, 0)
            if bridges > 0:
                # Choose symbol based on direction and number of bridges
                if edge.direction == 'H':
                    symbol = '=' if bridges == 2 else '-'
                else:
                    symbol = '$' if bridges == 2 else '|'
                
                # Fill in cells between two islands
                for r, c in edge.cells:
                    result[r][c] = symbol
        return result