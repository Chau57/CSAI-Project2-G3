from pathlib import Path
from typing import List, Dict, Tuple, Any
import numpy as np

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

Island = Tuple[int, int]  # (row, col)
Bridge = Dict[str, Any]   # {'from': Island, 'to': Island, 'count': int}
BridgeList = List[Bridge]

# ============================================================================
# HELPER: Create Bridge
# ============================================================================

def create_bridge(island1: Island, island2: Island, count: int) -> Bridge:
    """
    Create a bridge dictionary.
    
    Args:
        island1: Starting island (row, col)
        island2: Ending island (row, col)
        count: Number of bridges (1 or 2)
        
    Returns:
        Bridge dictionary: {'from': (r,c), 'to': (r,c), 'count': int}
        
    Example:
        >>> bridge = create_bridge((0, 1), (0, 3), 2)
        >>> print(bridge)
        {'from': (0, 1), 'to': (0, 3), 'count': 2}
    """
    r1, c1 = island1
    r2, c2 = island2
    
    # Validate alignment (must be same row OR same column)
    if r1 != r2 and c1 != c2:
        raise ValueError(f"Islands must be aligned: {island1} and {island2}")
    
    if count not in [1, 2]:
        raise ValueError(f"Bridge count must be 1 or 2, got {count}")
    
    return {
        'from': island1,
        'to': island2,
        'count': count
    }


# ============================================================================
# HELPER: Detect Direction
# ============================================================================

def _get_direction(island1: Island, island2: Island) -> str:
    """
    Auto-detect bridge direction from island coordinates.
    
    Args:
        island1: First island (row, col)
        island2: Second island (row, col)
        
    Returns:
        'h' for horizontal, 'v' for vertical
    """
    r1, c1 = island1
    r2, c2 = island2
    
    if r1 == r2:
        return 'h'  # Same row = horizontal
    elif c1 == c2:
        return 'v'  # Same column = vertical
    else:
        raise ValueError(f"Islands not aligned: {island1} and {island2}")

