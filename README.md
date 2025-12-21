# Hashiwokakero Solver

Đồ án Project 2 môn Cơ sở Trí tuệ Nhân tạo - Giải bài toán Hashiwokakero bằng các thuật toán AI.

## 📋 Mô tả

Hashiwokakero (橋をかけろ, tiếng Nhật nghĩa là "Xây cầu") là một trò chơi giải đố logic. Mục tiêu là kết nối các đảo (số) bằng các cây cầu sao cho:
- Mỗi đảo có số cầu nối với nó đúng bằng số ghi trên đảo
- Cầu chỉ có thể ngang hoặc dọc
- Cầu không được giao nhau
- Có thể có 1 hoặc 2 cầu giữa hai đảo
- Tất cả các đảo phải được kết nối thành một mạng lưới liên thông

Project này đã implement đầy đủ 4 thuật toán chính (PySAT, A*, Backtracking, Brute Force) cùng với 4 biến thể A* sử dụng CNF encoding.

## 🏗️ Cấu trúc Project

```
CSAI-Project2-G3/
├── main.py                  # Script chính để chạy solver
├── count_stats.py           # Công cụ phân tích thống kê puzzle
├── benchmark_analysis.ipynb # Jupyter notebook phân tích benchmark
├── requirements.txt         # Dependencies
├── README.md               # Tài liệu này
├── src/
│   ├── core/               # Định nghĩa puzzle và constraints
│   │   ├── puzzle.py       # Class Puzzle (islands, edges, intersections)
│   │   ├── variables.py    # Dataclass Island và Edge
│   │   └── constraints.py  # Hàm kiểm tra các ràng buộc
│   ├── solvers/            # Các thuật toán solver
│   │   ├── base_solver.py       # Abstract base class
│   │   ├── pysat_solver.py      # ✅ PySAT (edge-based CNF)
│   │   ├── astar_solver.py      # ✅ A* search
│   │   ├── astar_variants.py    # ✅ 4 biến thể A* với CNF
│   │   ├── backtracking_solver.py  # ✅ Backtracking
│   │   └── bruteforce_solver.py    # ✅ Brute force
│   ├── utils/              # I/O và rendering
│   │   ├── io_handler.py   # Đọc/ghi file
│   │   └── renderer.py     # Hiển thị solution
│   └── benchmark/          # So sánh performance
│       └── comparator.py   # Benchmark và compare solvers
└── data/
    ├── inputs/             # Test cases (input-00.txt đến input-10.txt)
    └── outputs/            # Kết quả theo solver
        ├── PySATSolver/
        ├── AStarSolver/
        ├── BacktrackingSolver/
        ├── BruteForceSolver/
        ├── AStar_Basic/
        ├── AStar_Weighted/
        ├── AStar_MOMs/
        └── AStar_JW/
```

## 🚀 Cài đặt

```bash
# Clone repository
cd CSAI-Project2-G3

# (Khuyến nghị) Tạo virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# hoặc
.venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

**Dependencies chính:**
- `python-sat`: PySAT solver
- `pandas`: Phân tích benchmark
- `numpy>=1.21.0`: Xử lý ma trận

## 💻 Sử dụng

### Giải một puzzle

```bash
# Sử dụng PySAT solver (mặc định)
python main.py data/inputs/input-00.txt

# Chỉ định solver cụ thể
python main.py data/inputs/input-01.txt -s pysat
python main.py data/inputs/input-01.txt -s astar
python main.py data/inputs/input-01.txt -s backtracking
python main.py data/inputs/input-01.txt -s bruteforce

# Chỉ định output file
python main.py data/inputs/input-01.txt -o data/outputs/my_solution.txt

# Verbose mode (hiển thị thống kê chi tiết)
python main.py data/inputs/input-01.txt -v
```

**Các solver có sẵn:**
- `pysat`: PySAT với edge-based CNF encoding
- `astar`: A* search với heuristic tối ưu
- `backtracking`: Backtracking với pruning
- `bruteforce`: Vét cạn toàn bộ không gian trạng thái

### So sánh các solver

```bash
# So sánh tất cả 4 solver chính
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

Kết quả benchmark sẽ được lưu vào `data/outputs/benchmark_report.csv` và `data/outputs/log_chay_thuc_te.txt`

### Phân tích thống kê puzzle

```bash
# Đếm số đảo, cạnh, kích thước grid
python count_stats.py
```

## 📊 Các thuật toán đã implement

### 1. ✅ PySAT Solver (Edge-Based CNF)

**File:** [src/solvers/pysat_solver.py](src/solvers/pysat_solver.py)

