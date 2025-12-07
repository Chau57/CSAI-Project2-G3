"""
Logical variable definitions for SAT encoding
"""
from typing import Tuple


class VariableManager:
    """
    Manages logical variables for SAT encoding of Hashiwokakero puzzle
    
    Variable encoding:
    - Each cell (r, c) can have 5 states (k):
        k=0: Empty (no bridge)
        k=1: Horizontal single bridge (-)
        k=2: Horizontal double bridge (=)
        k=3: Vertical single bridge (|)
        k=4: Vertical double bridge ($)
    
    Variable ID formula: (r * cols + c) * 5 + (k + 1)
    """
    
    def __init__(self, rows: int, cols: int):
        """
        Initialize variable manager
        
        Args:
            rows: Number of rows in puzzle
            cols: Number of columns in puzzle
        """
        self.rows = rows
        self.cols = cols
        self.max_var_id = rows * cols * 5
    
    def get_var_id(self, r: int, c: int, k: int) -> int:
        """
        Get variable ID for cell (r,c) in state k
        
        Args:
            r: Row index
            c: Column index
            k: State (0=Empty, 1=H-1, 2=H-2, 3=V-1, 4=V-2)
            
        Returns:
            Unique positive integer variable ID
        """
        return (r * self.cols + c) * 5 + (k + 1)
    
    def decode_var_id(self, var_id: int) -> Tuple[int, int, int]:
        """
        Decode variable ID back to (r, c, k)
        
        Args:
            var_id: Variable ID to decode
            
        Returns:
            Tuple of (row, col, state)
        """
        val = var_id - 1
        k = val % 5
        val //= 5
        c = val % self.cols
        r = val // self.cols
        return r, c, k
    
    def get_state_name(self, k: int) -> str:
        """Get human-readable name for state k"""
        names = {0: 'Empty', 1: 'H-Single', 2: 'H-Double', 3: 'V-Single', 4: 'V-Double'}
        return names.get(k, 'Unknown')
    
    def get_display_char(self, k: int) -> str:
        """Get display character for state k"""
        chars = {0: '0', 1: '-', 2: '=', 3: '|', 4: '$'}
        return chars.get(k, '?')
