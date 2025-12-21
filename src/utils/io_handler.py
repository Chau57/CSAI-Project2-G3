"""
Input/Output utilities for Hashiwokakero project.

This module handles:
- Reading puzzle input files
- Writing solution grids to output files
- Displaying solutions in console

This module is solver-independent.
"""

from pathlib import Path
from typing import List
import numpy as np


# ----------------------------------------------------------------------
# Input handling
# ----------------------------------------------------------------------

def read_input(filepath: str) -> List[List[int]]:
    """
    Read a Hashiwokakero puzzle from an input file.

    Parameters
    ----------
    filepath : str
        Path to the input file

    Returns
    -------
    List[List[int]]
        2D grid where:
        - 0 represents an empty cell
        - Positive integers represent islands
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    grid: List[List[int]] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Support space- or comma-separated format
            tokens = line.replace(",", " ").split()
            row = [int(token) for token in tokens]
            grid.append(row)

    return grid


def read_input_numpy(filepath: str) -> np.ndarray:
    """
    Read input file and return a NumPy array.

    This function is provided for convenience only.
    Core logic should use Python lists.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    np.ndarray
        2D numpy array of the puzzle grid
    """
    return np.array(read_input(filepath), dtype=int)


# ----------------------------------------------------------------------
# Output handling
# ----------------------------------------------------------------------

def write_output(
    solver_name: str,
    index: int,
    grid: List[List[str]],
    output_root: str = "data/outputs"
) -> None:
    """
    Write solution grid to a solver-specific output directory.

    Output file format:
        outputs/<solver_name>/output-XX.txt

    Parameters
    ----------
    solver_name : str
        Name of the solver (e.g., bruteforce, sat)
    index : int
        Test case index
    grid : List[List[str]]
        Rendered solution grid
    output_root : str, optional
        Root output directory
    """
    solver_dir = Path(output_root) / solver_name
    solver_dir.mkdir(parents='True', exist_ok=True)

    output_path = solver_dir / f"output-{index:02d}.txt"

    with output_path.open("w", encoding="utf-8") as f:
        for row in grid:
            f.write(",".join(row) + "\n")


# ----------------------------------------------------------------------
# Display utilities
# ----------------------------------------------------------------------

def display_solution(grid: List[List[str]]) -> None:
    """
    Print a solution grid to the console.

    Parameters
    ----------
    grid : List[List[str]]
        Rendered solution grid
    """
    print("\n=== Solution ===")
    for row in grid:
        print(" ".join(row))
    print()
