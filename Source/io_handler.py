"""
I/O handler for Hashiwokakero puzzle.

Provides:
- `parse_input_file(filepath, as_numpy=True)`: read a text input and return a 2D int grid
  (as a NumPy array when `as_numpy=True`).
- `write_output_file(grid, bridges, output_path)`: write an ASCII representation

The parser is permissive: non-integer tokens are treated as 0. The writer
accepts either a Python list-of-lists or a NumPy 2D array.
"""
from pathlib import Path
from typing import Optional, Any

import numpy as np


def parse_input_file(filepath: str, as_numpy: bool = True) -> Any:
    """Parse a simple comma-separated input file into a 2D integer grid.

    Each non-empty line is interpreted as a row. Values are comma-separated.
    Non-integer tokens are treated as 0.

    Args:
        filepath: path to input file
        as_numpy: if True, return a `numpy.ndarray` (dtype=int); otherwise
                  return a Python list of lists.

    Returns:
        `numpy.ndarray` or `list[list[int]]` depending on `as_numpy`.
    """
    p = Path(filepath)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    rows = []
    with p.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = [tok.strip() for tok in line.split(",")]
            row = []
            for tok in parts:
                if tok == "":
                    row.append(0)
                    continue
                try:
                    row.append(int(tok))
                except ValueError:
                    row.append(0)
            rows.append(row)

    if not rows:
        # return empty array/list
        return np.array(rows, dtype=int) if as_numpy else rows

    # Normalize row lengths by padding with zeros if needed
    max_len = max(len(r) for r in rows)
    norm = [r + [0] * (max_len - len(r)) for r in rows]

    if as_numpy:
        return np.array(norm, dtype=int)
    return norm


def _grid_to_lines(grid_arr: np.ndarray) -> list:
    """Convert a 2D integer NumPy array into printable ASCII lines.

    Islands (>0) are printed as their number; empty cells (0) are printed
    as a single space. Cells are separated by a single space.
    """
    lines = []
    for r in grid_arr:
        tokens = [str(int(v)) if v != 0 else " " for v in r]
        lines.append(" ".join(tokens))
    return lines


def write_output_file(grid: Any, bridges: Optional[Any], output_path: str) -> str:
    """Write a simple ASCII output representing the grid and (optionally)
    bridge markers.

    `grid` may be a NumPy array or a list of lists. `bridges` is accepted for
    future use (solver can pass a structure describing bridges). For now the
    function writes the island numbers and blanks for empty cells.

    Returns the path written.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to NumPy array for uniform handling
    if isinstance(grid, list):
        # assume list of lists
        grid_arr = np.array(grid, dtype=int)
    elif isinstance(grid, np.ndarray):
        grid_arr = grid.astype(int)
    else:
        raise TypeError("grid must be a list of lists or a numpy.ndarray")

    lines = _grid_to_lines(grid_arr)

    with out_path.open("w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")

    return str(out_path)