Sử dụng SAT solver với edge-based encoding:
- **Biến logic:** Mỗi cạnh có 2 biến:
  - `b1(e)`: Cạnh e có ít nhất 1 cầu (≥1)
  - `b2(e)`: Cạnh e có đúng 2 cầu (=2)
- **CNF Constraints:**
  - Implication: `¬b2(e) ∨ b1(e)` cho mọi cạnh
  - Crossing: Hai cạnh cắt nhau không thể đồng thời có cầu
  - Island Degree: Tổng số cầu kề với mỗi đảo = giá trị trên đảo (dùng `CardEnc.equals`)
  - Connectivity: Kiểm tra liên thông bằng BFS (lazy check với blocking clauses)
- **Thư viện:** PySAT (Glucose3 solver)

### 2. ✅ A* Search

**File:** [src/solvers/astar_solver.py](src/solvers/astar_solver.py)

A* search với state-space search:
- **State:** Tuple các giá trị (0, 1, 2) cho các cạnh đã duyệt
- **Heuristic:** Tổng số cầu còn thiếu của tất cả các đảo
- **Pruning:** 
  - Kiểm tra crossing constraints
  - Kiểm tra degree partial (không đảo nào vượt quá số cầu quy định)
- **Priority Queue:** Sử dụng heapq với f(n) = g(n) + h(n)

### 3. ✅ Backtracking

**File:** [src/solvers/backtracking_solver.py](src/solvers/backtracking_solver.py)

Backtracking với constraint checking:
- **Strategy:** Thử gán giá trị 2, 1, 0 cho từng cạnh theo thứ tự
- **Pruning:**
  - Early checking crossing constraints
  - Early checking degree partial
- **Base case:** Kiểm tra degree exact và connectivity khi đã duyệt hết các cạnh

### 4. ✅ Brute Force

**File:** [src/solvers/bruteforce_solver.py](src/solvers/bruteforce_solver.py)

Vét cạn toàn bộ không gian trạng thái:
- **Complexity:** O(3^n) với n = số cạnh
- **Strategy:** Duyệt qua tất cả các assignment có thể (0, 1, 2 cho mỗi cạnh)
- **Warning:** Chỉ dùng cho puzzle nhỏ (< 15 cạnh)

### 5. ✅ A* Variants with CNF (4 biến thể)

**File:** [src/solvers/astar_variants.py](src/solvers/astar_variants.py)

Các biến thể A* search trên CNF encoding, khác nhau về heuristic và variable selection:

#### a) AStar_Basic
- **Heuristic:** Đếm tổng số clause chưa thỏa mãn
- **Variable Selection:** Tuần tự
- Dùng làm baseline để so sánh

#### b) AStar_Weighted
- **Heuristic:** Phạt nặng (x10) nếu vi phạm Degree Constraints
- **Variable Selection:** Tuần tự
- Tích hợp domain knowledge về bài toán

#### c) AStar_MOMs (Maximum Occurrences in Minimum clauses)
- **Heuristic:** Weighted + phạt cực nặng Unit Clause
- **Variable Selection:** Chọn biến xuất hiện nhiều nhất trong các clause ngắn
- Thường hiệu quả nhất trong các biến thể

#### d) AStar_JW (Jeroslow-Wang)
- **Heuristic:** Phạt theo hàm mũ 2^(-length), clause ngắn phạt nặng hơn
- **Variable Selection:** Maximize J(x) = Σ(2^(-|C|))
- Tối ưu hóa theo lý thuyết SAT solver

## 🏛️ Kiến trúc Core Module

### Puzzle Class ([src/core/puzzle.py](src/core/puzzle.py))

Class chính đại diện cho một puzzle instance:
- **Islands:** Danh sách các đảo với ID, tọa độ, giá trị
- **Edges:** Danh sách các cạnh tiềm năng (potential bridges)
- **Intersections:** Tập các cặp cạnh giao nhau (pre-computed)
- **Adjacency List:** Danh sách kề tối ưu cho traversal

### Variables ([src/core/variables.py](src/core/variables.py))

Dataclass định nghĩa các thực thể:
- **Island:** `(id, row, col, value)`
- **Edge:** `(id, u, v, direction, cells)`

### Constraints ([src/core/constraints.py](src/core/constraints.py))

Các hàm kiểm tra ràng buộc (solver-independent):
- `check_crossing()`: Kiểm tra cầu không giao nhau
- `check_degree_partial()`: Kiểm tra số cầu không vượt quá (partial state)
- `check_degree_exact()`: Kiểm tra số cầu đúng bằng yêu cầu (complete state)
- `check_connected()`: Kiểm tra liên thông bằng BFS

