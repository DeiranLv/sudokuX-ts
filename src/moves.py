"""
This module defines move operations for Sudoku optimization algorithms.
Includes:
- Move type definition
- Functions to swap values in rows, columns, blocks, and diagonals while respecting fixed cells
- Utilities for move normalization and candidate generation

Note: The Tabu Search algorithm uses only row swaps (swapInRow) to preserve row validity.
Other swap functions are provided for potential alternative strategies.
"""

import random
from typing import Tuple, List, Optional
from sudoku import Grid

# Move type: a swap between two (row, col) positions
Move = Tuple[Tuple[int, int], Tuple[int, int]]

def swapInColumn(grid: Grid, fixedMask: List[List[bool]], rng: Optional[random.Random] = None) -> Tuple[Grid, Move]:
    """Swap two unfixed positions in a random column."""
    if rng is None:
        rng = random.Random()
    g = [row[:] for row in grid]
    col = rng.randrange(9)
    free = [i for i in range(9) if not fixedMask[i][col]]
    if len(free) < 2:
        return g, ((-1, -1), (-1, -1))
    a, b = rng.sample(free, 2)
    g[a][col], g[b][col] = g[b][col], g[a][col]
    move = ((a, col), (b, col))
    return g, normalizeMove(move)

def swapAnyUnfixed(grid: Grid, fixedMask: List[List[bool]], rng: Optional[random.Random] = None) -> Tuple[Grid, Move]:
    """Swap any two unfixed cells in the grid (for diversification)."""
    if rng is None:
        rng = random.Random()
    g = [row[:] for row in grid]
    free = [(i, j) for i in range(9) for j in range(9) if not fixedMask[i][j]]
    if len(free) < 2:
        return g, ((-1, -1), (-1, -1))
    (r1, c1), (r2, c2) = rng.sample(free, 2)
    g[r1][c1], g[r2][c2] = g[r2][c2], g[r1][c1]
    move = ((r1, c1), (r2, c2))
    return g, normalizeMove(move)

def swapInRow(grid: Grid, fixedMask: List[List[bool]], rng: Optional[random.Random] = None) -> Tuple[Grid, Move]:
    """Swap two unfixed positions in a random row. Return new grid and move descriptor."""
    if rng is None:
        rng = random.Random()
    g = [row[:] for row in grid]
    row = rng.randrange(9)
    free = [j for j in range(9) if not fixedMask[row][j]]
    if len(free) < 2:
        return g, ((-1, -1), (-1, -1))
    a, b = rng.sample(free, 2)
    g[row][a], g[row][b] = g[row][b], g[row][a]
    move = ((row, a), (row, b))
    return g, normalizeMove(move)

def swapInBlock(grid: Grid, fixedMask: List[List[bool]], rng: Optional[random.Random] = None) -> Tuple[Grid, Move]:
    """Swap two unfixed cells inside the same 3x3 block."""
    if rng is None:
        rng = random.Random()
    g = [row[:] for row in grid]
    bi = rng.randrange(3)
    bj = rng.randrange(3)
    cells = []
    for i in range(3):
        for j in range(3):
            r = bi*3 + i
            c = bj*3 + j
            if not fixedMask[r][c]:
                cells.append((r, c))
    if len(cells) < 2:
        return g, ((-1, -1), (-1, -1))
    (r1, c1), (r2, c2) = rng.sample(cells, 2)
    g[r1][c1], g[r2][c2] = g[r2][c2], g[r1][c1]
    move = ((r1, c1), (r2, c2))
    return g, normalizeMove(move)

def swapInDiagonal(grid: Grid, fixedMask: List[List[bool]], rng: Optional[random.Random] = None) -> Tuple[Grid, Move]:
    """Swap two unfixed cells on the same diagonal (main or anti-diagonal)."""
    if rng is None or not hasattr(rng, 'choice') or not hasattr(rng, 'sample'):
        rng = random.Random()
    g = [row[:] for row in grid]
    diag_type = getattr(rng, 'choice', random.choice)([0, 1])
    cells = []
    if diag_type == 0:
        for i in range(9):
            if not fixedMask[i][i]:
                cells.append((i, i))
    else:
        for i in range(9):
            if not fixedMask[i][8 - i]:
                cells.append((i, 8 - i))
    if len(cells) < 2:
        return g, ((-1, -1), (-1, -1))
    sample_func = getattr(rng, 'sample', random.sample)
    (r1, c1), (r2, c2) = sample_func(cells, 2)
    g[r1][c1], g[r2][c2] = g[r2][c2], g[r1][c1]
    move = ((r1, c1), (r2, c2))
    return g, normalizeMove(move)

def normalizeMove(move: Move) -> Move:
    """Return move tuple in canonical order so reverse swap equals same key."""
    if move is None:
        return None
    (a1, a2), (b1, b2) = move
    if (a1, a2) <= (b1, b2):
        return ((a1, a2), (b1, b2))
    else:
        return ((b1, b2), (a1, a2))

def generateCandidates(grid: Grid, fixedMask: List[List[bool]], sampleSize: int = 200, rng: Optional[random.Random] = None):
    """Generate a list of candidate (grid, move) pairs.
    All moves are row swaps to preserve row uniqueness (essential constraint for Sudoku).
    Returns list of (new_grid, move) tuples."""
    if rng is None:
        rng = random.Random()
    cand = []
    for _ in range(sampleSize):
        # Only use row swaps to preserve row constraint
        g, m = swapInRow(grid, fixedMask, rng)
        if m == ((-1, -1), (-1, -1)):
            continue
        cand.append((g, m))
    return cand
