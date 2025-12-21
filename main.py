"""
Hashiwokakero Solver - Main Entry Point
"""

import argparse
import sys
import time
import os
from pathlib import Path
import glob

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.io_handler import read_input, display_solution
from solvers.pysat_solver import PySATSolver
from solvers.backtracking_solver import BacktrackingSolver
from solvers.astar_solver import AStarSolver
from solvers.bruteforce_solver import BruteForceSolver
from solvers.astar_variants import AStarBasicCNF, AStarWeightedCNF, AStarMomsCNF
from benchmark.comparator import compare_solvers_on_single_input

def save_to_file_manual(filepath, grid):
    """
    Save the solution grid to a file in CSV format.
    
    Args:
        filepath (str): Path to the output file
        grid (List[List[int]]): 2D grid representing the solution
        
    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            for row in grid:
                row_str = [str(x) for x in row]
                f.write(",".join(row_str) + "\n")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    """
    Main entry point for Hashiwokakero solver.
    
    Parses command-line arguments, loads the puzzle, selects the appropriate solver,
    runs the solver, and saves/displays the solution.
    """
    parser = argparse.ArgumentParser(description='Hashiwokakero Puzzle Solver')
    
    parser.add_argument('input', help='Path to input file(s).')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-s', '--solver', default='pysat', 
                        choices=['pysat', 'astar', 'astar_basic', 'astar_weighted', 'astar_moms', 
                                 'backtracking', 'bruteforce'],
                        help='Solver algorithm')
    parser.add_argument('-c', '--compare', action='store_true', 
                        help='Compare all solvers on the input')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    input_files = glob.glob(args.input)
    if not input_files:
        print(f"Error: No files found matching '{args.input}'")
        sys.exit(1)
    
    input_file = input_files[0]
    
    try:
        if args.verbose:
            print(f"Reading: {input_file}")
        
        grid = read_input(input_file)
        
        if args.verbose:
            rows = len(grid)
            cols = len(grid[0]) if rows > 0 else 0
            print(f"Grid size: {rows}x{cols}")
            print(f"Running solver: {args.solver}...")
        
        if args.compare:
            compare_solvers_on_single_input(grid, verbose=args.verbose)
            return
        
        solver = None
        
        if args.solver == 'pysat':
            solver = PySATSolver()
            
        elif args.solver == 'backtracking':
            solver = BacktrackingSolver()
            
        elif args.solver == 'astar':
            solver = AStarSolver()
            
        elif args.solver == 'astar_basic':
            solver = AStarBasicCNF()
            
        elif args.solver == 'astar_weighted':
            solver = AStarWeightedCNF()
            
        elif args.solver == 'astar_moms':
            solver = AStarMomsCNF()
            
        elif args.solver == 'bruteforce':
            solver = BruteForceSolver()
        
        start_time = time.time()
        
        if hasattr(solver, 'solve_with_timing'):
            solution = solver.solve_with_timing(grid)
        else:
            solution = solver.solve(grid)
            
        duration = time.time() - start_time
        
        if solution is None:
            print(f"\n❌ {solver.name} FAILED! Time: {duration:.4f}s")
            sys.exit(1)
        else:
            print(f"\n✅ {solver.name} SUCCESS! Time: {duration:.4f}s")
            
        if args.verbose and hasattr(solver, 'print_stats'):
            solver.print_stats()
        
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