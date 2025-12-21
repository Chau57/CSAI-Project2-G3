from typing import List, Dict, Tuple, Set
import numpy as np

from .variables import Island, Edge

class Puzzle:
    """
    The main class representing a Hashiwokakero puzzle instance.
    
    It parses the input grid, identifies islands, generates all valid potential 
    edges, and pre-calculates structural information like edge intersections 
    and adjacency lists.
    """

    def __init__(self, grid: List[List[int]]):
        """
        Initialize the puzzle.

        Args:
            grid (List[List[int]]): 2D integer matrix where 0 is empty 
                                    and >0 represents an island's value.
        """
        self.grid = np.array(grid, dtype=int)
        self.rows, self.cols = self.grid.shape

        self.islands: List[Island] = []
        self.edges: List[Edge] = []
        
        # Pre-computed set of intersecting edge pairs (id1, id2).
        # Essential for checking the "Non-crossing" constraint efficiently.
        self.intersections: Set[Tuple[int, int]] = set()

        # Adjacency list: island_id -> List[Edge].
        # Optimized for A* and Backtracking traversal.
        self.adj: Dict[int, List[Edge]] = {}

        self._find_islands()
        self._find_edges()
        self._find_intersections()
        self._build_adjacency()

    def _find_islands(self) -> None:
        """Identify all islands in the grid."""
        island_id = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] > 0:
                    self.islands.append(
                        Island(island_id, r, c, int(self.grid[r, c]))
                    )
                    island_id += 1

    def _find_edges(self) -> None:
        """
        Generate all valid potential bridges (edges).
        
        Scans strictly RIGHT and DOWN from each island to avoid 
        duplicate edges in an undirected graph context.
        """
        edge_id = 0
        island_map = {(isl.row, isl.col): isl for isl in self.islands}

        for island in self.islands:
            r, c = island.row, island.col

            # 1. Look RIGHT (Horizontal)
            cc = c + 1
            cells = []
            while cc < self.cols and self.grid[r, cc] == 0:
                cells.append((r, cc))
                cc += 1
            if cc < self.cols and (r, cc) in island_map:
                neighbor = island_map[(r, cc)]
                self.edges.append(Edge(edge_id, island.id, neighbor.id, 'H', tuple(cells)))
                edge_id += 1

            # 2. Look DOWN (Vertical)
            rr = r + 1
            cells = []
            while rr < self.rows and self.grid[rr, c] == 0:
                cells.append((rr, c))
                rr += 1
            if rr < self.rows and (rr, c) in island_map:
                neighbor = island_map[(rr, c)]
                self.edges.append(Edge(edge_id, island.id, neighbor.id, 'V', tuple(cells)))
                edge_id += 1

    def _find_intersections(self) -> None:
        """
        Identify pairs of edges that cross each other.
        
        A Horizontal edge H and a Vertical edge V intersect if:
        - V's column is within H's column range.
        - H's row is within V's row range.
        
        Stores pairs (id1, id2) in self.intersections.
        """
        h_edges = [e for e in self.edges if e.direction == 'H']
        v_edges = [e for e in self.edges if e.direction == 'V']

        for he in h_edges:
            # Horizontal edge: same row, spanning cols [c_min, c_max]
            r_h = he.cells[0][0]
            c_min = min(he.cells[0][1], he.cells[-1][1])
            c_max = max(he.cells[0][1], he.cells[-1][1])

            for ve in v_edges:
                # Vertical edge: same col, spanning rows [r_min, r_max]
                c_v = ve.cells[0][1]
                r_min = min(ve.cells[0][0], ve.cells[-1][0])
                r_max = max(ve.cells[0][0], ve.cells[-1][0])

                if (c_min < c_v < c_max) and (r_min < r_h < r_max):
                    self.intersections.add((he.id, ve.id))

    def _build_adjacency(self) -> None:
        """Construct an adjacency map for O(1) edge lookup per island."""
        self.adj = {island.id: [] for island in self.islands}
        for edge in self.edges:
            self.adj[edge.u].append(edge)
            self.adj[edge.v].append(edge)