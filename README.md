# Hashiwokakero Solver

Đồ án Project 2 môn Cơ sở Trí tuệ Nhân tạo - Giải bài toán Hashiwokakero bằng các thuật toán AI.

## 📋 Mô tả

Hashiwokakero (橋をかけろ, tiếng Nhật nghĩa là "Xây cầu") là một trò chơi giải đố logic. Mục tiêu là kết nối các đảo (số) bằng các cây cầu sao cho:
- Mỗi đảo có số cầu nối với nó đúng bằng số ghi trên đảo
- Cầu chỉ có thể ngang hoặc dọc
- Cầu không được giao nhau
- Có thể có 1 hoặc 2 cầu giữa hai đảo
- Tất cả các đảo phải được kết nối thành một mạng lưới liên thông

**Các thuật toán đã implement:**
- **PySAT Solver**: SAT-based với CNF encoding (nhanh nhất)
- **A* Search**: Search với heuristic (edge-based)
- **A* CNF Variants**: 3 biến thể (Basic, Weighted, MOMs)
- **Backtracking**: Với constraint propagation
- **Brute Force**: Exhaustive search (baseline)

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
│   │   ├── pysat_solver.py      # PySAT (edge-based CNF)
│   │   ├── astar_solver.py      # A* search
│   │   ├── astar_variants.py    # 3 biến thể A* với CNF
│   │   ├── backtracking_solver.py  #  Backtracking
│   │   └── bruteforce_solver.py    # Brute force
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
        └── AStar_MOMs/
```

## 🚀 Cài đặt

```bash
# Clone repository
cd CSAI-Project2-G3

# Tạo virtual environment (khuyến nghị)
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Linux/macOS

# Cài đặt dependencies
pip install -r requirements.txt
```

**Dependencies:** `python-sat`, `pandas`, `numpy`

## 💻 Cách sử dụng

### 1. Giải một puzzle

```bash
# Sử dụng PySAT solver (mặc định, nhanh nhất)
python main.py data/inputs/input-00.txt

### 1. Giải một puzzle

```bash
# Dùng PySAT (mặc định - nhanh nhất)
python main.py data/inputs/input-00.txt

# Chọn solver khác
python main.py data/inputs/input-01.txt -s pysat          # PySAT
python main.py data/inputs/input-01.txt -s astar          # A* Search
python main.py data/inputs/input-01.txt -s astar_basic    # A* Basic CNF
python main.py data/inputs/input-01.txt -s astar_weighted # A* Weighted
python main.py data/inputs/input-01.txt -s astar_moms     # A* MOMs
python main.py data/inputs/input-01.txt -s backtracking   # Backtracking
python main.py data/inputs/input-01.txt -s bruteforce     # Brute Force

# Chế độ verbose
python main.py data/inputs/input-01.txt -v
```

### 2. So sánh các solver

```bash
# So sánh tất cả 7 solvers trên 1 puzzle
python main.py data/inputs/input-00.txt --compare

# Với verbose
python main.py data/inputs/input-00.txt --compare -v
```

### 3. Benchmark nhiều test

```bash
cd src/benchmark
python comparator.py
```

Kết quả: `data/outputs/benchmark_report.csv`

## 📈 Công cụ Benchmark & Analysis

### 1. Comparator (src/benchmark/comparator.py)

Module benchmark chính với các tính năng:
- **Cross-platform timeout:** Sử dụng threading thay vì signal (hoạt động trên Windows/Linux/macOS)
- **Memory tracking:** Sử dụng `tracemalloc` để đo memory usage chính xác
- **Dual logging:** Ghi kết quả vào cả terminal và file log
- **CSV export:** Xuất kết quả ra CSV để dễ phân tích

**Chạy benchmark:**
```bash
cd src/benchmark
python comparator.py
```

**Output files:**
- `data/outputs/benchmark_report.csv`: Kết quả chi tiết (time, memory, status)
- `data/outputs/log_chay_thuc_te.txt`: Log đầy đủ quá trình benchmark

Giúp hiểu được complexity của từng test case.

### 3. Benchmark Analysis Notebook (benchmark_analysis.ipynb)

Jupyter notebook với visualizations:
- **Time comparison charts:** So sánh thời gian chạy
- **Memory usage plots:** Phân tích memory usage
- **Success rate heatmaps:** Biểu đồ success rate theo solver và test
- **Scatter plots:** Correlation giữa puzzle size và performance

**Các metric được phân tích:**
- Execution time (seconds)
- Memory usage (MB)
- Success rate (%)
- Nodes explored (cho search algorithms)


**Tất cả thành viên đều tham gia:**
- Code review và testing
- Viết documentation và README
- Benchmark analysis và visualization
- Presentation preparation

## 🔧 Công cụ hỗ trợ phát triển

### Development Tools
- **IDE:** VS Code / PyCharm
- **Version Control:** Git / GitHub
- **Python Version:** 3.8+
- **Virtual Environment:** venv

### Dependencies chính
```
python-sat>=0.1.7    # SAT solver
pandas>=1.3.0        # Data analysis
numpy>=1.21.0        # Numerical operations
jupyter>=1.0.0       # Notebook analysis
matplotlib>=3.4.0    # Visualization (optional)
seaborn>=0.11.0      # Statistical plots (optional)
```

## 📝 Format Input/Output

### Input Format
```
0 , 2 , 0 , 5 , 0 , 0 , 2
0 , 0 , 0 , 0 , 0 , 0 , 0
4 , 0 , 2 , 0 , 2 , 0 , 4
```
- **Số > 0:** Đảo cần nối (số cầu)
- **0:** Ô trống
- **Format:** CSV với dấu phẩy

### Output Format
```
["0", "2", "=", "5", "-", "-", "2"]
["0", "0", "0", "$", "0", "0", "|"]
["4", "=", "2", "$", "2", "=", "4"]
```

**Ký hiệu:**
- `-` : Cầu ngang đơn
- `=` : Cầu ngang đôi
- `|` : Cầu dọc đơn
- `$` : Cầu dọc đôi
- `0` : Ô trống

## 👥 Nhóm thực hiện

**Nhóm:** 3 
**Môn học:** Cơ sở Trí tuệ Nhân tạo (CSC14003)  
**Trường:** Đại học Khoa học Tự nhiên TP.HCM  
**Học kỳ:** HK1 2025-2026

---

*Cập nhật: Tháng 12/2025