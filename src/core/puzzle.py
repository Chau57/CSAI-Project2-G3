"""
Puzzle class for Hashiwokakero
"""
from typing import List, Tuple
import numpy as np


class Puzzle:
    """
    Represents a Hashiwokakero puzzle
    
    Attributes:
        grid: 2D array where islands are represented by numbers (1-8), empty cells by 0
        rows: Number of rows in the grid
        cols: Number of columns in the grid
    """
    
    def __init__(self, grid: np.ndarray):
        """
        Initialize puzzle from grid
        
        Args:
            grid: 2D numpy array representing the puzzle
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
    
    def is_island(self, r: int, c: int) -> bool:
        """Check if position (r,c) is an island"""
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] > 0
    
    def is_empty(self, r: int, c: int) -> bool:
        """Check if position (r,c) is empty"""
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 0
    
    def get_islands(self) -> List[Tuple[int, int, int]]:
        """
        Get all islands in the puzzle
        
        Returns:
            List of tuples (row, col, value)
        """
        islands = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0:
                    islands.append((r, c, self.grid[r][c]))
        return islands
    
    def __str__(self) -> str:
        """String representation of the puzzle"""
        lines = []
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                val = self.grid[r][c]
                row_str.append(str(val))
            lines.append(" ".join(row_str))
        return "\n".join(lines)
