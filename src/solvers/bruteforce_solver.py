from typing import List, Optional, Dict
from itertools import product
from .base_solver import BaseSolver
from core.puzzle import Puzzle
from core.constraints import (
    check_degree_exact,
    check_crossing,
    check_connected
)

class BruteForceSolver(BaseSolver):
    """
    Solve Hashiwokakero using brute-force search.
    Enumerates all possible bridge assignments.
    """

    def __init__(self):
        super().__init__()
        self.name = "BruteForceSolver" # <--- CẦN CÓ ĐỂ TẠO THƯ MỤC OUTPUT

    def solve(self, grid_or_puzzle) -> Optional[List[List[str]]]:
        """
        Attempt to solve the puzzle by enumerating all states.
        """
        # 1. CHUẨN HÓA INPUT (List -> Puzzle)
        if isinstance(grid_or_puzzle, Puzzle):
            puzzle = grid_or_puzzle
        else:
            puzzle = Puzzle(grid_or_puzzle)

        num_edges = len(puzzle.edges)
        
        # Cảnh báo nếu số cạnh quá lớn (vì 3 mũ N tăng rất nhanh)
        if num_edges > 15:
            print(f"  [Warning] BruteForce: {num_edges} edges -> 3^{num_edges} states. This will be slow!")

        # 2. VÉT CẠN
        # Mỗi cạnh có thể có 0, 1, hoặc 2 cầu
        for assignment in product([0, 1, 2], repeat=num_edges):
            # Tạo state dict: {edge_id: số_cầu}
            state = {i: assignment[i] for i in range(num_edges)}

            # Constraint checking
            # Check crossing trước vì nó vi phạm luật vật lý cơ bản
            if not check_crossing(puzzle, state):
                continue
            
            # Check đủ số cầu trên đảo
            if not check_degree_exact(puzzle, state):
                continue
            
            # Check liên thông (nếu bài toán yêu cầu chặt chẽ)
            if not check_connected(puzzle, state):
                continue

            # 3. RENDER OUTPUT (Dict -> Grid String)
            return self._render_solution(puzzle, state)

        return None

    def _render_solution(self, puzzle: Puzzle, state: Dict[int, int]) -> List[List[str]]:
        """Hàm hỗ trợ chuyển đổi trạng thái số sang lưới ký tự"""
        # Copy grid gốc
        result = [[str(cell) for cell in row] for row in puzzle.grid]
        
        for edge in puzzle.edges:
            bridges = state.get(edge.id, 0)
            if bridges > 0:
                # Chọn ký tự dựa trên hướng và số lượng cầu
                if edge.direction == 'H':
                    symbol = '=' if bridges == 2 else '-'
                else:
                    symbol = '$' if bridges == 2 else '|'
                
                # Điền vào các ô giữa 2 đảo
                for r, c in edge.cells:
                    result[r][c] = symbol
        return result