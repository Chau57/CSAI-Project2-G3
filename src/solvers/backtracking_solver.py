from typing import List, Optional, Dict
from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import check_degree_partial, check_crossing, check_degree_exact, check_connected

class BacktrackingSolver(BaseSolver):
    """
    Backtracking implementation using Core Puzzle & Constraints.
    """
    
    def __init__(self):
        super().__init__()
        self.name = "BacktrackingSolver"
        self.puzzle: Optional[Puzzle] = None
        self.num_edges = 0

    def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
        """
        Main solve function.
        Accepts either raw grid or Puzzle object.
        """
        # 1. Chuẩn hóa Input thành Puzzle Object
        if isinstance(grid_or_puzzle, Puzzle):
            self.puzzle = grid_or_puzzle
        else:
            self.puzzle = Puzzle(grid_or_puzzle)
            
        self.num_edges = len(self.puzzle.edges)
        
        # 2. Khởi tạo state rỗng (Dictionary: edge_id -> bridges)
        # Ban đầu chưa gán cạnh nào
        initial_state: Dict[int, int] = {}
        
        # 3. Chạy đệ quy
        final_state = self._backtrack(0, initial_state)
        
        if final_state:
            return self._render_solution(final_state)
        return None

    def _backtrack(self, edge_idx: int, current_state: Dict[int, int]) -> Optional[Dict[int, int]]:
        # Base case: Đã duyệt hết tất cả các cạnh
        if edge_idx == self.num_edges:
            # Kiểm tra trạng thái cuối cùng (đủ cầu + liên thông)
            if check_degree_exact(self.puzzle, current_state) and \
               check_connected(self.puzzle, current_state):
                return current_state
            return None

        # Lấy cạnh hiện tại
        edge = self.puzzle.edges[edge_idx]
        
        # Chiến lược Heuristic: Thử nối cầu (2, 1) trước để về đích nhanh hơn
        # (Hoặc đổi thành [0, 1, 2] nếu muốn vét cạn an toàn)
        for val in [2, 1, 0]:
            # Gán thử giá trị
            current_state[edge.id] = val
            
            # --- PRUNING (CẮT TỈA) ---
            # 1. Kiểm tra Giao nhau (Crossing)
            # Chỉ cần check nếu cạnh này có cầu (>0)
            if val > 0:
                if not check_crossing(self.puzzle, current_state):
                    del current_state[edge.id] # Backtrack
                    continue
            
            # 2. Kiểm tra Số cầu trên đảo (Degree) - Partial Check
            # Không đảo nào được vượt quá số quy định
            if not check_degree_partial(self.puzzle, current_state):
                del current_state[edge.id] # Backtrack
                continue
                
            # Đệ quy bước tiếp theo
            result = self._backtrack(edge_idx + 1, current_state)
            if result:
                return result
                
            # Backtrack: Xóa trạng thái để thử giá trị khác
            del current_state[edge.id]
            
        return None

    def _render_solution(self, state: Dict[int, int]) -> List[List[str]]:
        """Convert logical state back to visual grid."""
        # Tạo bản copy từ grid gốc (đang là numpy int array)
        result = [[str(cell) for cell in row] for row in self.puzzle.grid]
        
        for edge in self.puzzle.edges:
            bridges = state.get(edge.id, 0)
            if bridges > 0:
                symbol = ('=' if bridges == 2 else '-') if edge.direction == 'H' else \
                         ('$' if bridges == 2 else '|')
                
                for r, c in edge.cells:
                    result[r][c] = symbol
        return result