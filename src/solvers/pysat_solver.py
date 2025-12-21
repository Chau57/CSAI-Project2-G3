"""
PySAT-based solver for Hashiwokakero using CNF encoding (Edge-Based)

This solver uses edge-based encoding, consistent with other solvers (A*, Backtracking, BruteForce).
It leverages the Puzzle object from core/ for islands, edges, intersections, and adjacency.
"""
from typing import List, Optional, Dict, Set
from pysat.solvers import Glucose3
from pysat.card import CardEnc

from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import check_connected


class PySATSolver(BaseSolver):
    """
    Solves Hashiwokakero puzzle using SAT solver with edge-based CNF formulation.
    
    Edge-Based Encoding:
    - Each edge has 2 boolean variables:
        b1: True if edge has at least 1 bridge
        b2: True if edge has exactly 2 bridges
    - Variable ID: b1 = edge_id * 2 + 1, b2 = edge_id * 2 + 2
    
    Value mapping:
        0 bridges: b1=False, b2=False
        1 bridge:  b1=True,  b2=False
        2 bridges: b1=True,  b2=True
    
    Constraints:
    1. Implication: b2 implies b1 (¬b2 ∨ b1)
    2. Crossing: Intersecting edges cannot both have bridges
    3. Degree: Each island has exactly the required number of bridges
    4. Connectivity: All islands must be connected (checked via lazy approach)
    """
    
    def __init__(self):
        """Initialize PySAT solver"""
        super().__init__()
        self.puzzle: Optional[Puzzle] = None
        self.cnf_clauses: List[List[int]] = []
        self.max_var_id: int = 0
    
    def get_b1_var(self, edge_id: int) -> int:
        """
        Get variable ID for b1 (at least 1 bridge) of an edge.
        
        Args:
            edge_id: Edge identifier
            
        Returns:
            Unique positive integer variable ID
        """
        return edge_id * 2 + 1
    
    def get_b2_var(self, edge_id: int) -> int:
        """
        Get variable ID for b2 (exactly 2 bridges) of an edge.
        
        Args:
            edge_id: Edge identifier
            
        Returns:
            Unique positive integer variable ID
        """
        return edge_id * 2 + 2
    
    def generate_implication_constraints(self) -> None:
        """
        Generate constraints: b2 implies b1 for each edge.
        
        If an edge has 2 bridges (b2=True), it must have at least 1 bridge (b1=True).
        CNF: ¬b2 ∨ b1
        """
        for edge in self.puzzle.edges:
            b1 = self.get_b1_var(edge.id)
            b2 = self.get_b2_var(edge.id)
            # ¬b2 ∨ b1
            self.cnf_clauses.append([-b2, b1])
    
    def generate_crossing_constraints(self) -> None:
        """
        Generate crossing constraints: Intersecting edges cannot both have bridges.
        
        For each pair of intersecting edges (e1, e2):
        CNF: ¬b1[e1] ∨ ¬b1[e2]
        """
        for e1_id, e2_id in self.puzzle.intersections:
            b1_e1 = self.get_b1_var(e1_id)
            b1_e2 = self.get_b2_var(e2_id)
            # If e1 has bridges, e2 cannot have bridges (and vice versa)
            self.cnf_clauses.append([-self.get_b1_var(e1_id), -self.get_b1_var(e2_id)])
    
    def generate_degree_constraints(self) -> None:
        """
        Generate degree constraints: Each island has exactly the required number of bridges.
        
        For each island with value N:
        - Sum of bridge weights from adjacent edges must equal N
        - b1 contributes weight 1, b2 contributes weight 1 more (total 2 if both true)
        - Use CardEnc.equals for cardinality constraint
        """
        for island in self.puzzle.islands:
            # Get all edges adjacent to this island
            adjacent_edges = self.puzzle.adj[island.id]
            
            if not adjacent_edges:
                # Island with no possible edges - unsolvable if value > 0
                if island.value > 0:
                    self.cnf_clauses.append([])  # Empty clause = UNSAT
                continue
            
            # Build weighted literals
            # b1 contributes 1, b2 contributes 1 more
            # Total: 0 bridges = 0, 1 bridge = 1, 2 bridges = 2
            expanded_lits = []
            for edge in adjacent_edges:
                b1 = self.get_b1_var(edge.id)
                b2 = self.get_b2_var(edge.id)
                # b1 = 1 bridge, b2 = 1 additional bridge
                expanded_lits.append(b1)
                expanded_lits.append(b2)
            
            # Add cardinality constraint: sum = island.value
            if len(expanded_lits) > 0:
                cnf = CardEnc.equals(
                    lits=expanded_lits, 
                    bound=island.value, 
                    top_id=self.max_var_id
                )
                self.cnf_clauses.extend(cnf.clauses)
                self.max_var_id = cnf.nv
    
    def parse_model_to_state(self, model: List[int]) -> Dict[int, int]:
        """
        Parse SAT model to edge state dictionary.
        
        Args:
            model: List of variable assignments from SAT solver
            
        Returns:
            Dictionary mapping edge_id to number of bridges (0, 1, or 2)
        """
        model_set: Set[int] = set(model)
        state: Dict[int, int] = {}
        
        for edge in self.puzzle.edges:
            b1 = self.get_b1_var(edge.id)
            b2 = self.get_b2_var(edge.id)
            
            b1_true = b1 in model_set
            b2_true = b2 in model_set
            
            if b2_true:
                state[edge.id] = 2
            elif b1_true:
                state[edge.id] = 1
            else:
                state[edge.id] = 0
        
        return state
    
    def render_solution(self, state: Dict[int, int]) -> List[List[str]]:
        """
        Render edge state to solution grid.
        
        Args:
            state: Dictionary mapping edge_id to number of bridges
            
        Returns:
            2D list of strings representing the solution
        """
        # Initialize result with island numbers and zeros
        result = [[str(cell) for cell in row] for row in self.puzzle.grid]
        
        # Fill in bridge symbols
        for edge in self.puzzle.edges:
            bridges = state.get(edge.id, 0)
            if bridges > 0:
                if edge.direction == 'H':
                    symbol = '=' if bridges == 2 else '-'
                else:  # 'V'
                    symbol = '$' if bridges == 2 else '|'
                
                for r, c in edge.cells:
                    result[r][c] = symbol
        
        return result
    
    def generate_blocking_clause(self, state: Dict[int, int]) -> List[int]:
        """
        Generate a blocking clause to exclude the current solution.
        
        This is used for the lazy connectivity check - if a solution is not connected,
        we add a clause that blocks this exact assignment and search for another.
        
        Args:
            state: Current edge state to block
            
        Returns:
            Blocking clause as list of literals
        """
        clause = []
        for edge in self.puzzle.edges:
            b1 = self.get_b1_var(edge.id)
            b2 = self.get_b2_var(edge.id)
            bridges = state.get(edge.id, 0)
            
            if bridges == 0:
                # Currently false, so add positive literal to clause
                clause.append(b1)
            elif bridges == 1:
                # b1=True, b2=False -> negate: ¬b1 ∨ b2
                clause.append(-b1)
                clause.append(b2)
            else:  # bridges == 2
                # b1=True, b2=True -> negate: ¬b2
                clause.append(-b2)
        
        return clause
    
    def solve(self, grid) -> Optional[List[List[str]]]:
        """
        Solve the puzzle using PySAT with edge-based encoding.
        
        Args:
            grid: Puzzle grid (numpy array, list, or Puzzle object)
            
        Returns:
            Solution as 2D list of strings, or None if no solution
        """
        # Initialize puzzle
        if isinstance(grid, Puzzle):
            self.puzzle = grid
        else:
            self.puzzle = Puzzle(grid)
        
        # Initialize variables
        num_edges = len(self.puzzle.edges)
        self.cnf_clauses = []
        self.max_var_id = num_edges * 2  # 2 variables per edge
        
        # Generate all constraints
        self.generate_implication_constraints()
        self.generate_crossing_constraints()
        self.generate_degree_constraints()
        
        # Create SAT solver and add clauses
        solver = Glucose3()
        for clause in self.cnf_clauses:
            solver.add_clause(clause)
        
        # Solve with lazy connectivity check
        max_iterations = 1000  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            self.nodes_explored += 1
            
            if not solver.solve():
                return None
            
            model = solver.get_model()
            state = self.parse_model_to_state(model)
            
            # Check connectivity
            if check_connected(self.puzzle, state):
                return self.render_solution(state)
            
            # Not connected - add blocking clause and try again
            blocking = self.generate_blocking_clause(state)
            solver.add_clause(blocking)
        
        # Exceeded max iterations
        return None
