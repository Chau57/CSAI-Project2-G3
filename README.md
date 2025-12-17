# Hashiwokakero Solver

Đồ án Project 2 môn Cơ sở Trí tuệ Nhân tạo - Giải bài toán Hashiwokakero bằng các thuật toán AI.

## 📋 Mô tả

Hashiwokakero (橋をかけろ, tiếng Nhật nghĩa là "Xây cầu") là một trò chơi giải đố logic. Mục tiêu là kết nối các đảo (số) bằng các cây cầu sao cho:
- Mỗi đảo có số cầu nối với nó đúng bằng số ghi trên đảo
- Cầu chỉ có thể ngang hoặc dọc
- Cầu không được giao nhau
- Có thể có 1 hoặc 2 cầu giữa hai đảo
- Tất cả các đảo phải được kết nối thành một mạng lưới liên thông

## 🏗️ Cấu trúc Project

```
hashiwokakero/
├── main.py              # Script chính để chạy solver
├── requirements.txt     # Dependencies
├── src/
│   ├── core/           # Định nghĩa puzzle và logical variables
│   │   ├── puzzle.py
│   │   └── variables.py
│   ├── solvers/        # Các thuật toán solver
│   │   ├── base_solver.py       # Abstract base class
│   │   ├── pysat_solver.py      # ✅ PySAT implementation
│   │   ├── astar_solver.py      # 🔄 A* search
│   │   ├── backtracking_solver.py  # 🔄 Backtracking
│   │   └── bruteforce_solver.py    # 🔄 Brute force
│   ├── utils/          # I/O và CNF generation
│   │   └── io_handler.py
│   └── benchmark/      # So sánh performance
│       └── comparator.py
└── data/
    ├── inputs/         # Test cases
    └── outputs/        # Kết quả
```

## 🚀 Cài đặt

```bash
cd hashiwokakero
pip install -r requirements.txt
```

## 💻 Sử dụng

### Giải một puzzle

```bash
# Sử dụng PySAT solver (mặc định)
python main.py data/inputs/input-01.txt

# Chỉ định output file
python main.py data/inputs/input-01.txt -o data/outputs/output-01.txt

# Verbose mode
python main.py data/inputs/input-01.txt -v
```

### So sánh các solver

```bash
# So sánh tất cả các solver
python main.py data/inputs/input-01.txt --compare

# So sánh với verbose output
python main.py data/inputs/input-01.txt --compare -v
```

### Benchmark trên nhiều file

```bash
# Test trên tất cả input files
python main.py "data/inputs/*.txt" --benchmark

# Với verbose output
python main.py "data/inputs/*.txt" --benchmark -v
```

## 📊 Yêu cầu Project

### ✅ Đã hoàn thành

1. **Define Logical Variables**: Mỗi ô trong ma trận được gán 5 biến logic
   - k=0: Empty (không có cầu)
   - k=1: Horizontal Single (-)
   - k=2: Horizontal Double (=)
   - k=3: Vertical Single (|)
   - k=4: Vertical Double ($)

2. **CNF Constraints**: Đã formulate các constraint theo CNF
   - Cell constraints: Mỗi ô có đúng 1 trạng thái
   - Flow constraints: Cầu phải nối liền
   - Island constraints: Mỗi đảo có đúng số cầu yêu cầu

3. **Automate CNF Generation**: Tự động sinh CNF từ puzzle

4. **PySAT Solver**: Sử dụng thư viện PySAT để giải SAT problem

### 🔄 TODO (cho các thành viên khác)

5. **A* Search Algorithm**: Implement trong `src/solvers/astar_solver.py`
   - Định nghĩa heuristic function
   - Implement priority queue
   - Search cho solution

6. **Compare Methods**: Implement các thuật toán để so sánh
   - **Backtracking**: `src/solvers/backtracking_solver.py`
   - **Brute Force**: `src/solvers/bruteforce_solver.py`

## 🧪 Testing

```bash
# Run tests (khi đã implement)
python -m pytest tests/

# Test specific solver
python -m pytest tests/test_pysat_solver.py
```

## 📝 Format Input/Output

### Input Format
```
0 , 2 , 0 , 5 , 0 , 0 , 2
0 , 0 , 0 , 0 , 0 , 0 , 0
4 , 0 , 2 , 0 , 2 , 0 , 4
0 , 0 , 0 , 0 , 0 , 0 , 0
0 , 1 , 0 , 5 , 0 , 2 , 0
0 , 0 , 0 , 0 , 0 , 0 , 0
4 , 0 , 0 , 0 , 0 , 0 , 3
```

### Output Format
```
["0", "2", "=", "5", "-", "-", "2"]
["0", "0", "0", "$", "0", "0", "|"]
["4", "=", "2", "$", "2", "=", "4"]
["$", "0", "0", "$", "0", "0", "|"]
["$", "1", "-", "5", "=", "2", "|"]
["$", "0", "0", "0", "0", "0", "|"]
["4", "=", "=", "=", "=", "=", "3"]

```

Ký hiệu:
- Số : Đảo (island)
- `-`: Cầu ngang đơn
- `=`: Cầu ngang đôi
- `|`: Cầu dọc đơn
- `$`: Cầu dọc đôi
- `0`: Ô trống (không có cầu)

## 👥 Phân công

- **Thành viên 1**: PySAT Solver
- **Thành viên 2**: A* Search Algorithm
- **Thành viên 3**: Brute Force & Backtracking

## 📚 Tài liệu tham khảo

- [PySAT Documentation](https://pysathq.github.io/)
- [Hashiwokakero Rules](https://en.wikipedia.org/wiki/Hashiwokakero)
- [SAT Solving](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)

## 🤝 Hướng dẫn Contribute

1. Mỗi solver phải kế thừa từ `BaseSolver`
2. Implement phương thức `solve(grid)` 
3. Trả về `List[List[str]]` hoặc `None` nếu không có solution
4. Update `src/solvers/__init__.py` để export solver mới
5. Uncomment solver trong `main.py` và `benchmark/comparator.py`

### Ví dụ implement solver mới:

```python
from .base_solver import BaseSolver

class MyNewSolver(BaseSolver):
    def __init__(self):
        super().__init__()
    
    def solve(self, grid):
        # Your implementation here
        return solution
```

## 📄 License

Project này được tạo cho mục đích học tập tại HCMUS.

---

**Nhóm**: CSAI-Project2-G3  
**Môn học**: Cơ sở Trí tuệ Nhân tạo  
**Trường**: Đại học Khoa học Tự nhiên TP.HCM
