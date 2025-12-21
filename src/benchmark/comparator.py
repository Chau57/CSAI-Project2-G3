import sys
import os
import time
import signal
import glob
import tracemalloc
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path

# --- 1. SETUP PATHS TỰ ĐỘNG ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

# Trỏ đúng vào thư mục data
INPUT_DIR = os.path.join(PROJECT_ROOT, "data", "inputs")
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "outputs")

# Tên file log và báo cáo
OUTPUT_REPORT_CSV = "benchmark_report.csv"
OUTPUT_LOG_TXT = "log_chay_thuc_te.txt" 

MAX_TIMEOUT_SECONDS = 300 

# Fix import lỗi
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from solvers.pysat_solver import PySATSolver
from solvers.astar_solver import AStarSolver
from solvers.backtracking_solver import BacktrackingSolver
from solvers.bruteforce_solver import BruteForceSolver
from utils.io_handler import read_input
from solvers.astar_variants import AStarBasicCNF, AStarWeightedCNF, AStarMomsCNF, AStarJWCNF

# --- CLASS LOGGER ĐỂ GHI SONG SONG (Màn hình + File) ---
class DualLogger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message) # Ghi ra màn hình
        self.log.write(message)      # Ghi vào file
        self.log.flush()             # Lưu ngay lập tức để không mất dữ liệu nếu crash

    def flush(self):
        # Hàm này cần thiết cho python 3 khi dùng flush=True
        self.terminal.flush()
        self.log.flush()

# --- CÁC CLASS CŨ GIỮ NGUYÊN ---

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

class BenchmarkRunner:
    def __init__(self):
        self.solvers = [
            PySATSolver(),   
            
            # Đã chạy trước đó
            # AStarSolver(), 
            # BacktrackingSolver(),
            # BruteForceSolver(),
            
            AStarBasicCNF(),
            AStarWeightedCNF(),
            AStarMomsCNF(),
            AStarJWCNF(),
        ]
        self.results = []

    def run_solver_safe(self, solver, grid, timeout):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        tracemalloc.start()
        start_time = time.time()
        
        status = "OK"
        solution = None
        error_msg = ""
        
        try:
            solution = solver.solve(grid)
            if solution is None:
                status = "NO_SOL"
        except TimeoutException:
            status = "TIMEOUT"
        except Exception as e:
            status = "ERROR"
            error_msg = str(e)
        finally:
            signal.alarm(0)
            end_time = time.time()
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        elapsed_time = end_time - start_time
        peak_mem_mb = peak_mem / (1024 * 1024)

        return {
            "solver": solver.name,
            "time": elapsed_time,
            "memory_mb": peak_mem_mb,
            "status": status,
            "solution": solution,
            "error": error_msg
        }

    def check_correctness(self, ref_solution, test_solution):
        if ref_solution is None and test_solution is None: return True
        if ref_solution is None or test_solution is None: return False
        
        rows = len(ref_solution)
        cols = len(ref_solution[0])
        for r in range(rows):
            for c in range(cols):
                if ref_solution[r][c] != test_solution[r][c]:
                    return False
        return True

    def save_solution_file(self, input_filename, solver_name, solution):
        if solution is None: return

        solver_dir = os.path.join(OUTPUT_BASE_DIR, solver_name)
        if not os.path.exists(solver_dir):
            os.makedirs(solver_dir)

        output_filename = input_filename.replace("input", "output")
        output_path = os.path.join(solver_dir, output_filename)

        try:
            with open(output_path, 'w') as f:
                for row in solution:
                    line = ",".join(str(cell) for cell in row)
                    f.write(line + "\n")
        except Exception as e:
            print(f"    [Warning] Could not save file {output_path}: {e}")

    def run_all(self):
        input_files = sorted(glob.glob(os.path.join(INPUT_DIR, "input-*.txt")))
        
        print(f"Found {len(input_files)} inputs.")
        print(f"Saving outputs to: {OUTPUT_BASE_DIR}")
        print("-" * 80)

        for filepath in input_files:
            filename = os.path.basename(filepath)
            print(f"\nProcessing: {filename}...")
            
            try:
                grid = read_input(filepath)
            except Exception as e:
                print(f"  Err reading file: {e}")
                continue

            # --- 1. Run PySAT (Ground Truth) ---
            print(f"  > PySATSolver (Reference)...", end=" ", flush=True)
            pysat_res = self.run_solver_safe(self.solvers[0], grid, timeout=60)
            
            ground_truth_sol = pysat_res['solution']
            if pysat_res['status'] == 'OK':
                print(f"Done ({pysat_res['time']:.4f}s)")
                self.save_solution_file(filename, "PySATSolver", pysat_res['solution'])
            else:
                print(f"Failed ({pysat_res['status']})")

            self.record_result(filename, pysat_res, True)

            # --- 2. Run other Solvers ---
            for solver in self.solvers[1:]:
                print(f"  > {solver.name}...", end=" ", flush=True)
                
                import copy
                grid_copy = copy.deepcopy(grid)
                
                res = self.run_solver_safe(solver, grid_copy, timeout=MAX_TIMEOUT_SECONDS)
                
                is_correct = False
                if res['status'] == 'OK':
                    if ground_truth_sol:
                        is_correct = self.check_correctness(ground_truth_sol, res['solution'])
                    else:
                        is_correct = True
                    self.save_solution_file(filename, solver.name, res['solution'])
                
                print(f"{res['status']} | Time: {res['time']:.4f}s | Correct: {is_correct}")
                self.record_result(filename, res, is_correct)

    def record_result(self, filename, res, is_correct):
        entry = {
            "Input": filename,
            "Solver": res['solver'],
            "Status": res['status'],
            "Time (s)": round(res['time'], 4),
            "Memory (MB)": round(res['memory_mb'], 4),
            "Correct": is_correct,
            "Pass 1min": res['status'] == 'OK' and res['time'] <= 60,
            "Pass 2min": res['status'] == 'OK' and res['time'] <= 120,
            "Pass 5min": res['status'] == 'OK' and res['time'] <= 300,
        }
        self.results.append(entry)

    def generate_report(self):
        print("\n" + "="*80)
        print("BENCHMARK REPORT")
        print("="*80)
        
        if not self.results:
            print("[Warning] No results to save.")
            return

        df = pd.DataFrame(self.results)
        
        print("\n--- Summary ---")
        try:
            summary = df.groupby("Solver")[["Pass 1min", "Pass 2min", "Pass 5min"]].sum()
            summary["Total"] = df["Input"].nunique()
            print(summary)
        except Exception:
            pass
        
        report_path = os.path.join(OUTPUT_BASE_DIR, OUTPUT_REPORT_CSV)
        os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
        df.to_csv(report_path, index=False)
        print(f"\n[SUCCESS] Report saved to: {report_path}")

# --- MAIN ---
if __name__ == "__main__":
    # 1. Đảm bảo thư mục output tồn tại trước
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    # 2. Thiết lập đường dẫn file log
    log_file_path = os.path.join(OUTPUT_BASE_DIR, OUTPUT_LOG_TXT)

    # 3. Kích hoạt DualLogger: Chuyển hướng print vào cả file và màn hình
    # Từ dòng này trở đi, mọi lệnh print() sẽ tự động ghi vào log_file_path
    sys.stdout = DualLogger(log_file_path)

    print(f"Logging started. Log file: {log_file_path}")

    # 4. Chạy Benchmark
    runner = BenchmarkRunner()
    runner.run_all()
    runner.generate_report()