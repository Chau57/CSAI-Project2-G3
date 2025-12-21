from typing import List, Optional, Tuple, Dict
import heapq
from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import check_degree_partial, check_crossing, check_degree_exact, check_connected

class AStarSolver(BaseSolver):
    """
    A* Solver using Core modules.
    State: Tuple of assignments for edges determined so far.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "AStarSolver"
        self.puzzle: Optional[Puzzle] = None

    def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
        """
        Solve the puzzle using A* search algorithm.
        
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
            
        num_edges = len(self.puzzle.edges)
        
        # Priority Queue: (f, g, edge_idx, state_tuple)
        # state_tuple: tuple containing values (0,1,2) for edges processed so far
        # Using tuple for hashing and storage in visited set
        initial_state = ()
        initial_h = self.heuristic(initial_state)
        
        pq = [(0 + initial_h, 0, 0, initial_state)]
        visited = set()
        
        while pq:
            f, g, idx, current_tuple = heapq.heappop(pq)
            
            # Base case: All edges have been processed
            if idx == num_edges:
                # Convert tuple to dict to check final constraints
                final_state_dict = {i: val for i, val in enumerate(current_tuple)}
                if check_degree_exact(self.puzzle, final_state_dict) and \
                   check_connected(self.puzzle, final_state_dict):
                    return self._render_solution(final_state_dict)
                continue
            
            # Visited Check
            if current_tuple in visited:
                continue
            visited.add(current_tuple)
            
            # Expand Successors (0, 1, 2)
            edge = self.puzzle.edges[idx]
            
            for val in [2, 1, 0]:
                # Create temporary state as Dict for constraint checking (for convenience)
                # Note: Only need to check constraints related to the newly added edge
                temp_state_dict = {i: v for i, v in enumerate(current_tuple)}
                temp_state_dict[idx] = val
                
                # --- PRUNING ---
                valid = True
                if val > 0:
                    # Crossing check is expensive but necessary
                    if not check_crossing(self.puzzle, temp_state_dict):
                        valid = False
                
                if valid:
                    if not check_degree_partial(self.puzzle, temp_state_dict):
                        valid = False
                
                if valid:
                    new_tuple = current_tuple + (val,)
                    new_g = g + 1
                    new_h = self.heuristic(new_tuple)
                    
                    heapq.heappush(pq, (new_g + new_h, new_g, idx + 1, new_tuple))
                    
        return None

    def heuristic(self, state_tuple: Tuple[int, ...]) -> float:
        """
        Calculate heuristic cost: total number of missing bridges for all islands.
        
        Args:
            state_tuple: Tuple of bridge assignments for edges processed so far
            
        Returns:
            Heuristic cost (float). Returns infinity if constraints are violated.
        """
        # Calculate current bridge count for each island based on assigned state
        current_degrees = {island.id: 0 for island in self.puzzle.islands}
        
        for edge_idx, val in enumerate(state_tuple):
            if val > 0:
                edge = self.puzzle.edges[edge_idx]
                current_degrees[edge.u] += val
                current_degrees[edge.v] += val
                
        # Calculate cost
        h_score = 0
        for island in self.puzzle.islands:
            diff = island.value - current_degrees[island.id]
            if diff < 0:
                return float('inf') # Heavy penalty if already exceeded
            h_score += diff
            
        return h_score

    def _render_solution(self, state_dict: Dict[int, int]) -> List[List[str]]:
        """
        Convert logical state to visual grid representation.
        
        Args:
            state_dict: Dictionary mapping edge_id to number of bridges (0, 1, or 2)
            
        Returns:
            2D list of strings representing the solution grid
        """
        # (Rendering code identical to Backtracking, copied for convenience)
        result = [[str(cell) for cell in row] for row in self.puzzle.grid]
        for edge in self.puzzle.edges:
            bridges = state_dict.get(edge.id, 0)
            if bridges > 0:
                symbol = ('=' if bridges == 2 else '-') if edge.direction == 'H' else \
                         ('$' if bridges == 2 else '|')
                for r, c in edge.cells:
                    result[r][c] = symbol
        return result

