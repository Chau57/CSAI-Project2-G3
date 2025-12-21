from typing import List, Optional, Dict, Tuple, Set
import heapq
from collections import defaultdict
from .base_solver import BaseSolver
from .pysat_solver import PySATSolver
from core.puzzle import Puzzle

# =============================================================================
# BASE CLASS: A* FRAMEWORK ON CNF
# =============================================================================
class AStarCNFBase(BaseSolver):
    """
    Abstract base class for A* variants on CNF.
    Responsibilities:
    1. Generate CNF clauses (Encoding).
    2. Manage main A* loop.
    3. Provide utility functions (Check Satisfied, Reconstruct Solution).
    """
    def __init__(self):
        super().__init__()
        self.sat_helper = PySATSolver()
        self.clauses: List[List[int]] = []
        self.num_vars: int = 0
        self.degree_clause_indices: Set[int] = set()
        self.var_to_clauses: Dict[int, List[int]] = defaultdict(list)

    def setup(self, grid_or_puzzle):
        """
        Prepare puzzle data and generate CNF clauses.
        
        Args:
            grid_or_puzzle: Either a Puzzle object or a 2D list/array representing the grid
        """
        if isinstance(grid_or_puzzle, Puzzle):
            puzzle = grid_or_puzzle
        else:
            puzzle = Puzzle(grid_or_puzzle)
        
        self.sat_helper.puzzle = puzzle
        self.sat_helper.cnf_clauses = []
        num_edges = len(puzzle.edges)
        self.sat_helper.max_var_id = num_edges * 2
        
        # Generate different types of constraints
        self.sat_helper.generate_implication_constraints()
        self.sat_helper.generate_crossing_constraints()
        
        # Save starting position of Degree Constraints (Most important constraints)
        idx_degree = len(self.sat_helper.cnf_clauses)
        self.sat_helper.generate_degree_constraints()
        
        self.clauses = self.sat_helper.cnf_clauses
        self.num_vars = self.sat_helper.max_var_id
        
        # Mark indices of Degree Clauses
        for i in range(idx_degree, len(self.clauses)):
            self.degree_clause_indices.add(i)
            
        # Build map: Variable -> List of Clauses containing it (for fast lookup)
        self.var_to_clauses.clear()
        for i, clause in enumerate(self.clauses):
            for lit in clause:
                self.var_to_clauses[abs(lit)].append(i)

    def is_invalid(self, assignment: Dict[int, bool]) -> bool:
        """
        Check if the recent assignment violates any clauses (pruning optimization).
        
        Args:
            assignment: Dictionary mapping variable IDs to boolean values
            
        Returns:
            True if any clause is violated, False otherwise
        """
        if not assignment: return False
        # Get the last variable that was added
        last_var = list(assignment.keys())[-1]
        
        indices = self.var_to_clauses.get(last_var, [])
        for idx in indices:
            clause = self.clauses[idx]
            is_falsified = True
            
            for lit in clause:
                val = assignment.get(abs(lit), None)
                # If literal is unassigned, or this literal is True -> Clause not yet violated
                if val is None or (lit > 0 and val) or (lit < 0 and not val):
                    is_falsified = False
                    break
            
            if is_falsified: return True
        return False

    def is_satisfied(self, assignment: Dict[int, bool]) -> bool:
        """
        Check if all CNF clauses are satisfied by the current assignment.
        
        Args:
            assignment: Dictionary mapping variable IDs to boolean values
            
        Returns:
            True if all clauses are satisfied, False otherwise
        """
        for clause in self.clauses:
            sat = False
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None and ((lit > 0 and val) or (lit < 0 and not val)):
                    sat = True; break
            if not sat: return False
        return True

    def reconstruct(self, assignment: Dict[int, bool]) -> List[List[str]]:
        """
        Convert Boolean variable assignment to visual grid representation.
        
        Args:
            assignment: Dictionary mapping variable IDs to boolean values
            
        Returns:
            2D list of strings representing the solution grid
        """
        model = [v if val else -v for v, val in assignment.items()]
        state = self.sat_helper.parse_model_to_state(model)
        return self.sat_helper.render_solution(state)

    # --- FUNCTIONS TO OVERRIDE IN SUBCLASS ---
    def heuristic(self, assignment: Dict[int, bool]) -> int:
        """
        Calculate heuristic cost for the current assignment.
        
        Args:
            assignment: Dictionary mapping variable IDs to boolean values
            
        Returns:
            Heuristic cost estimate (lower is better)
        """
        return 0
    
    def select_variable(self, assignment: Dict[int, bool]) -> Optional[int]:
        """
        Select the next variable to assign.
        
        Args:
            assignment: Dictionary mapping variable IDs to boolean values
            
        Returns:
            Variable ID to assign next, or None if all variables are assigned
        """
        # Default: Select variables sequentially 1 -> N that are unassigned
        for i in range(1, self.num_vars + 1):
            if i not in assignment: return i
        return None

    def solve(self, grid) -> Optional[List[List[str]]]:
        """
        Main A* search loop.
        
        Args:
            grid: Either a Puzzle object or a 2D list/array representing the grid
            
        Returns:
            2D list of strings representing the solution, or None if no solution exists
        """
        self.setup(grid)
        start_assignment = {}
        
        # Priority Queue: (f, g, tie_breaker, assignment)
        # tie_breaker helps avoid Dict comparison errors in Python 3
        h_start = self.heuristic(start_assignment)
        pq = [(h_start, 0, 0, start_assignment)]
        tie_counter = 0

        while pq:
            f, g, _, assignment = heapq.heappop(pq)
            
            # 1. Goal Check
            if self.is_satisfied(assignment):
                return self.reconstruct(assignment)

            # 2. Variable Selection
            var = self.select_variable(assignment)
            if var is None: continue # No more variables but not satisfied (dead end)

            # 3. Branching (True/False)
            for val in [True, False]:
                new_assign = assignment.copy()
                new_assign[var] = val
                
                # 4. Pruning
                if self.is_invalid(new_assign): continue
                
                h = self.heuristic(new_assign)
                tie_counter += 1
                heapq.heappush(pq, (g + 1 + h, g + 1, tie_counter, new_assign))
                
        return None


