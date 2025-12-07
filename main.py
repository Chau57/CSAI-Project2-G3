"""
Hashiwokakero Solver - Main Entry Point

This is the main script for solving Hashiwokakero puzzles using various algorithms.

Usage:
    python main.py <input_file> [options]
    
Examples:
    # Solve with PySAT (default)
    python main.py data/inputs/input-01.txt
    
    # Specify output file
    python main.py data/inputs/input-01.txt -o data/outputs/output-01.txt
    
    # Use specific solver
    python main.py data/inputs/input-01.txt -s astar
    
    # Compare all solvers
    python main.py data/inputs/input-01.txt --compare
    
    # Benchmark on multiple files
    python main.py data/inputs/*.txt --benchmark
"""

import argparse
import sys
from pathlib import Path
import glob

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.io_handler import read_input, write_output, display_solution
from solvers.pysat_solver import PySATSolver
# from solvers.astar_solver import AStarSolver
# from solvers.backtracking_solver import BacktrackingSolver
# from solvers.bruteforce_solver import BruteforceSolver
from benchmark.comparator import compare_solvers, print_comparison_table, benchmark_on_multiple_inputs


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Hashiwokakero Puzzle Solver',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'input',
        help='Path to input file(s). Use wildcards for multiple files.'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: print to console)'
    )
    
    parser.add_argument(
        '-s', '--solver',
        default='pysat',
        choices=['pysat', 'astar', 'backtracking', 'bruteforce'],
        help='Solver algorithm to use (default: pysat)'
    )
    
    parser.add_argument(
        '-c', '--compare',
        action='store_true',
        help='Compare all available solvers'
    )
    
    parser.add_argument(
        '-b', '--benchmark',
        action='store_true',
        help='Run benchmark on multiple input files'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Handle wildcards in input path
    input_files = glob.glob(args.input)
    if not input_files:
        print(f"Error: No files found matching '{args.input}'")
        sys.exit(1)
    
    # Benchmark mode: process multiple files
    if args.benchmark and len(input_files) > 1:
        benchmark_on_multiple_inputs(input_files, verbose=args.verbose)
        return
    
    # Single file mode
    input_file = input_files[0]
    
    try:
        # Read input
        if args.verbose:
            print(f"Reading: {input_file}")
        
        grid = read_input(input_file)
        
        if args.verbose:
            print(f"Grid size: {grid.shape[0]}x{grid.shape[1]}")
            print("Solving puzzle...")
        
        # Compare mode: test all solvers
        if args.compare:
            results = compare_solvers(grid, verbose=args.verbose)
            print_comparison_table(results)
            
            # Use solution from first successful solver for output
            for solver_name, result in results.items():
                if result['success']:
                    solution = result['solution']
                    break
            else:
                print("\n❌ No solver found a solution!")
                sys.exit(1)
        
        # Single solver mode
        else:
            # Select solver
            if args.solver == 'pysat':
                solver = PySATSolver()
            elif args.solver == 'astar':
                print("Error: A* solver not yet implemented")
                sys.exit(1)
            elif args.solver == 'backtracking':
                print("Error: Backtracking solver not yet implemented")
                sys.exit(1)
            elif args.solver == 'bruteforce':
                print("Error: Brute force solver not yet implemented")
                sys.exit(1)
            else:
                print(f"Error: Unknown solver '{args.solver}'")
                sys.exit(1)
            
            # Solve
            solution = solver.solve_with_timing(grid)
            
            if solution is None:
                print(f"\n❌ {solver.name} could not find a solution!")
                sys.exit(1)
            
            if args.verbose:
                solver.print_stats()
        
        # Output solution
        if args.output:
            write_output(args.output, solution)
            print(f"\n✅ Solution written to: {args.output}")
        else:
            display_solution(solution)
        
        print("\n✅ Puzzle solved successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
