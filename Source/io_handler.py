"""
I/O handler for Hashiwokakero puzzle.

SIMPLE & CLEAN DESIGN:
- Bridge format: {'from': (r,c), 'to': (r,c), 'count': 1-2}
- Direction is AUTO-DETECTED from coordinates (no need to store!)

Usage:
    grid = parse_input_file("input-01.txt")
    bridges = [
        {'from': (0,1), 'to': (0,3), 'count': 2},
        {'from': (0,1), 'to': (2,1), 'count': 1},
    ]
    write_output_file(grid, bridges, "output-01.txt")
"""
from pathlib import Path
from typing import List, Dict, Tuple, Any
import numpy as np
from helper_01 import *
# ============================================================================
# HELPER: Direction Detection
# ============================================================================

def _get_direction(island1: Tuple[int, int], island2: Tuple[int, int]) -> str:
    """
    Auto-detect bridge direction from island coordinates.
    
    Args:
        island1: (row, col) of first island
        island2: (row, col) of second island
        
    Returns:
        'h' for horizontal, 'v' for vertical
        
    Raises:
        ValueError: If islands are not aligned horizontally or vertically
    """
    r1, c1 = island1
    r2, c2 = island2
    
    if r1 == r2:
        return 'h'
    elif c1 == c2:
        return 'v'
    else:
        raise ValueError(f"Islands at {island1} and {island2} are not aligned")
# ============================================================================
# INPUT PARSING
# ============================================================================

def parse_input_file(filepath: str) -> np.ndarray:
    """
    Parse comma-separated input file into 2D numpy array.
    
    Args:
        filepath: Path to input file
        
    Returns:
        2D numpy array with islands (1-8) and empty cells (0)
        
    Example:
        >>> grid = parse_input_file("input-01.txt")
        >>> print(grid.shape)
        (7, 7)
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
        return np.array([], dtype=int).reshape(0, 0)

    # Normalize row lengths
    max_len = max(len(r) for r in rows)
    norm = [r + [0] * (max_len - len(r)) for r in rows]

    return np.array(norm, dtype=int)


# ============================================================================
# OUTPUT WRITING
# ============================================================================

def write_output_file(grid: np.ndarray, bridges: BridgeList, output_path: str) -> str:
    """
    Write solution to file in project format.
    
    Args:
        grid: Input grid with islands
        bridges: List of bridge dictionaries
                 Format: [{'from': (r,c), 'to': (r,c), 'count': 1-2}, ...]
        output_path: Where to save the output
        
    Returns:
        Absolute path of the saved file
        
    Example:
        >>> grid = parse_input_file("input-01.txt")
        >>> bridges = [
        ...     {'from': (0,1), 'to': (0,3), 'count': 2},
        ...     {'from': (0,1), 'to': (2,1), 'count': 1},
        ... ]
        >>> write_output_file(grid, bridges, "output-01.txt")
    """
    rows, cols = grid.shape
    
    # Initialize output grid with quoted "0" for empty cells
    output_grid = [['"0"' for _ in range(cols)] for _ in range(rows)]
    
    # Place islands first
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] > 0:
                output_grid[r][c] = f'"{grid[r, c]}"'
    
    # Place bridges
    for bridge in bridges:
        island1 = bridge['from']
        island2 = bridge['to']
        count = bridge['count']
        
        r1, c1 = island1
        r2, c2 = island2
        
        # Auto-detect direction
        direction = _get_direction(island1, island2)
        
        if direction == 'h':
            # Horizontal bridge
            symbol = '"="' if count == 2 else '"-"'
            for c in range(min(c1, c2) + 1, max(c1, c2)):
                output_grid[r1][c] = symbol
                
        elif direction == 'v':
            # Vertical bridge
            symbol = '"$"' if count == 2 else '"|"'
            for r in range(min(r1, r2) + 1, max(r1, r2)):
                output_grid[r][c1] = symbol
    
    # Write to file
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with out_path.open("w", encoding="utf-8") as f:
        for row in output_grid:
            line = "[" + ", ".join(row) + "]\n"
            f.write(line)
    
    return str(out_path.absolute())


