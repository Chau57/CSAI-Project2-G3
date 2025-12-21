from typing import List, Optional, Dict, Tuple, Set
import heapq
from collections import defaultdict
from .base_solver import BaseSolver
from .pysat_solver import PySATSolver
from core.puzzle import Puzzle

# =============================================================================
# BASE CLASS: KHUNG SƯỜN A* TRÊN CNF
# =============================================================================
class AStarCNFBase(BaseSolver):
    """
    Lớp cơ sở trừu tượng cho các biến thể A* trên CNF.
    Chịu trách nhiệm:
    1. Sinh mệnh đề CNF (Encoding).
    2. Quản lý vòng lặp chính của A*.
    3. Cung cấp các hàm tiện ích (Check Satisfied, Reconstruct Solution).
    """
    def __init__(self):
        super().__init__()
        self.sat_helper = PySATSolver()
        self.clauses: List[List[int]] = []
        self.num_vars: int = 0
        self.degree_clause_indices: Set[int] = set()
        self.var_to_clauses: Dict[int, List[int]] = defaultdict(list)

    def setup(self, grid_or_puzzle):
        """Chuẩn bị dữ liệu và sinh mệnh đề CNF."""
        if isinstance(grid_or_puzzle, Puzzle):
            puzzle = grid_or_puzzle
        else:
            puzzle = Puzzle(grid_or_puzzle)
        
        self.sat_helper.puzzle = puzzle
        self.sat_helper.cnf_clauses = []
        num_edges = len(puzzle.edges)
        self.sat_helper.max_var_id = num_edges * 2
        
        # Sinh các loại ràng buộc
        self.sat_helper.generate_implication_constraints()
        self.sat_helper.generate_crossing_constraints()
        
        # Lưu lại vị trí bắt đầu của Degree Constraints (Ràng buộc quan trọng nhất)
        idx_degree = len(self.sat_helper.cnf_clauses)
        self.sat_helper.generate_degree_constraints()
        
        self.clauses = self.sat_helper.cnf_clauses
        self.num_vars = self.sat_helper.max_var_id
        
        # Đánh dấu index của các Degree Clause
        for i in range(idx_degree, len(self.clauses)):
            self.degree_clause_indices.add(i)
            
        # Xây dựng map: Biến -> Danh sách Clause chứa nó (để tra cứu nhanh)
        self.var_to_clauses.clear()
        for i, clause in enumerate(self.clauses):
            for lit in clause:
                self.var_to_clauses[abs(lit)].append(i)

    def is_invalid(self, assignment: Dict[int, bool]) -> bool:
        """
        Pruning: Kiểm tra nhanh xem phép gán vừa rồi có làm sai mệnh đề nào không.
        Chỉ kiểm tra các clause liên quan đến biến vừa gán (Optimization).
        """
        if not assignment: return False
        # Lấy biến cuối cùng được thêm vào
        last_var = list(assignment.keys())[-1]
        
        indices = self.var_to_clauses.get(last_var, [])
        for idx in indices:
            clause = self.clauses[idx]
            is_falsified = True
            
            for lit in clause:
                val = assignment.get(abs(lit), None)
                # Nếu còn literal chưa gán, hoặc literal này Đúng -> Clause chưa sai
                if val is None or (lit > 0 and val) or (lit < 0 and not val):
                    is_falsified = False
                    break
            
            if is_falsified: return True
        return False

    def is_satisfied(self, assignment: Dict[int, bool]) -> bool:
        """Kiểm tra xem TẤT CẢ mệnh đề đã được thỏa mãn chưa."""
        for clause in self.clauses:
            sat = False
            for lit in clause:
                val = assignment.get(abs(lit), None)
                if val is not None and ((lit > 0 and val) or (lit < 0 and not val)):
                    sat = True; break
            if not sat: return False
        return True

    def reconstruct(self, assignment: Dict[int, bool]) -> List[List[str]]:
        """Chuyển đổi assignment Boolean về dạng lưới (Grid) hiển thị."""
        model = [v if val else -v for v, val in assignment.items()]
        state = self.sat_helper.parse_model_to_state(model)
        return self.sat_helper.render_solution(state)

    # --- CÁC HÀM CẦN OVERRIDE Ở LỚP CON ---
    def heuristic(self, assignment: Dict[int, bool]) -> int:
        return 0
    
    def select_variable(self, assignment: Dict[int, bool]) -> Optional[int]:
        # Mặc định: Chọn biến tuần tự 1 -> N chưa được gán
        for i in range(1, self.num_vars + 1):
            if i not in assignment: return i
        return None

    def solve(self, grid) -> Optional[List[List[str]]]:
        """Vòng lặp chính của thuật toán A*."""
        self.setup(grid)
        start_assignment = {}
        
        # Priority Queue: (f, g, tie_breaker, assignment)
        # tie_breaker giúp tránh lỗi so sánh Dict trong Python 3
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
            if var is None: continue # Hết biến mà chưa thỏa mãn (Dead end)

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
# VARIANT 1: A* BASIC (Đếm số clause chưa thỏa mãn)
# =============================================================================
class AStarBasicCNF(AStarCNFBase):
    """
    Chiến lược: Ngây thơ (Naive).
    - Heuristic: Đếm tổng số mệnh đề chưa thỏa mãn.
    - Chọn biến: Tuần tự.
    => Dùng để làm Baseline so sánh.
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
# VARIANT 2: A* WEIGHTED (Có trọng số Domain Knowledge)
# =============================================================================
class AStarWeightedCNF(AStarCNFBase):
    """
    Chiến lược: Có hiểu biết về bài toán (Domain Knowledge).
    - Heuristic: Phạt nặng (x10) nếu vi phạm Degree Constraints (số cầu).
    - Chọn biến: Tuần tự.
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
                # Nếu là ràng buộc số cầu -> Quan trọng -> Trọng số cao
                weight = 10 if i in self.degree_clause_indices else 1
                score += weight
        return score


