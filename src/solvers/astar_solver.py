from typing import List, Optional, Tuple, Dict
import heapq
from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import check_degree_partial, check_crossing, check_degree_exact, check_connected

class AStarSolver(BaseSolver):
    """
    A* Solver using Core modules.
    State: Tuple of assignments for edges determined so far.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "AStarSolver"
        self.puzzle: Optional[Puzzle] = None

    def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
        # 1. Chuẩn hóa Input
        if isinstance(grid_or_puzzle, Puzzle):
            self.puzzle = grid_or_puzzle
        else:
            self.puzzle = Puzzle(grid_or_puzzle)
            
        num_edges = len(self.puzzle.edges)
        
        # Priority Queue: (f, g, edge_idx, state_tuple)
        # state_tuple: tuple chứa các giá trị (0,1,2) cho các cạnh đã duyệt
        # Dùng tuple để có thể hash và lưu vào visited set
        initial_state = ()
        initial_h = self.heuristic(initial_state)
        
        pq = [(0 + initial_h, 0, 0, initial_state)]
        visited = set()
        
        while pq:
            f, g, idx, current_tuple = heapq.heappop(pq)
            
            # Base case: Đã duyệt xong hết cạnh
            if idx == num_edges:
                # Convert tuple sang dict để check constraints cuối cùng
                final_state_dict = {i: val for i, val in enumerate(current_tuple)}
                if check_degree_exact(self.puzzle, final_state_dict) and \
                   check_connected(self.puzzle, final_state_dict):
                    return self._render_solution(final_state_dict)
                continue
            
            # Visited Check
            if current_tuple in visited:
                continue
            visited.add(current_tuple)
            
            # Expand Successors (0, 1, 2)
            edge = self.puzzle.edges[idx]
            
            for val in [2, 1, 0]:
                # Tạo state tạm thời dạng Dict để check constraints (cho tiện)
                # Lưu ý: Chỉ cần check các constraints liên quan đến cạnh mới thêm
                temp_state_dict = {i: v for i, v in enumerate(current_tuple)}
                temp_state_dict[idx] = val
                
                # --- PRUNING ---
                valid = True
                if val > 0:
                    # Check crossing tốn chi phí, nhưng cần thiết
                    if not check_crossing(self.puzzle, temp_state_dict):
                        valid = False
                
                if valid:
                    if not check_degree_partial(self.puzzle, temp_state_dict):
                        valid = False
                
                if valid:
                    new_tuple = current_tuple + (val,)
                    new_g = g + 1
                    new_h = self.heuristic(new_tuple)
                    
                    heapq.heappush(pq, (new_g + new_h, new_g, idx + 1, new_tuple))
                    
        return None

    def heuristic(self, state_tuple: Tuple[int, ...]) -> float:
        """
        Heuristic: Tổng số cầu còn thiếu của tất cả các đảo.
        """
        # Tính số cầu hiện tại của các đảo dựa trên state đã gán
        current_degrees = {island.id: 0 for island in self.puzzle.islands}
        
        for edge_idx, val in enumerate(state_tuple):
            if val > 0:
                edge = self.puzzle.edges[edge_idx]
                current_degrees[edge.u] += val
                current_degrees[edge.v] += val
                
        # Tính Cost
        h_score = 0
        for island in self.puzzle.islands:
            diff = island.value - current_degrees[island.id]
            if diff < 0:
                return float('inf') # Phạt cực nặng nếu đã vượt quá
            h_score += diff
            
        return h_score

    def _render_solution(self, state_dict: Dict[int, int]) -> List[List[str]]:
        # (Code render giống hệt Backtracking, copy lại cho gọn)
        result = [[str(cell) for cell in row] for row in self.puzzle.grid]
        for edge in self.puzzle.edges:
            bridges = state_dict.get(edge.id, 0)
            if bridges > 0:
                symbol = ('=' if bridges == 2 else '-') if edge.direction == 'H' else \
                         ('$' if bridges == 2 else '|')
                for r, c in edge.cells:
                    result[r][c] = symbol
        return result


# from typing import List, Optional, Dict, Tuple, Set
# import heapq
# from collections import defaultdict
# from .base_solver import BaseSolver
# from .pysat_solver import PySATSolver
# from core.puzzle import Puzzle

# class AStarSolver(BaseSolver):
#     """
#     [A* ON CNF - OPTIMIZED HEURISTIC & VARIABLE ORDERING]
#     Cải tiến:
#     1. Weighted Heuristic: Ưu tiên thỏa mãn các ràng buộc quan trọng (Degree).
#     2. Dynamic Variable Ordering (MOM-like): Chọn biến có ảnh hưởng lớn nhất để gán trước.
#     """
    
