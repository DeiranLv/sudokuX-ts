"""
This module provides the initial solution generator for Sudoku puzzles.
It fills each row with missing numbers randomly, ensuring each row contains 1..9 without repeats,
while preserving the fixed (given) cells. Used for generating starting states for optimization algorithms.
"""
import random
from typing import List, Optional
from sudoku import Grid, fixedMask

def initialSolution(puzzle: Grid, seed: Optional[int] = None) -> Grid:
    """Generate initial solution with valid rows.
       Fixed cells (non-zero) are preserved.
       For empty puzzles: fills each row with 1-9 randomly (row-valid only).
       For partially filled puzzles: attempts to respect all constraints where possible."""
    if seed is not None:
        random.seed(seed)
    grid = [row[:] for row in puzzle]
    fixed = [[cell != 0 for cell in row] for row in puzzle]

    # Check if the puzzle is fully empty
    is_empty = all(cell == 0 for row in puzzle for cell in row)
    if is_empty:
        # For empty puzzles: just fill each row with a random permutation of 1-9
        # This gives us a row-valid starting point with conflicts to resolve
        for i in range(9):
            nums = list(range(1, 10))
            random.shuffle(nums)
            grid[i] = nums
        return grid

    # Fallback: for partially filled puzzles, use the previous logic
    for i in range(9):
        for j in range(9):
            if not fixed[i][j]:
                row_vals = set(grid[i])
                col_vals = set(grid[x][j] for x in range(9))
                # Block values
                block_r, block_c = (i // 3) * 3, (j // 3) * 3
                block_vals = set(grid[block_r + bi][block_c + bj] for bi in range(3) for bj in range(3))
                diag1_vals = set()
                diag2_vals = set()
                if i == j:
                    diag1_vals = set(grid[d][d] for d in range(9))
                if i + j == 8:
                    diag2_vals = set(grid[d][8-d] for d in range(9))
                used = row_vals | col_vals | block_vals | diag1_vals | diag2_vals
                candidates = [n for n in range(1, 10) if n not in used]
                if candidates:
                    grid[i][j] = random.choice(candidates)
                else:
                    present = set(val for val in grid[i] if val != 0)
                    missing = [n for n in range(1,10) if n not in present]
                    grid[i][j] = random.choice(missing) if missing else random.randint(1,9)
    return grid
