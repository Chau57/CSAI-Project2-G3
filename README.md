# Hashiwokakero Puzzle Solver - CSAI-Project2-G3
-----

## 1\. Introduction

Hashiwokakero (also known as Bridges or Hashi) is a logic puzzle published by Nikoli that challenges players to connect numbered islands with specific rules.

This project explores Hashiwokakero as a **Constraint Satisfaction Problem (CSP)**. The primary objective is to develop a solver using **Conjunctive Normal Form (CNF)** logic and compare its performance against traditional search algorithms.

The project integrates:

  - **Logical Modeling:** Encoding puzzle constraints into CNF.
  - **SAT Solving:** Using the PySAT library to infer results.
  - **Heuristic Search:** Implementing the $A^{*}$ algorithm.
  - **Baseline Comparison:** Implementing Brute-force and Backtracking algorithms for performance benchmarking.

-----

## 2\. Objectives

The project is designed to fulfill the following academic requirements:

1.  **Define Logical Variables:** Assign logical variables to the grid matrix.
2.  **Formulate CNF Constraints:** Generate constraint clauses for bridge placement and connectivity, ensuring duplicate clauses are removed.
3.  **Automate Solving:**
      * Implement an automated CNF generator.
      * Use the `pysat` library to find the model for variables.
      * Implement $A^{*}$ search without using external search libraries.
4.  **Performance Evaluation:** Compare the speed and efficiency of the logic-based approach against Brute-force and Backtracking methods.

-----

## 3\. Directory Structure

The project directory is organized according to the submission requirements:

```text
StudentID1_StudentID2_.../
│
├── Docs/
│   ├── Report.pdf               # Detailed explanation of algorithms and results
│   ├── References_01.pdf        # Academic references
│   └── References_02.pdf
│
├── Source/
│   ├── Inputs/                  # Input text files (e.g., input-01.txt)
│   ├── Outputs/                 # Generated solutions
│   ├── main.py                  # Main entry point for the program
│   ├── helper_01.py             # Helper functions/modules
│   ├── helper_02.py
│   ├── requirements.txt         # List of required libraries
│   └── README.txt               # Instructions on how to run source code
│
└── [Video Demo Link in Report]  # Demonstration of the running process
```
-----

## 4\. Prerequisites & Installation

### System Requirements

  - **Language:** Python 3.7 or later.
  - **Libraries:** Standard libraries and `python-sat` (PySAT).

### Installation

1.  Navigate to the `Source` directory.
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
-----

## 5\. Methodology

### 5.1 Logic & CNF (SAT Approach)

We formulate the puzzle rules into CNF clauses. The solver ensures:

  - Bridges connect distinct islands via straight lines.
  - Bridges do not cross other bridges or islands.
  - Bridges run only perpendicularly.
  - At most two bridges connect any pair of islands.
  - The bridge count matches the island number.
  - All islands form a single connected group.

### 5.2 Search Algorithms

  - **A\* Search:** Uses a heuristic function to guide the bridge placement process efficiently.
  - **Backtracking:** A systematic depth-first search to find valid configurations.
  - **Brute-force:** An exhaustive search used as a baseline to compare speed and complexity.

-----

## 6\. Input and Output Format

### Input Format

The input files are named `input-xx.txt`. The grid uses `0` for empty spaces and numbers (1-8) for islands.
*Example:*

```text
0, 2, 0, 5, 0
0, 0, 0, 0, 0
4, 0, 2, 0, 2
...
```

### Output Format

The solution is visualized using ASCII characters:

  - `|` : One vertical bridge
  - `$` : Two vertical bridges
  - `-` : One horizontal bridge (represented as empty string `""` or `-` depending on parsing)
  - `=` : Two horizontal bridges

*Example output representation:*

```text
["0", "2", "=", "5", "-", "2"]
["|", " ", " ", "|", " ", " "]
["4", "=", "2", "$", "2", " "]
...
```

-----

## 7\. Usage

To run the solver, execute the `main.py` script from the `Source` directory.

**Command Syntax:**

```bash
python main.py --input <path_to_input_file> --method <algorithm>
```

*Note: Refer to `main.py` arguments for specific implementation details.*

-----

## 8\. Experimental Evaluation

The algorithms are evaluated using a set of at least 10 input files ranging in size from $7\times7$ to $20\times20$.

**Assessment Criteria:**

  - **Correctness:** Ability to solve constraints correctly.
  - **Speed:** Comparison of running time between PySAT, A\*, Backtracking, and Brute-force.
  - **Scalability:** Performance on larger grids (e.g., $13\times13$, $20\times20$).
  - This project is a group assignment for CSC14003.
  - Plagiarism or cheating results in a 0 grade.
  - AI-generated content in the report is limited to under 30%.
