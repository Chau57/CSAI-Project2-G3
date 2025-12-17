"""
Hashiwokakero Solver - Main Entry Point
"""

import argparse
import sys
import time
import os
from pathlib import Path
import glob

from src.utils.io_handler import read_input, display_solution

# --- 1. IMPORT ĐẦY ĐỦ CÁC SOLVER ---
from src.solvers.pysat_solver import PySATSolver
from src.solvers.backtracking_solver import BacktrackingSolver
from src.solvers.astar_solver import AStarSolver
from src.solvers.bruteforce_solver import BruteForceSolver
from src.benchmark.comparator import compare_solvers, print_comparison_table, benchmark_on_multiple_inputs

def save_to_file_manual(filepath, grid):
    """Hàm lưu file thủ công để đảm bảo chạy được mọi lúc"""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            for row in grid:
                # Chuyển list thành string nếu cần
                row_str = [str(x) for x in row]
                f.write(",".join(row_str) + "\n") # Dùng dấu phẩy cho đúng chuẩn nhóm
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Hashiwokakero Puzzle Solver')
    
    parser.add_argument('input', help='Path to input file(s).')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-s', '--solver', default='pysat', 
                        choices=['pysat', 'astar', 'backtracking', 'bruteforce'],
                        help='Solver algorithm')
    parser.add_argument('-c', '--compare', action='store_true', help='Compare solvers')
    parser.add_argument('-b', '--benchmark', action='store_true', help='Run benchmark')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    input_files = glob.glob(args.input)
    if not input_files:
        print(f"Error: No files found matching '{args.input}'")
        sys.exit(1)
    
    if args.benchmark and len(input_files) > 1:
        benchmark_on_multiple_inputs(input_files, verbose=args.verbose)
        return
    
    input_file = input_files[0]
    
    try:
        # 1. Đọc Input
        if args.verbose:
            print(f"Reading: {input_file}")
        
        grid = read_input(input_file)
        
        if args.verbose:
            rows = len(grid)
            cols = len(grid[0]) if rows > 0 else 0
            print(f"Grid size: {rows}x{cols}")
            print(f"Running solver: {args.solver}...")
        
        # 2. Chọn Solver
        if args.compare:
            results = compare_solvers(grid, verbose=args.verbose)
            print_comparison_table(results)
            return

        solver = None
        
        # --- 2. SỬA LOGIC CHỌN SOLVER TẠI ĐÂY ---
        if args.solver == 'pysat':
            solver = PySATSolver()
            
        elif args.solver == 'backtracking':
            solver = BacktrackingSolver()
            
        elif args.solver == 'astar':
            solver = AStarSolver()  # <--- Đã thêm dòng này để chạy A*
            
        elif args.solver == 'bruteforce':
            solver = BruteForceSolver()
        # ----------------------------------------
        
        # 3. Chạy Solver và ĐO THỜI GIAN
        start_time = time.time()
        
        # Gọi hàm solve
        if hasattr(solver, 'solve_with_timing'):
            solution = solver.solve_with_timing(grid)
        else:
            solution = solver.solve(grid)
            
        duration = time.time() - start_time
        
        # 4. In kết quả thời gian
        if solution is None:
            print(f"\n❌ {solver.name} FAILED! Time: {duration:.4f}s")
            sys.exit(1)
        else:
            print(f"\n✅ {solver.name} SUCCESS! Time: {duration:.4f}s")
            
        if args.verbose and hasattr(solver, 'print_stats'):
            solver.print_stats()
        
        # 5. Xử lý Lưu File (Tự động nếu không có -o)
        save_path = args.output
        if not save_path:
            input_path_obj = Path(input_file)
            output_filename = input_path_obj.name.replace("input", "output")
            save_path = f"data/outputs/{solver.name}/{output_filename}"
            
        if save_to_file_manual(save_path, solution):
            print(f"📄 Solution saved to: {save_path}")
        
        if not args.output and not args.verbose:
            display_solution(solution)

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()