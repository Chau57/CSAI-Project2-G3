from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Island:
    """
    Represents an Island in the Hashiwokakero puzzle.
    
    Attributes:
        id (int): Unique identifier for the island.
        row (int): Row index in the grid.
        col (int): Column index in the grid.
        value (int): The required number of bridges connected to this island.
    """
    id: int
    row: int
    col: int
    value: int

    def __repr__(self) -> str:
        return f"Island({self.id}, val={self.value} at {self.row},{self.col})"


@dataclass(frozen=True)
class Edge:
    """
    Represents a potential bridge connection between two islands.
    
    Attributes:
        id (int): Unique identifier for the edge.
        u (int): The ID of the starting island.
        v (int): The ID of the ending island.
        direction (str): Direction of the bridge ('H' for Horizontal, 'V' for Vertical).
        cells (Tuple[Tuple[int, int], ...]): A tuple of (row, col) coordinates 
                                            that the bridge passes through.
    """
    id: int
    u: int
    v: int
    direction: str 
    cells: Tuple[Tuple[int, int], ...]

    def __repr__(self) -> str:
        return f"Edge({self.id}: {self.u}-{self.v} dir={self.direction})"