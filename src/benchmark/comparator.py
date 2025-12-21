"""
Benchmark comparator for Hashiwokakero solvers.
Provides functionality to compare and benchmark multiple solver implementations
with timeout support and memory tracking (cross-platform compatible).
"""

import sys
import os
import time
import glob
import tracemalloc
import pandas as pd
import threading
import copy
from typing import List, Dict, Any, Optional
from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

INPUT_DIR = os.path.join(PROJECT_ROOT, "data", "inputs")
OUTPUT_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "outputs")

OUTPUT_REPORT_CSV = "benchmark_report.csv"
OUTPUT_LOG_TXT = "log_chay_thuc_te.txt" 

MAX_TIMEOUT_SECONDS = 300 

SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from solvers.pysat_solver import PySATSolver
from solvers.astar_solver import AStarSolver
from solvers.backtracking_solver import BacktrackingSolver
from solvers.bruteforce_solver import BruteForceSolver
from utils.io_handler import read_input
from solvers.astar_variants import AStarBasicCNF, AStarWeightedCNF, AStarMomsCNF


class DualLogger(object):
    """
    Logger that writes output to both terminal and a file simultaneously.
    """
    
    def __init__(self, filename):
        """
        Initialize dual logger.
        
        Args:
            filename (str): Path to the log file
        """
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        """
        Write message to both terminal and log file.
        
        Args:
            message (str): Message to write
        """
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        """Flush both terminal and log file buffers."""
        self.terminal.flush()
        self.log.flush()


class TimeoutException(Exception):
    """Exception raised when a solver execution times out."""
    pass


class SolverRunner:
    """
    Helper class to run a solver in a separate thread with timeout support.
    This provides cross-platform timeout functionality.
    """
    
    def __init__(self, solver, grid):
        """
        Initialize solver runner.
        
        Args:
            solver: Solver instance to run
            grid: Puzzle grid to solve
        """
        self.solver = solver
        self.grid = grid
        self.solution = None
        self.exception = None
        self.thread = None
        
    def run(self):
        """Execute the solver in the current thread."""
        try:
            self.solution = self.solver.solve(self.grid)
        except Exception as e:
            self.exception = e
    
    def start_with_timeout(self, timeout):
        """
        Start solver in a separate thread with timeout.
        
        Args:
            timeout (int): Maximum execution time in seconds
            
        Returns:
            bool: True if completed within timeout, False otherwise
        """
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        self.thread.join(timeout)
        
        return not self.thread.is_alive()


class BenchmarkRunner:
    """
    Main benchmark runner for comparing solver performance.
    """
    
    def __init__(self):
        """Initialize benchmark runner with default solvers."""
        self.solvers = [
            PySATSolver(),   
            AStarBasicCNF(),
            AStarWeightedCNF(),
            AStarMomsCNF(),
            AStarSolver(),
            BacktrackingSolver(),
            BruteForceSolver(),
        ]
        self.results = []

    def run_solver_safe(self, solver, grid, timeout):
        """
        Run a solver with timeout and memory tracking.
        
        Args:
            solver: Solver instance to run
            grid: Puzzle grid to solve
            timeout (int): Maximum execution time in seconds
            
        Returns:
            dict: Dictionary containing solver performance metrics including
                  solver name, time, memory usage, status, solution, and errors
        """
        tracemalloc.start()
        start_time = time.time()
        
        status = "OK"
        solution = None
        error_msg = ""
        
        try:
            runner = SolverRunner(solver, copy.deepcopy(grid))
            completed = runner.start_with_timeout(timeout)
            
            if not completed:
                status = "TIMEOUT"
            elif runner.exception is not None:
                status = "ERROR"
                error_msg = str(runner.exception)
            else:
                solution = runner.solution
                if solution is None:
                    status = "NO_SOL"
                    
        except Exception as e:
            status = "ERROR"
            error_msg = str(e)
        finally:
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
        """
        Check if test solution matches reference solution.
        
        Args:
            ref_solution: Reference solution grid
            test_solution: Test solution grid to compare
            
        Returns:
            bool: True if solutions match, False otherwise
        """
        if ref_solution is None and test_solution is None: 
            return True
        if ref_solution is None or test_solution is None: 
            return False
        
        rows = len(ref_solution)
        cols = len(ref_solution[0])
        for r in range(rows):
            for c in range(cols):
                if ref_solution[r][c] != test_solution[r][c]:
                    return False
        return True

    def save_solution_file(self, input_filename, solver_name, solution):
        """
        Save solution to output file.
        
        Args:
            input_filename (str): Name of input file
            solver_name (str): Name of solver
            solution: Solution grid to save
        """
        if solution is None: 
            return

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
        """
        Run benchmark on all input files in the input directory.
        Tests all configured solvers and generates performance report.
        """
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

            print(f"  > PySATSolver (Reference)...", end=" ", flush=True)
            pysat_res = self.run_solver_safe(self.solvers[0], grid, timeout=60)
            
            ground_truth_sol = pysat_res['solution']
            if pysat_res['status'] == 'OK':
                print(f"Done ({pysat_res['time']:.4f}s)")
                self.save_solution_file(filename, "PySATSolver", pysat_res['solution'])
            else:
                print(f"Failed ({pysat_res['status']})")

            self.record_result(filename, pysat_res, True)

            for solver in self.solvers[1:]:
                print(f"  > {solver.name}...", end=" ", flush=True)
                
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
        """
        Record benchmark result for a single solver run.
        
        Args:
            filename (str): Input filename
            res (dict): Result dictionary from run_solver_safe
            is_correct (bool): Whether the solution is correct
        """
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
        """
        Generate and save benchmark report to CSV file.
        Includes summary statistics and per-test results.
        """
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

