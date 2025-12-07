"""
Backtracking Algorithm for Hashiwokakero
TODO: Implement by team member
"""
from typing import List, Optional
from .base_solver import BaseSolver


class BacktrackingSolver(BaseSolver):
    """
    Backtracking implementation for Hashiwokakero
    
    TODO: Implement the following:
    1. Define variable ordering (which cell to fill next)
    2. Implement constraint checking
    3. Implement backtracking with pruning
    4. Add forward checking for efficiency
    
    Constraint Satisfaction Problem (CSP) approach:
    - Variables: Each empty cell
    - Domain: {Empty, H-Single, H-Double, V-Single, V-Double}
    - Constraints: Flow constraints, Island constraints
    """
    
    def __init__(self):
        """Initialize backtracking solver"""
        super().__init__()
    
    def solve(self, grid) -> Optional[List[List[str]]]:
        """
        Solve puzzle using backtracking
        
        Args:
            grid: Puzzle grid
            
        Returns:
            Solution or None if no solution found
        """
        # TODO: Implement backtracking algorithm
        raise NotImplementedError(
            "Backtracking solver not yet implemented. "
            "Please implement this solver using backtracking algorithm."
        )
    
    def is_valid(self, assignment) -> bool:
        """
        Check if current assignment is valid
        
        TODO: Implement constraint checking
        
        Args:
            assignment: Current variable assignments
            
        Returns:
            True if valid, False otherwise
        """
        raise NotImplementedError("Constraint checking not implemented")
    
    def select_unassigned_variable(self, assignment):
        """
        Select next variable to assign (heuristic)
        
        TODO: Implement variable selection
        Suggestions: Most constrained variable (MRV), degree heuristic
        
        Args:
            assignment: Current assignments
            
        Returns:
            Next variable to assign
        """
        raise NotImplementedError("Variable selection not implemented")
