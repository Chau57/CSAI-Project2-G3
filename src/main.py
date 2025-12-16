"""
Main entry point for the Hashiwokakero project.

This script:
- Loads all input test cases
- Runs multiple solvers on each puzzle
- Writes solver-specific outputs
"""

from pathlib import Path
from typing import List

from core.puzzle import Puzzle
from utils.io_handler import read_input, write_output
from utils.renderer import render_solution

from solvers.bruteforce_solver import BruteForceSolver
# from solvers.backtracking_solver import BacktrackingSolver
# from solvers.astar_solver import AStarSolver
# from solvers.pysat_solver import PySATSolver


# ----------------------------------------------------------------------
# Solver registry
# ----------------------------------------------------------------------

SOLVERS = [
    BruteForceSolver(),
    # BacktrackingSolver(),
    # AStarSolver(),
    # PySATSolver(),
]


# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------

def load_inputs(input_dir: str) -> List[Path]:
    """
    Load and sort all input files from a directory.
    """
    return sorted(Path(input_dir).glob("input-*.txt"))


def main() -> None:
    input_dir = "data/inputs"
    input_files = load_inputs(input_dir)

    if not input_files:
        print("No input files found.")
        return

    for index, input_path in enumerate(input_files):
        print(f"\n=== Processing {input_path.name} ===")

        grid = read_input(str(input_path))
        puzzle = Puzzle(grid)

        for solver in SOLVERS:
            print(f"→ Running solver: {solver.name}")

            state = solver.solve(puzzle)

            if state is None:
                print(f"  ✗ No solution found")
                continue

            solution_grid = render_solution(puzzle, state)

            write_output(
                solver_name=solver.name,
                index=index,
                grid=solution_grid
            )

            print(f"  ✓ Output written to data/outputs/{solver.name}/output-{index:02d}.txt")


if __name__ == "__main__":
    main()
