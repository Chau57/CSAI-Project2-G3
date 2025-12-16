================================================================================
Hashiwokakero Puzzle Solver - Instructions
================================================================================

HOW TO RUN:

1. Install dependencies:
   pip install -r requirements.txt

2. Place input files in the Inputs/ directory (e.g., input-01.txt)

3. Run the solver with:
   python main.py --input Inputs/input-01.txt --method sat

4. Available methods:
   - sat         : SAT solver using PySAT library
   - astar       : A* search algorithm
   - backtracking: Backtracking algorithm
   - bruteforce  : Brute-force algorithm (baseline)

5. Solutions will be generated in the Outputs/ directory

INPUT FORMAT:
- Each line contains comma-separated values
- 0 represents empty space
- Numbers 1-8 represent islands with that many required bridges

Example:
0, 2, 0, 5, 0
0, 0, 0, 0, 0
4, 0, 2, 0, 2

OUTPUT FORMAT:
ASCII representation with:
- | : One vertical bridge
- $ : Two vertical bridges
- - : One horizontal bridge
- = : Two horizontal bridges
- Numbers: Islands

================================================================================
