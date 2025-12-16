from core.puzzle import Puzzle
from core.constraints import check_degree, check_crossing, check_connected

grid = [
    [0, 2, 0, 5, 0],
    [0, 0, 0, 0, 0],
    [3, 0, 0, 0, 4]
]

puzzle = Puzzle(grid)
state = {0: 1, 1: 2}

print(check_degree(puzzle, state))     # True/False
print(check_crossing(puzzle, state))   # True
print(check_connected(puzzle, state))  # True