#     def __init__(self):
#         super().__init__()
#         self.name = "AStarSolver" 
#         self.sat_helper = PySATSolver()
#         self.clauses: List[List[int]] = []
#         self.num_vars: int = 0
        
#         # Lưu index của các clause quan trọng (Degree constraints)
#         self.degree_clause_indices: Set[int] = set()
        
#         # Map: Biến -> Danh sách các clause chứa biến đó (để tra cứu nhanh)
#         self.var_to_clauses: Dict[int, List[int]] = defaultdict(list)

#     def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
#         # --- 1. SETUP & ENCODING ---
#         if isinstance(grid_or_puzzle, Puzzle):
#             puzzle = grid_or_puzzle
#         else:
#             puzzle = Puzzle(grid_or_puzzle)
            
#         self.sat_helper.puzzle = puzzle
#         self.sat_helper.cnf_clauses = []
#         num_edges = len(puzzle.edges)
#         self.sat_helper.max_var_id = num_edges * 2
        
#         # Sinh ràng buộc
#         # Lưu lại index bắt đầu của từng loại ràng buộc để đánh trọng số
#         self.sat_helper.generate_implication_constraints() # Ít quan trọng
#         idx_crossing = len(self.sat_helper.cnf_clauses)
        
#         self.sat_helper.generate_crossing_constraints() # Quan trọng vừa
#         idx_degree = len(self.sat_helper.cnf_clauses)
        
#         self.sat_helper.generate_degree_constraints() # QUAN TRỌNG NHẤT
        
#         self.clauses = self.sat_helper.cnf_clauses
#         self.num_vars = self.sat_helper.max_var_id
        
#         # Đánh dấu các clause quan trọng (Degree Constraints)
#         for i in range(idx_degree, len(self.clauses)):
#             self.degree_clause_indices.add(i)
            
#         # Xây dựng map biến -> clauses để heuristic chọn biến nhanh hơn
#         for i, clause in enumerate(self.clauses):
#             for lit in clause:
#                 self.var_to_clauses[abs(lit)].append(i)

#         # --- 2. A* SEARCH ---
#         # State: assignment (Dict)
#         start_assignment = {} 
        
#         # Priority Queue: (f_score, g_score, assignment_id, assignment)
#         # assignment_id dùng để tie-break vì dict không so sánh được
#         tie_breaker = 0
#         h_start = self.heuristic_weighted(start_assignment)
#         pq = [(h_start, 0, tie_breaker, start_assignment)]
        
#         visited_states = set() # Tránh lặp trạng thái (Optional nếu bộ nhớ cho phép)

#         while pq:
#             f, g, _, assignment = heapq.heappop(pq)
            
#             # --- Goal Check ---
#             if self.is_satisfied(assignment):
#                 return self._construct_solution(assignment)
            
#             # --- Variable Selection (Dynamic Ordering) ---
#             # Thay vì chọn var_id + 1, hãy chọn biến "hot" nhất
#             next_var = self.select_most_constrained_variable(assignment)
            
#             if next_var is None:
#                 continue # Hết biến mà chưa satisfied -> Dead end

#             # --- Branching ---
#             # Thử True/False. 
#             # Mẹo: Thử giá trị nào có khả năng thỏa mãn nhiều clause nhất trước
#             # Ở đây ta thử cả 2, A* sẽ tự sắp xếp dựa trên f-score
#             for value in [True, False]:
#                 new_assignment = assignment.copy()
#                 new_assignment[next_var] = value
                
#                 # Pruning: Nếu gán xong mà vi phạm clause nào đó -> Bỏ qua luôn
#                 if self.is_invalid_partial(new_assignment, next_var):
#                     continue

#                 h = self.heuristic_weighted(new_assignment)
#                 new_g = g + 1
                
#                 tie_breaker += 1
#                 heapq.heappush(pq, (new_g + h, new_g, tie_breaker, new_assignment))
                
#         return None

