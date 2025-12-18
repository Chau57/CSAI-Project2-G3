import sys
import os
import time
import signal
import glob
import tracemalloc
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path

# --- Setup Paths ---
sys.path.insert(0, str(Path(__file__).parent.parent))

from solvers.pysat_solver import PySATSolver
from solvers.astar_solver import AStarSolver
from solvers.backtracking_solver import BacktrackingSolver
from solvers.bruteforce_solver import BruteForceSolver
from utils.io_handler import read_input

# --- CONFIGURATION ---
INPUT_DIR = "../data/inputs"
OUTPUT_BASE_DIR = "../data/outputs"  
OUTPUT_REPORT_CSV = "benchmark_report.csv"
MAX_TIMEOUT_SECONDS = 300 

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

class BenchmarkRunner:
    def __init__(self):
        self.solvers = [
            PySATSolver(),       
            AStarSolver(),
            BacktrackingSolver(),
            BruteForceSolver()
        ]
        self.results = []

    def run_solver_safe(self, solver, grid, timeout):
        """Chạy solver với timeout và đo memory."""
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
        """So sánh output với PySAT"""
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
        """Lưu kết quả ra file text vào thư mục outputs/SolverName/"""
        if solution is None:
            return

        # Tạo đường dẫn: data/outputs/TenThuatToan
        solver_dir = os.path.join(OUTPUT_BASE_DIR, solver_name)
        if not os.path.exists(solver_dir):
            os.makedirs(solver_dir)

        # Đổi tên input-xx.txt -> output-xx.txt
        output_filename = input_filename.replace("input", "output")
        output_path = os.path.join(solver_dir, output_filename)

        try:
            with open(output_path, 'w') as f:
                # Nếu solution là list of strings (như PySAT trả về)
                # Hoặc list of list of chars. Cần đảm bảo format string.
                for row in solution:
                    # Nối các ký tự trong row thành chuỗi nếu nó là list
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
                # Lưu file kết quả của PySAT
                self.save_solution_file(filename, "PySATSolver", pysat_res['solution'])
            else:
                print(f"Failed ({pysat_res['status']})")

            self.record_result(filename, pysat_res, True)

            # --- 2. Run other Solvers ---
            for solver in self.solvers[1:]:
                print(f"  > {solver.name}...", end=" ", flush=True)
                
                # Deepcopy grid để an toàn
                import copy
                grid_copy = copy.deepcopy(grid)
                
                res = self.run_solver_safe(solver, grid_copy, timeout=MAX_TIMEOUT_SECONDS)
                
                # Check đúng sai
                is_correct = False
                if res['status'] == 'OK':
                    if ground_truth_sol:
                        is_correct = self.check_correctness(ground_truth_sol, res['solution'])
                    else:
                        is_correct = True
                    
                    # --- LƯU FILE KẾT QUẢ ---
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
        
        df = pd.DataFrame(self.results)
        
        print("\n--- Summary ---")
        summary = df.groupby("Solver")[["Pass 1min", "Pass 2min", "Pass 5min"]].sum()
        summary["Total"] = df["Input"].nunique()
        print(summary)
        
        df.to_csv(OUTPUT_REPORT_CSV, index=False)
        print(f"\nReport saved to {OUTPUT_REPORT_CSV}")

if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run_all()
    runner.generate_report()