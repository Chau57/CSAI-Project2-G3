"""
I/O Handler for reading input files and writing output files
"""
from pathlib import Path
from typing import List, Union
import numpy as np


def read_input(filepath: str) -> np.ndarray:
    """
    Read puzzle input from file
    
    Args:
        filepath: Path to input file
        
    Returns:
        2D numpy array representing the puzzle grid
        
    Format:
        - Each line is a row
        - Numbers separated by spaces or commas
        - Islands are numbers 1-8, empty cells are 0
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    grid = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Support both comma and space separated
            line = line.replace(',', ' ')
            row = [int(x) for x in line.split()]
            grid.append(row)
    
    return np.array(grid, dtype=int)


def write_output(filepath: str, result: List[List[str]]) -> None:
    """
    Write solution to output file
    
    Args:
        filepath: Path to output file
        result: 2D list of strings representing the solution
        
    Format:
        Each line is formatted as: ["char1", "char2", ...]
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in result:
            formatted_row = '["' + '", "'.join(row) + '"]'
            f.write(formatted_row + '\n')


def display_solution(result: List[List[str]]) -> None:
    """
    Display solution in console
    
    Args:
        result: 2D list of strings representing the solution
    """
    print("\n=== Solution ===")
    for row in result:
        print(' '.join(row))
    print()


def read_input_simple(filepath: str) -> List[List[int]]:
    """
    Simple version that returns Python list instead of numpy array
    
    Args:
        filepath: Path to input file
        
    Returns:
        2D list of integers
    """
    grid = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                line = line.replace(',', ' ')
                row = [int(x) for x in line.split()]
                grid.append(row)
    return grid
