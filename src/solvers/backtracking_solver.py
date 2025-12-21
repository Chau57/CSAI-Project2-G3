from typing import List, Optional, Dict
from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import check_degree_partial, check_crossing, check_degree_exact, check_connected

class BacktrackingSolver(BaseSolver):
    """
    Backtracking implementation using Core Puzzle & Constraints.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "BacktrackingSolver"
        self.puzzle: Optional[Puzzle] = None
        self.num_edges = 0

    def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
        """
        Solve the puzzle using backtracking search with pruning.
        
        Args:
            grid_or_puzzle: Either a Puzzle object or a 2D list/array representing the grid
            
        Returns:
            2D list of strings representing the solution, or None if no solution exists
        """
        # 1. Normalize input to Puzzle object
        if isinstance(grid_or_puzzle, Puzzle):
            self.puzzle = grid_or_puzzle
        else:
            self.puzzle = Puzzle(grid_or_puzzle)
            
        self.num_edges = len(self.puzzle.edges)
        
        # 2. Initialize empty state (Dictionary: edge_id -> bridges)
        # Initially no edges are assigned
        initial_state: Dict[int, int] = {}
        
        # 3. Run recursion
        final_state = self._backtrack(0, initial_state)
        
        if final_state:
            return self._render_solution(final_state)
        return None

    def _backtrack(self, edge_idx: int, current_state: Dict[int, int]) -> Optional[Dict[int, int]]:
        """
        Recursive backtracking helper function.
        
        Args:
            edge_idx: Index of the current edge to process
            current_state: Dictionary mapping edge_id to number of bridges
            
        Returns:
            Complete state dictionary if solution found, None otherwise
        """
        # Base case: All edges have been processed
        if edge_idx == self.num_edges:
            # Check final state (sufficient bridges + connectivity)
            if check_degree_exact(self.puzzle, current_state) and \
               check_connected(self.puzzle, current_state):
                return current_state
            return None

        # Get current edge
        edge = self.puzzle.edges[edge_idx]
        
        # Heuristic Strategy: Try connecting bridges (2, 1) first to reach goal faster
        # (Or change to [0, 1, 2] if you want exhaustive safe search)
        for val in [2, 1, 0]:
            # Try assigning value
            current_state[edge.id] = val
            
            # --- PRUNING ---
            # 1. Check Crossing\n            # Only need to check if this edge has bridges (>0)
            if val > 0:
                if not check_crossing(self.puzzle, current_state):
                    del current_state[edge.id] # Backtrack
                    continue
            
            # 2. Check Bridge count on islands (Degree) - Partial Check
            # No island is allowed to exceed its required number
            if not check_degree_partial(self.puzzle, current_state):
                del current_state[edge.id] # Backtrack
                continue
                
            # Recurse to next step
            result = self._backtrack(edge_idx + 1, current_state)
            if result:
                return result
                
            # Backtrack: Remove state to try another value
            del current_state[edge.id]
            
        return None

    def _render_solution(self, state: Dict[int, int]) -> List[List[str]]:
        """
        Convert logical state to visual grid representation.
        
        Args:
            state: Dictionary mapping edge_id to number of bridges (0, 1, or 2)
            
        Returns:
            2D list of strings representing the solution grid
        """
        # Create copy from original grid (currently numpy int array)
        result = [[str(cell) for cell in row] for row in self.puzzle.grid]
        
        for edge in self.puzzle.edges:
            bridges = state.get(edge.id, 0)
            if bridges > 0:
                symbol = ('=' if bridges == 2 else '-') if edge.direction == 'H' else \
                         ('$' if bridges == 2 else '|')
                
                for r, c in edge.cells:
                    result[r][c] = symbol
        return result