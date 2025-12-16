"""
Puzzle definition for Hashiwokakero (Bridges) problem.

This module is responsible for:
- Parsing the input grid
- Identifying islands
- Generating all valid edges (possible bridge connections)

It does NOT solve the puzzle.
"""

from typing import List, Dict, Tuple
import numpy as np

from .variables import Island, Edge


class Puzzle:
    """
    Represents a Hashiwokakero puzzle instance.

    Attributes
    ----------
    grid : np.ndarray
        2D grid representation of the puzzle
    rows : int
        Number of rows
    cols : int
        Number of columns
    islands : List[Island]
        List of all islands found in the grid
    edges : List[Edge]
        List of all valid edges (possible bridge connections)
    """

    def __init__(self, grid: List[List[int]]):
        """
        Initialize the puzzle from a grid.

        Parameters
        ----------
        grid : List[List[int]]
            2D list where 0 represents empty cell,
            and positive integers represent islands with required degrees.
        """
        self.grid = np.array(grid, dtype=int)
        self.rows, self.cols = self.grid.shape

        self.islands: List[Island] = []
        self.edges: List[Edge] = []

        self._find_islands()
        self._find_edges()

    # ------------------------------------------------------------------
    # Island detection
    # ------------------------------------------------------------------

    def _find_islands(self) -> None:
        """
        Scan the grid and create Island objects for all island cells.
        """
        island_id = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] > 0:
                    self.islands.append(
                        Island(
                            id=island_id,
                            row=r,
                            col=c,
                            value=int(self.grid[r, c])
                        )
                    )
                    island_id += 1

    # ------------------------------------------------------------------
    # Edge generation
    # ------------------------------------------------------------------

    def _find_edges(self) -> None:
        """
        Generate all valid edges between islands.

        An edge exists between two islands if:
        - They are aligned horizontally or vertically
        - All cells between them are empty
        - No other island lies between them

        Each edge represents a potential bridge (0, 1, or 2).
        """
        edge_id = 0

        # Map island position to Island object for O(1) lookup
        island_map: Dict[Tuple[int, int], Island] = {
            (island.row, island.col): island for island in self.islands
        }

        for island in self.islands:
            r, c = island.row, island.col

            # ----------------------------------------------------------
            # Look RIGHT (horizontal edge)
            # ----------------------------------------------------------
            cells = []
            cc = c + 1
            while cc < self.cols and self.grid[r, cc] == 0:
                cells.append((r, cc))
                cc += 1

            if cc < self.cols and (r, cc) in island_map:
                self.edges.append(
                    Edge(
                        id=edge_id,
                        u=island.id,
                        v=island_map[(r, cc)].id,
                        direction='H',
                        cells=tuple(cells)
                    )
                )
                edge_id += 1

            # ----------------------------------------------------------
            # Look DOWN (vertical edge)
            # ----------------------------------------------------------
            cells = []
            rr = r + 1
            while rr < self.rows and self.grid[rr, c] == 0:
                cells.append((rr, c))
                rr += 1

            if rr < self.rows and (rr, c) in island_map:
                self.edges.append(
                    Edge(
                        id=edge_id,
                        u=island.id,
                        v=island_map[(rr, c)].id,
                        direction='V',
                        cells=tuple(cells)
                    )
                )
                edge_id += 1

    # ------------------------------------------------------------------
    # Debug / visualization helpers
    # ------------------------------------------------------------------

    def summary(self) -> None:
        """
        Print a human-readable summary of the puzzle.
        """
        print("Islands:")
        for island in self.islands:
            print(island)

        print("\nEdges:")
        for edge in self.edges:
            print(edge)