# =============================================================================
# VARIANT 3: A* MOMs (Maximum Occurrences in Minimum length clauses)
# =============================================================================
class AStarMomsCNF(AStarCNFBase):
    """
    Chiến lược: Tối ưu hóa SAT (Dynamic Variable Ordering).
    - Heuristic: Weighted + Phạt cực nặng Unit Clause (sắp vi phạm).
    - Chọn biến: Chọn biến xuất hiện nhiều nhất trong các mệnh đề khó/ngắn.
    => Đây thường là chiến lược hiệu quả nhất.
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
                # Nếu clause chỉ còn 1 biến chưa gán (Unit Clause) -> Cực kỳ nguy hiểm
                if unassigned_count == 1: 
                    weight += 20 
                score += weight
        return score

    def select_variable(self, assignment):
        # Đếm tần suất biến trong các clause chưa thỏa mãn
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
                # Tính điểm quan trọng của clause này
                w = 5 if i in self.degree_clause_indices else 1
                # Clause càng ngắn càng ưu tiên xử lý (MOMs principle)
                if len(unassigned_vars) <= 2: 
                    w *= 5 
                
                for v in unassigned_vars:
                    counts[v] += w
        
        # Nếu không còn biến nào đặc biệt, chọn biến chưa gán đầu tiên
        if not counts:
            for i in range(1, self.num_vars + 1):
                if i not in assignment: return i
            return None
            
        # Trả về biến có điểm cao nhất
        return max(counts, key=counts.get)

    """
    Chiến lược: Tính trọng số theo hàm mũ (Exponential Weighting).
    - Heuristic: Phạt dựa trên 2^(-length). Clause càng ngắn phạt càng đau.
    - Chọn biến: Chọn biến maximize J(x) = Sum(2^-|C|).
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
                # Phạt hàm mũ: Còn ít biến -> Phạt tăng vọt
                if unassigned_count > 0:
                    penalty = 20.0 * (0.5 ** (unassigned_count - 1))
                    score += weight * penalty
                else:
                    score += 1000 # Clause đã vi phạm (empty)
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