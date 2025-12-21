"""
Abstract Base Class for all Hashiwokakero solvers
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time


class BaseSolver(ABC):
    """
    Base class that all solvers must inherit from
    
    Provides:
    - Standard interface for solving puzzles
    - Statistics tracking (time, nodes explored, etc.)
    - Common utilities
    """
    
    def __init__(self):
        """Initialize solver"""
        self.name = self.__class__.__name__
        self.solve_time = 0.0
        self.solution_found = False
    
    @abstractmethod
    def solve(self, grid: Any) -> Optional[List[List[str]]]:
        """
        Solve the Hashiwokakero puzzle
        
        Args:
            grid: The puzzle grid (numpy array or list of lists)
            
        Returns:
            2D list of strings representing solution, or None if no solution
        """
        pass
    
    def solve_with_timing(self, grid: Any) -> Optional[List[List[str]]]:
        """
        Solve puzzle and track execution time
        
        Args:
            grid: The puzzle grid
            
        Returns:
            Solution or None
        """
        start_time = time.time()
        result = self.solve(grid)
        self.solve_time = time.time() - start_time
        self.solution_found = result is not None
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get solving statistics
        
        Returns:
            Dictionary with stats (time, nodes explored, etc.)
        """
        return {
            'solver': self.name,
            'time': self.solve_time,
            'solution_found': self.solution_found
        }
    
    def print_stats(self) -> None:
        """Print statistics to console"""
        stats = self.get_stats()
        print(f"\n=== {self.name} Statistics ===")
        print(f"Time: {stats['time']:.4f}s")
        print(f"Solution found: {stats['solution_found']}")