# =============================================================================
# VARIANT 1: A* BASIC (Count unsatisfied clauses)
# =============================================================================
class AStarBasicCNF(AStarCNFBase):
    """
    Naive baseline strategy.
    - Heuristic: Count total number of unsatisfied clauses.
    - Variable selection: Sequential.
    => Used as baseline for comparison.
    """
    def __init__(self):
        super().__init__()
        self.name = "AStar_Basic"

    def heuristic(self, assignment):
        cnt = 0
        for clause in self.clauses:
            sat = False
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None and ((lit > 0 and val) or (lit < 0 and not val)):
                    sat = True; break
            if not sat: cnt += 1
        return cnt


# =============================================================================
# VARIANT 2: A* WEIGHTED (Domain knowledge weights)
# =============================================================================
class AStarWeightedCNF(AStarCNFBase):
    """
    Strategy with domain knowledge.
    - Heuristic: Heavy penalty (x10) for violating Degree Constraints (bridge count).
    - Variable selection: Sequential.
    """
    def __init__(self):
        super().__init__()
        self.name = "AStar_Weighted"

    def heuristic(self, assignment):
        score = 0
        for i, clause in enumerate(self.clauses):
            sat = False
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None and ((lit > 0 and val) or (lit < 0 and not val)):
                    sat = True; break
            
            if not sat:
                # If it's a degree constraint -> Important -> High weight
                weight = 10 if i in self.degree_clause_indices else 1
                score += weight
        return score


# =============================================================================
# VARIANT 3: A* MOMs (Maximum Occurrences in Minimum length clauses)
# =============================================================================
class AStarMomsCNF(AStarCNFBase):
    """
    SAT optimization strategy (Dynamic Variable Ordering).
    - Heuristic: Weighted + Heavy penalty for Unit Clauses (about to be violated).
    - Variable selection: Choose variable appearing most in difficult/short clauses.
    => Usually the most efficient strategy.
    """
    def __init__(self):
        super().__init__()
        self.name = "AStar_MOMs"

    def heuristic(self, assignment):
        score = 0
        for i, clause in enumerate(self.clauses):
            sat = False
            unassigned_count = 0
            
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None:
                    if (lit > 0 and val) or (lit < 0 and not val):
                        sat = True; break
                else:
                    unassigned_count += 1
            
            if not sat:
                weight = 10 if i in self.degree_clause_indices else 1
                # If clause has only 1 unassigned variable (Unit Clause) -> Extremely dangerous
                if unassigned_count == 1: 
                    weight += 20 
                score += weight
        return score

    def select_variable(self, assignment):
        # Count variable frequency in unsatisfied clauses
        counts = defaultdict(int)
        
        for i, clause in enumerate(self.clauses):
            sat = False
            unassigned_vars = []
            
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None:
                    if (lit > 0 and val) or (lit < 0 and not val):
                        sat = True; break
                else:
                    unassigned_vars.append(abs(lit))
            
            if not sat:
                # Calculate importance score of this clause
                w = 5 if i in self.degree_clause_indices else 1
                # Shorter clauses get higher priority (MOMs principle)
                if len(unassigned_vars) <= 2: 
                    w *= 5 
                
                for v in unassigned_vars:
                    counts[v] += w
        
        # If no special variable, choose first unassigned variable
        if not counts:
            for i in range(1, self.num_vars + 1):
                if i not in assignment: return i
            return None
            
        # Return variable with highest score
        return max(counts, key=counts.get)


# =============================================================================
# VARIANT 4: A* JW (Jeroslow-Wang heuristic)
# =============================================================================
class AStarJWCNF(AStarCNFBase):
    """
    Exponential weighting strategy.
    - Heuristic: Penalty based on 2^(-length). Shorter clauses get heavier penalties.
    - Variable selection: Choose variable that maximizes J(x) = Sum(2^-|C|).
    """
    def __init__(self):
        super().__init__()
        self.name = "AStar_JW"

    def heuristic(self, assignment):
        score = 0.0
        for i, clause in enumerate(self.clauses):
            sat = False
            unassigned_count = 0
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None:
                    if (lit > 0 and val) or (lit < 0 and not val):
                        sat = True; break
                else:
                    unassigned_count += 1
            
            if not sat:
                weight = 10 if i in self.degree_clause_indices else 1
                # Exponential penalty: Fewer variables -> Penalty spikes
                if unassigned_count > 0:
                    penalty = 20.0 * (0.5 ** (unassigned_count - 1))
                    score += weight * penalty
                else:
                    score += 1000 # Clause already violated (empty)
        return int(score)

    def select_variable(self, assignment):
        scores = defaultdict(float)
        
        for i, clause in enumerate(self.clauses):
            sat = False
            unassigned_vars = []
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None:
                    if (lit > 0 and val) or (lit < 0 and not val):
                        sat = True; break
                else:
                    unassigned_vars.append(abs(lit))
            
            if not sat:
                length = len(unassigned_vars)
                if length == 0: continue
                
                # J(C) = 2^(-len)
                increment = 2.0 ** (-length)
                if i in self.degree_clause_indices:
                    increment *= 5
                
                for var in unassigned_vars:
                    scores[var] += increment
        
        if not scores:
            for i in range(1, self.num_vars + 1):
                if i not in assignment: return i
            return None
            
        return max(scores, key=scores.get)