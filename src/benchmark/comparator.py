"""
Benchmark and compare different solver algorithms
"""
from typing import Dict, Any, List
import time
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from solvers.pysat_solver import PySATSolver
# from solvers.astar_solver import AStarSolver
# from solvers.backtracking_solver import BacktrackingSolver
# from solvers.bruteforce_solver import BruteforceSolver


def compare_solvers(grid: Any, verbose: bool = True) -> Dict[str, Dict[str, Any]]:
    """
    Compare performance of different solvers on the same puzzle
    
    Args:
        grid: The puzzle grid to solve
        verbose: If True, print progress information
        
    Returns:
        Dictionary with results for each solver:
        {
            'PySATSolver': {
                'time': 0.123,
                'success': True,
                'nodes_explored': 1000,
                'solution': [...],
                'error': None
            },
            ...
        }
    """
    results = {}
    
    # List of available solvers (uncomment as they are implemented)
    solvers = [
        PySATSolver(),
        # AStarSolver(),          # TODO: Uncomment when implemented
        # BacktrackingSolver(),    # TODO: Uncomment when implemented
        # BruteforceSolver(),      # TODO: Uncomment when implemented
    ]
    
    for solver in solvers:
        if verbose:
            print(f"\n{'='*60}")
            print(f"Testing: {solver.name}")
            print(f"{'='*60}")
        
        try:
            start_time = time.time()
            solution = solver.solve(grid)
            end_time = time.time()
            
            elapsed = end_time - start_time
            
            results[solver.name] = {
                'time': elapsed,
                'success': solution is not None,
                'nodes_explored': solver.nodes_explored,
                'solution': solution,
                'error': None
            }
            
            if verbose:
                print(f"✓ Completed in {elapsed:.4f}s")
                print(f"  Success: {solution is not None}")
                print(f"  Nodes explored: {solver.nodes_explored}")
                
        except NotImplementedError as e:
            results[solver.name] = {
                'time': 0,
                'success': False,
                'nodes_explored': 0,
                'solution': None,
                'error': f"Not implemented: {str(e)}"
            }
            if verbose:
                print(f"⚠ Not implemented yet")
                
        except Exception as e:
            results[solver.name] = {
                'time': 0,
                'success': False,
                'nodes_explored': 0,
                'solution': None,
                'error': str(e)
            }
            if verbose:
                print(f"✗ Error: {str(e)}")
    
    return results


def print_comparison_table(results: Dict[str, Dict[str, Any]]) -> None:
    """
    Print a formatted comparison table
    
    Args:
        results: Results from compare_solvers()
    """
    print("\n" + "="*80)
    print("SOLVER COMPARISON SUMMARY")
    print("="*80)
    print(f"{'Solver':<20} {'Time (s)':<12} {'Success':<10} {'Nodes':<15} {'Status'}")
    print("-"*80)
    
    for solver_name, result in results.items():
        time_str = f"{result['time']:.4f}" if result['success'] else "N/A"
        success_str = "✓" if result['success'] else "✗"
        nodes_str = str(result['nodes_explored']) if result['success'] else "N/A"
        status = "OK" if result['success'] else (result['error'] or "Failed")
        
        # Truncate status if too long
        if len(status) > 25:
            status = status[:22] + "..."
        
        print(f"{solver_name:<20} {time_str:<12} {success_str:<10} {nodes_str:<15} {status}")
    
    print("="*80)
    
    # Find fastest solver
    successful_solvers = [(name, res) for name, res in results.items() if res['success']]
    if successful_solvers:
        fastest = min(successful_solvers, key=lambda x: x[1]['time'])
        print(f"\n🏆 Fastest solver: {fastest[0]} ({fastest[1]['time']:.4f}s)")


def benchmark_on_multiple_inputs(input_files: List[str], verbose: bool = False) -> None:
    """
    Run benchmark on multiple input files
    
    Args:
        input_files: List of paths to input files
        verbose: If True, print detailed information
    """
    from utils.io_handler import read_input
    
    print("\n" + "="*80)
    print("MULTI-FILE BENCHMARK")
    print("="*80)
    
    all_results = {}
    
    for input_file in input_files:
        print(f"\n📁 Processing: {Path(input_file).name}")
        
        try:
            grid = read_input(input_file)
            results = compare_solvers(grid, verbose=verbose)
            all_results[input_file] = results
            
            if not verbose:
                # Print summary for this file
                successful = sum(1 for r in results.values() if r['success'])
                print(f"   Solvers succeeded: {successful}/{len(results)}")
                
        except Exception as e:
            print(f"   ✗ Error reading file: {str(e)}")
    
    # Print overall statistics
    print("\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    
    solver_names = list(next(iter(all_results.values())).keys())
    
    for solver_name in solver_names:
        times = [res[solver_name]['time'] for res in all_results.values() 
                if res[solver_name]['success']]
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            success_rate = len(times) / len(all_results) * 100
            
            print(f"\n{solver_name}:")
            print(f"  Success rate: {success_rate:.1f}%")
            print(f"  Average time: {avg_time:.4f}s")
            print(f"  Min time: {min_time:.4f}s")
            print(f"  Max time: {max_time:.4f}s")
        else:
            print(f"\n{solver_name}: No successful runs")