## 🧪 Testing

Project đã được test với 11 test cases (`input-00.txt` đến `input-10.txt`):
- Input nhỏ: 5x5, 7x7
- Input trung bình: 9x9, 11x11
- Input lớn: 15x15, 20x20

Kết quả được lưu trong `data/outputs/` theo từng solver.

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
- Số > 0: Đảo (island) với giá trị là số cầu cần nối
- 0: Ô trống

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
- **Số**: Đảo (island)
- **`-`**: Cầu ngang đơn (1 bridge horizontal)
- **`=`**: Cầu ngang đôi (2 bridges horizontal)
- **`|`**: Cầu dọc đơn (1 bridge vertical)
- **`$`**: Cầu dọc đôi (2 bridges vertical)
- **`0`**: Ô trống (không có cầu)

## 📈 Benchmark & Phân tích

Project có công cụ benchmark tích hợp:

### Chạy Benchmark
```bash
python main.py "data/inputs/*.txt" --benchmark -v
```

### Kết quả
- **CSV Report:** `data/outputs/benchmark_report.csv`
  - Thời gian chạy từng solver
  - Memory usage
  - Success/Fail status
- **Log File:** `data/outputs/log_chay_thuc_te.txt`
  - Chi tiết quá trình chạy
- **Jupyter Notebook:** `benchmark_analysis.ipynb`
  - Phân tích và visualize kết quả

### Các metric đo lường
- **Execution Time:** Thời gian giải (seconds)
- **Memory Usage:** Bộ nhớ sử dụng (MB)
- **Success Rate:** Tỷ lệ giải thành công
- **Nodes Explored:** Số trạng thái đã duyệt (cho A*, Backtracking)

## 👥 Nhóm thực hiện

**Nhóm:** CSAI-Project2-G3  
**Môn học:** Cơ sở Trí tuệ Nhân tạo  
**Trường:** Đại học Khoa học Tự nhiên TP.HCM

### Phân công công việc

Tất cả các thành viên đều đã hoàn thành phần việc được giao:

1. **PySAT Solver & Core Infrastructure**
   - Implement edge-based CNF encoding
   - Develop Puzzle, Island, Edge classes
   - Constraint checking system

2. **A* Search & Variants**
   - A* solver với heuristic tối ưu
   - 4 biến thể A* với CNF (Basic, Weighted, MOMs, JW)
   - Variable selection strategies

3. **Backtracking & Brute Force**
   - Backtracking với pruning
   - Brute force solver
   - Benchmark infrastructure

## 🔧 Công cụ hỗ trợ

### count_stats.py
Phân tích thống kê các puzzle:
```bash
python count_stats.py
```
Output: Số đảo, số cạnh tiềm năng, kích thước grid cho từng test case

### benchmark_analysis.ipynb
Jupyter notebook để:
- Visualize kết quả benchmark
- So sánh performance các solver
- Phân tích complexity vs execution time

## 📚 Tài liệu tham khảo

- [PySAT Documentation](https://pysathq.github.io/)
- [Hashiwokakero Rules](https://en.wikipedia.org/wiki/Hashiwokakero)
- [SAT Solving](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)
- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

## 🎯 Kết quả đạt được

✅ **Đã hoàn thành đầy đủ các yêu cầu:**
1. Implement 4 thuật toán chính: PySAT, A*, Backtracking, Brute Force
2. Edge-based logical variables và CNF encoding
3. Constraint checking system (crossing, degree, connectivity)
4. Automated CNF generation
5. Benchmark và comparison tools
6. 4 biến thể A* với các heuristic khác nhau
7. Documentation đầy đủ

✅ **Tested trên 11 test cases với độ khó tăng dần**

✅ **Có công cụ phân tích và visualize kết quả**

## 💡 Lưu ý khi sử dụng

- **Brute Force:** Chỉ nên dùng cho puzzle nhỏ (< 15 cạnh) vì complexity O(3^n)
- **PySAT:** Thường nhanh nhất cho puzzle lớn và phức tạp
- **A*:** Cân bằng tốt giữa tốc độ và tính tối ưu
- **Backtracking:** Hiệu quả với pruning strategies tốt
- **A* Variants:** MOMs và JW thường cho performance tốt nhất với CNF encoding

## 🐛 Known Issues

- Timeout mặc định: 300 giây (có thể điều chỉnh trong [src/benchmark/comparator.py](src/benchmark/comparator.py))
- Memory usage có thể cao với puzzle rất lớn (> 20x20)

---

**Cập nhật lần cuối:** Tháng 12, 2025
