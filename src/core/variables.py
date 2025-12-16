# src/core/variables.py

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Island:
    id: int
    row: int
    col: int
    value: int


@dataclass(frozen=True)
class Edge:
    id: int
    u: int        # island id
    v: int        # island id
    direction: str  # 'H' or 'V'
    cells: Tuple[Tuple[int, int], ...]  # cells between u and v
