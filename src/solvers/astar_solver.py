"""
A* Search Algorithm for Hashiwokakero
TODO: Implement by team member
"""
from typing import List, Optional
from .base_solver import BaseSolver


class AStarSolver(BaseSolver):
    """
    A* search implementation for Hashiwokakero
    
    TODO: Implement the following:
    1. Define state representation
    2. Implement heuristic function (estimated cost to goal)
    3. Implement successor generation (valid next states)
    4. Implement priority queue with f(n) = g(n) + h(n)
    5. Search for solution
    
    Suggested heuristic ideas:
    - Number of unsatisfied islands
    - Difference between required and actual bridges
    - Manhattan distance metrics
    """
    
    def __init__(self):
        """Initialize A* solver"""
        super().__init__()
    
    def solve(self, grid) -> Optional[List[List[str]]]:
        """
        Solve puzzle using A* search
        
        Args:
            grid: Puzzle grid
            
        Returns:
            Solution or None if no solution found
        """
        # TODO: Implement A* algorithm
        raise NotImplementedError(
            "A* solver not yet implemented. "
            "Please implement this solver using A* search algorithm."
        )
    
    def heuristic(self, state) -> float:
        """
        Heuristic function h(n) - estimated cost to goal
        
        TODO: Implement heuristic
        
        Args:
            state: Current puzzle state
            
        Returns:
            Estimated cost to reach goal
        """
        raise NotImplementedError("Heuristic not implemented")
    
    def get_successors(self, state):
        """
        Generate valid successor states
        
        TODO: Implement successor generation
        
        Args:
            state: Current state
            
        Returns:
            List of (successor_state, cost) tuples
        """
        raise NotImplementedError("Successor generation not implemented")