def compare_solvers_on_single_input(grid, verbose=False):
    """
    Compare all solvers on a single input grid.
    
    Args:
        grid: The puzzle grid to solve
        verbose (bool): Print detailed output
        
    Returns:
        list: List of result dictionaries containing performance metrics
    """
    solvers = [
        PySATSolver(),
        AStarSolver(),
        AStarBasicCNF(),
        AStarWeightedCNF(),
        AStarMomsCNF(),
        BacktrackingSolver(),
        BruteForceSolver(),
    ]
    
    print("\n" + "="*80)
    print("SOLVER COMPARISON")
    print("="*80)
    
    results = []
    reference_solution = None
    
    runner = BenchmarkRunner()
    
    for solver in solvers:
        if verbose:
            print(f"\nRunning {solver.name}...")
        else:
            print(f"\nRunning {solver.name}...", end=" ", flush=True)
        
        grid_copy = copy.deepcopy(grid)
        
        result = runner.run_solver_safe(solver, grid_copy, timeout=MAX_TIMEOUT_SECONDS)
        
        if result['status'] == 'OK' and reference_solution is None:
            reference_solution = result['solution']
        
        is_correct = False
        if result['status'] == 'OK' and reference_solution is not None:
            is_correct = runner.check_correctness(reference_solution, result['solution'])
        
        result['correct'] = is_correct
        results.append(result)
        
        if verbose:
            print(f"  Status: {result['status']}")
            print(f"  Time: {result['time']:.4f}s")
            print(f"  Memory: {result['memory_mb']:.4f} MB")
            print(f"  Correct: {is_correct}")
            if result['error']:
                print(f"  Error: {result['error']}")
        else:
            print(f"{result['status']} | Time: {result['time']:.4f}s | Memory: {result['memory_mb']:.4f}MB | Correct: {is_correct}")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"{'Solver':<25} {'Status':<15} {'Time (s)':<12} {'Memory (MB)':<12} {'Correct':<10}")
    print("-"*80)
    
    for result in results:
        print(f"{result['solver']:<25} {result['status']:<15} "
              f"{result['time']:<12.4f} {result['memory_mb']:<12.4f} {str(result['correct']):<10}")
    
    print("="*80)
    
    return results


if __name__ == "__main__":
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    log_file_path = os.path.join(OUTPUT_BASE_DIR, OUTPUT_LOG_TXT)

    sys.stdout = DualLogger(log_file_path)

    print(f"Logging started. Log file: {log_file_path}")

    runner = BenchmarkRunner()
    runner.run_all()
    runner.generate_report()