"""
PySAT-based solver for Hashiwokakero using CNF encoding
"""
from typing import List, Optional
import numpy as np
from pysat.solvers import Glucose3
from pysat.card import CardEnc

from .base_solver import BaseSolver


class PySATSolver(BaseSolver):
    """
    Solves Hashiwokakero puzzle using SAT solver with CNF formulation
    
    Encoding:
    - Each cell (r,c) has 5 possible states (k):
        k=0: Empty, k=1: H-Single, k=2: H-Double, k=3: V-Single, k=4: V-Double
    - Variable ID: (r * cols + c) * 5 + (k + 1)
    
    Constraints:
    1. Cell constraints: Each cell has exactly one state
    2. Flow constraints: Bridges must connect properly
    3. Island constraints: Each island must have correct number of bridges
    """
    
    def __init__(self):
        """Initialize PySAT solver"""
        super().__init__()
        self.grid = None
        self.rows = 0
        self.cols = 0
        self.cnf_clauses = []
        self.max_var_id = 0
    
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
    
    def decode_var_id(self, var_id: int) -> tuple:
        """
        Decode variable ID back to (r, c, k)
        
        Args:
            var_id: Variable ID
            
        Returns:
            Tuple of (row, col, state)
        """
        val = var_id - 1
        k = val % 5
        val //= 5
        c = val % self.cols
        r = val // self.cols
        return r, c, k
    
    def generate_cell_constraints(self) -> None:
        """
        Generate constraints: Each non-island cell has exactly one state
        
        For each empty cell:
        1. At least one state is true: (X0 v X1 v X2 v X3 v X4)
        2. At most one state is true: (-Xi v -Xj) for all i<j
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0:  # Skip islands
                    continue
                
                # At least one state
                vars = [self.get_var_id(r, c, k) for k in range(5)]
                self.cnf_clauses.append(vars)
                
                # At most one state
                for i in range(5):
                    for j in range(i + 1, 5):
                        self.cnf_clauses.append([-vars[i], -vars[j]])
    
    def generate_flow_constraints(self) -> None:
        """
        Generate flow constraints: Bridges must connect properly
        
        If a cell has a horizontal bridge, its neighbors must also have horizontal bridges
        If a cell has a vertical bridge, its neighbors must also have vertical bridges
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0:  # Skip islands
                    continue
                
                # Horizontal bridges (k=1, k=2)
                for k in [1, 2]:
                    curr_var = self.get_var_id(r, c, k)
                    
                    # Check right neighbor
                    if c + 1 < self.cols:
                        if self.grid[r][c+1] == 0:  # Empty cell
                            next_var = self.get_var_id(r, c+1, k)
                            self.cnf_clauses.append([-curr_var, next_var])
                    else:
                        # At border -> forbidden
                        self.cnf_clauses.append([-curr_var])
                    
                    # Check left neighbor
                    if c - 1 >= 0:
                        if self.grid[r][c-1] == 0:  # Empty cell
                            prev_var = self.get_var_id(r, c-1, k)
                            self.cnf_clauses.append([-curr_var, prev_var])
                    else:
                        # At border -> forbidden
                        self.cnf_clauses.append([-curr_var])
                
                # Vertical bridges (k=3, k=4)
                for k in [3, 4]:
                    curr_var = self.get_var_id(r, c, k)
                    
                    # Check down neighbor
                    if r + 1 < self.rows:
                        if self.grid[r+1][c] == 0:
                            next_var = self.get_var_id(r+1, c, k)
                            self.cnf_clauses.append([-curr_var, next_var])
                    else:
                        self.cnf_clauses.append([-curr_var])
                    
                    # Check up neighbor
                    if r - 1 >= 0:
                        if self.grid[r-1][c] == 0:
                            prev_var = self.get_var_id(r-1, c, k)
                            self.cnf_clauses.append([-curr_var, prev_var])
                    else:
                        self.cnf_clauses.append([-curr_var])
    
    def generate_island_constraints(self) -> None:
        """
        Generate island constraints: Each island must have correct number of bridges
        
        For each island with value N:
        - Sum of bridge weights from adjacent cells must equal N
        - Single bridge = weight 1, Double bridge = weight 2
        - Use CardEnc.equals for cardinality constraint
        """
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                if val == 0:  # Not an island
                    continue
                
                bridge_vars = []
                
                # North neighbor
                if r > 0 and self.grid[r-1][c] == 0:
                    bridge_vars.append((self.get_var_id(r-1, c, 3), 1))  # V-1
                    bridge_vars.append((self.get_var_id(r-1, c, 4), 2))  # V-2
                
                # South neighbor
                if r + 1 < self.rows and self.grid[r+1][c] == 0:
                    bridge_vars.append((self.get_var_id(r+1, c, 3), 1))  # V-1
                    bridge_vars.append((self.get_var_id(r+1, c, 4), 2))  # V-2
                
                # West neighbor
                if c > 0 and self.grid[r][c-1] == 0:
                    bridge_vars.append((self.get_var_id(r, c-1, 1), 1))  # H-1
                    bridge_vars.append((self.get_var_id(r, c-1, 2), 2))  # H-2
                
                # East neighbor
                if c + 1 < self.cols and self.grid[r][c+1] == 0:
                    bridge_vars.append((self.get_var_id(r, c+1, 1), 1))  # H-1
                    bridge_vars.append((self.get_var_id(r, c+1, 2), 2))  # H-2
                
                # Expand variables by weight for cardinality encoding
                expanded_lits = []
                for var_id, weight in bridge_vars:
                    for _ in range(weight):
                        expanded_lits.append(var_id)
                
                # Add cardinality constraint: sum = val
                if len(expanded_lits) > 0:
                    cnf = CardEnc.equals(lits=expanded_lits, bound=val, top_id=self.max_var_id)
                    self.cnf_clauses.extend(cnf.clauses)
                    self.max_var_id = cnf.nv
    
    def parse_model(self, model: List[int]) -> List[List[str]]:
        """
        Parse SAT model to solution grid
        
        Args:
            model: List of variable assignments from SAT solver
            
        Returns:
            2D list of strings representing the solution
        """
        # Initialize result with island numbers
        result = [[str(self.grid[r][c]) if self.grid[r][c] != 0 else "0" 
                   for c in range(self.cols)] for r in range(self.rows)]
        
        # Map state to display character
        char_map = {0: '0', 1: '-', 2: '=', 3: '|', 4: '$'}
        
        # Process positive variables
        for var in model:
            if var > 0 and var <= self.rows * self.cols * 5:
                r, c, k = self.decode_var_id(var)
                
                # Only update empty cells
                if self.grid[r][c] == 0:
                    result[r][c] = char_map[k]
        
        return result
    
    def solve(self, grid) -> Optional[List[List[str]]]:
        """
        Solve the puzzle using PySAT
        
        Args:
            grid: Puzzle grid (numpy array or list)
            
        Returns:
            Solution as 2D list of strings, or None if no solution
        """
        # Convert to numpy array if needed
        if isinstance(grid, list):
            self.grid = np.array(grid, dtype=int)
        else:
            self.grid = grid
        
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        self.cnf_clauses = []
        self.max_var_id = self.rows * self.cols * 5
        
        # Generate all constraints
        self.generate_cell_constraints()
        self.generate_flow_constraints()
        self.generate_island_constraints()
        
        # Solve using SAT solver
        solver = Glucose3()
        for clause in self.cnf_clauses:
            solver.add_clause(clause)
        
        if solver.solve():
            model = solver.get_model()
            return self.parse_model(model)
        else:
            return None