#     def select_most_constrained_variable(self, assignment: Dict[int, bool]) -> Optional[int]:
#         """
#         [MOM Heuristic Simplified]
#         Chọn biến chưa được gán mà xuất hiện nhiều nhất trong các 
#         clause chưa thỏa mãn (ưu tiên clause ngắn).
#         """
#         # Đếm tần suất xuất hiện của các biến chưa gán trong các clause chưa thỏa mãn
#         counts = defaultdict(int)
        
#         for i, clause in enumerate(self.clauses):
#             # Kiểm tra clause này đã thỏa mãn chưa
#             is_sat = False
#             unassigned_vars = []
            
#             for lit in clause:
#                 var = abs(lit)
#                 val = assignment.get(var, None)
#                 if val is not None:
#                     if (lit > 0 and val) or (lit < 0 and not val):
#                         is_sat = True
#                         break
#                 else:
#                     unassigned_vars.append(var)
            
#             if not is_sat:
#                 # Clause chưa thỏa mãn -> Tăng điểm cho các biến trong nó
#                 # Clause càng ngắn (càng dễ vi phạm) -> Điểm càng cao
#                 weight = 10 if i in self.degree_clause_indices else 1
#                 if len(unassigned_vars) <= 2: 
#                     weight *= 5 # Unit clause hoặc Binary clause cực quan trọng
                    
#                 for var in unassigned_vars:
#                     counts[var] += weight

#         if not counts:
#             # Nếu không còn biến nào trong các clause chưa thỏa mãn, 
#             # lấy biến chưa gán bất kỳ (để điền nốt cho đủ bộ)
#             for v in range(1, self.num_vars + 1):
#                 if v not in assignment:
#                     return v
#             return None

#         # Trả về biến có điểm cao nhất
#         return max(counts, key=counts.get)

#     def is_invalid_partial(self, assignment: Dict[int, bool], last_var: int) -> bool:
#         """
#         Chỉ kiểm tra các clause có chứa biến vừa gán (last_var) để tăng tốc độ.
#         """
#         relevant_clause_indices = self.var_to_clauses.get(last_var, [])
        
#         for idx in relevant_clause_indices:
#             clause = self.clauses[idx]
#             is_clause_falsified = True
            
#             for lit in clause:
#                 var = abs(lit)
#                 val = assignment.get(var, None)
                
#                 if val is None:
#                     is_clause_falsified = False # Còn biến chưa gán -> Chưa sai
#                     break
                
#                 if (lit > 0 and val) or (lit < 0 and not val):
#                     is_clause_falsified = False # Đã thỏa mãn
#                     break
            
#             if is_clause_falsified:
#                 return True
#         return False

#     def heuristic_weighted(self, assignment: Dict[int, bool]) -> int:
#         """
#         Tính chi phí heuristic dựa trên trọng số clause.
#         """
#         score = 0
#         for i, clause in enumerate(self.clauses):
#             is_sat = False
#             unassigned_count = 0
            
#             for lit in clause:
#                 var = abs(lit)
#                 val = assignment.get(var, None)
                
#                 if val is not None:
#                     if (lit > 0 and val) or (lit < 0 and not val):
#                         is_sat = True
#                         break
#                 else:
#                     unassigned_count += 1
            
#             if not is_sat:
#                 # Clause chưa thỏa mãn
#                 weight = 1
#                 # Nếu là Degree Constraint -> Phạt nặng
#                 if i in self.degree_clause_indices:
#                     weight = 10
                
#                 # Nếu clause sắp bị vi phạm (chỉ còn 1 biến chưa gán - Unit Clause)
#                 # -> Cần ưu tiên xử lý ngay (coi như chi phí cao để A* chú ý)
#                 if unassigned_count == 1:
#                     weight += 5
                    
#                 score += weight
                
#         return score

#     def is_satisfied(self, assignment: Dict[int, bool]) -> bool:
#         # (Giữ nguyên như cũ)
#         for clause in self.clauses:
#             clause_sat = False
#             for lit in clause:
#                 var = abs(lit)
#                 val = assignment.get(var, None)
#                 if val is not None:
#                     if (lit > 0 and val) or (lit < 0 and not val):
#                         clause_sat = True
#                         break
#             if not clause_sat:
#                 return False
#         return True

#     def _construct_solution(self, assignment: Dict[int, bool]) -> List[List[str]]:
#         # (Giữ nguyên như cũ)
#         model = []
#         for var, val in assignment.items():
#             if val: model.append(var)
#             else: model.append(-var)
#         state = self.sat_helper.parse_model_to_state(model)
#         return self.sat_helper.render_solution(state)