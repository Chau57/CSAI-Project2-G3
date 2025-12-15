"""
Brute Force Algorithm for Hashiwokakero
TODO: Implement by team member
"""
from typing import List, Optional
from .base_solver import BaseSolver


class BruteforceSolver(BaseSolver):
    """
    Brute force implementation for Hashiwokakero
    
    TODO: Implement the following:
    1. Generate all possible assignments
    2. Check each assignment against constraints
    3. Return first valid solution
    
    Warning: This approach has exponential time complexity!
    For a grid with N empty cells and 5 possible states each,
    there are 5^N possible assignments to check.
    
    Use only for small puzzles or for comparison purposes.
    """
    
    def __init__(self):
        """Initialize brute force solver"""
        super().__init__()
    
    def solve(self, grid) -> Optional[List[List[str]]]:
        """
        Solve puzzle using brute force
        
        Args:
            grid: Puzzle grid
            
        Returns:
            Solution or None if no solution found
        """
        # TODO: Implement brute force algorithm
        raise NotImplementedError(
            "Brute force solver not yet implemented. "
            "Please implement this solver using exhaustive search."
        )
    
    def generate_all_assignments(self, empty_cells):
        """
        Generate all possible assignments for empty cells
        
        TODO: Implement assignment generation
        
        Args:
            empty_cells: List of empty cell positions
            
        Yields:
            Complete assignments (one at a time to save memory)
        """
        raise NotImplementedError("Assignment generation not implemented")
    
    def check_solution(self, grid, assignment) -> bool:
        """
        Check if an assignment is a valid solution
        
        TODO: Implement solution checking
        
        Args:
            grid: Original puzzle grid
            assignment: Cell assignments to check
            
        Returns:
            True if valid solution, False otherwise
        """
        raise NotImplementedError("Solution checking not implemented")
