from pysat.solvers import Glucose3
from pysat.card import CardEnc


class HashiSolver:
    def __init__(self, grid):
        self.grid = grid # Ma trận đầu vào (số là đảo, 0 là rỗng)
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.cnf_clauses = [] # Chứa tất cả các mệnh đề
        # Tính toán max_id để dùng cho biến phụ của CardEnc sau này
        self.max_var_id = self.rows * self.cols * 5 

    def get_var_id(self, r, c, k):
        """
        k: 0=Empty, 1=H-1, 2=H-2, 3=V-1, 4=V-2
        Output: Một số nguyên dương duy nhất > 0
        """
        return (r * self.cols + c) * 5 + (k + 1)

    def decode_var_id(self, var_id):
        """Dùng để giải mã kết quả từ Solver"""
        val = var_id - 1
        k = val % 5
        val //= 5
        c = val % self.cols
        r = val // self.cols
        return r, c, k
    
    def generate_cell_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0: continue # Bỏ qua đảo

                # 1. At Least One: (X0 v X1 v X2 v X3 v X4)
                vars = [self.get_var_id(r, c, k) for k in range(5)]
                self.cnf_clauses.append(vars)

                # 2. At Most One: Không thể có 2 trạng thái cùng lúc
                for i in range(5):
                    for j in range(i + 1, 5):
                        # (-Xi v -Xj)
                        self.cnf_clauses.append([-vars[i], -vars[j]])
                        
    def generate_flow_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] > 0: continue # Bỏ qua đảo

                # --- Xử lý Cầu Ngang (k=1, k=2) ---
                for k in [1, 2]: 
                    curr_var = self.get_var_id(r, c, k)
                    
                    # Kiểm tra ô bên Phải (Right)
                    if c + 1 < self.cols: # Còn trong biên
                        if self.grid[r][c+1] > 0: 
                            pass # Gặp đảo -> OK, không cần thêm luật
                        else:
                            # Gặp ô thường -> Ô đó phải là cầu cùng loại k
                            next_var = self.get_var_id(r, c+1, k)
                            # Logic: curr -> next <=> -curr v next
                            self.cnf_clauses.append([-curr_var, next_var])
                    else:
                        # Hết biên -> Không thể là cầu ngang
                        self.cnf_clauses.append([-curr_var])

                    # Kiểm tra ô bên Trái (Left) -> Tương tự hoặc bỏ qua nếu duyệt 1 chiều
                    # (Lưu ý: Thường chỉ cần duyệt forward (phải/dưới) HOẶC 
                    # duyệt cả 2 chiều để chặt chẽ. Đơn giản nhất là check biên:
                    # Nếu c-1 < 0 thì không thể là cầu ngang).
                    if c - 1 < 0:
                         self.cnf_clauses.append([-curr_var])

                # --- Xử lý Cầu Dọc (k=3, k=4) ---
                # (Bạn tự implement tương tự cho r+1 và r-1)
                for k in [3, 4]:
                    curr_var = self.get_var_id(r, c, k)
                    
                    # Kiểm tra ô bên Dưới (Down)
                    if r + 1 < self.rows: # Còn trong biên
                        if self.grid[r+1][c] > 0: 
                            pass # Gặp đảo -> OK, không cần thêm luật
                        else:
                            # Gặp ô thường -> Ô đó phải là cầu cùng loại k
                            next_var = self.get_var_id(r+1, c, k)
                            # Logic: curr -> next <=> -curr v next
                            self.cnf_clauses.append([-curr_var, next_var])
                    else:
                        # Hết biên -> Không thể là cầu dọc
                        self.cnf_clauses.append([-curr_var])

                    # Kiểm tra ô bên Trên (Up)
                    if r - 1 < 0:
                         self.cnf_clauses.append([-curr_var])

    def generate_island_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                if val == 0: continue # Không phải đảo thì bỏ qua

                # Danh sách các biến cầu xung quanh đảo
                # Mỗi phần tử là (var_id, weight)
                bridge_vars = []

                # 1. Hàng xóm phía Bắc (North): (r-1, c)
                if r > 0 and self.grid[r-1][c] == 0:
                    bridge_vars.append((self.get_var_id(r-1, c, 3), 1)) # V-1
                    bridge_vars.append((self.get_var_id(r-1, c, 4), 2)) # V-2
                
                # 2. Hàng xóm phía Nam (South): (r+1, c)
                if r + 1 < self.rows and self.grid[r+1][c] == 0:
                    bridge_vars.append((self.get_var_id(r+1, c, 3), 1)) # V-1
                    bridge_vars.append((self.get_var_id(r+1, c, 4), 2)) # V-2
                
                # 3. Hàng xóm phía Tây (West): (r, c-1)
                if c > 0 and self.grid[r][c-1] == 0:
                    bridge_vars.append((self.get_var_id(r, c-1, 1), 1)) # H-1
                    bridge_vars.append((self.get_var_id(r, c-1, 2), 2)) # H-2
                
                # 4. Hàng xóm phía Đông (East): (r, c+1)
                if c + 1 < self.cols and self.grid[r][c+1] == 0:
                    bridge_vars.append((self.get_var_id(r, c+1, 1), 1)) # H-1
                    bridge_vars.append((self.get_var_id(r, c+1, 2), 2)) # H-2

                # Tạo constraint: tổng trọng số = val
                # Chuyển thành danh sách literal mở rộng
                # Ví dụ: nếu có V-2 (weight=2), ta thêm 2 lần literal đó
                expanded_lits = []
                for var_id, weight in bridge_vars:
                    for _ in range(weight):
                        expanded_lits.append(var_id)
                
                # Dùng CardEnc.equals với danh sách đã mở rộng
                if len(expanded_lits) > 0:
                    cnf = CardEnc.equals(lits=expanded_lits, bound=val, top_id=self.max_var_id)
                    self.cnf_clauses.extend(cnf.clauses)
                    self.max_var_id = cnf.nv

    def solve(self):
        # 1. Sinh toàn bộ luật
        self.generate_cell_constraints()
        self.generate_flow_constraints()
        self.generate_island_constraints()

        # 2. Khởi tạo Solver
        g = Glucose3()
        for clause in self.cnf_clauses:
            g.add_clause(clause)

        # 3. Giải
        if g.solve():
            model = g.get_model()
            return self.parse_model(model)
        else:
            return None # Không tìm thấy lời giải

    def parse_model(self, model):
        # Tạo bảng kết quả rỗng
        result = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Chỉ quan tâm các biến True dương
        for var in model:
            if var > 0 and var <= self.rows * self.cols * 5: # Bỏ qua biến phụ của CardEnc
                r, c, k = self.decode_var_id(var)
                
                # Mapping k ra ký tự theo đề bài
                char_map = {0: '0', 1: '-', 2: '=', 3: '|', 4: '$'}
                
                # Nếu ô đó là đảo thì giữ nguyên số, ngược lại điền ký tự cầu
                if self.grid[r][c] == 0:
                    result[r][c] = char_map[k]
                else:
                    result[r][c] = str(self.grid[r][c])
        return result