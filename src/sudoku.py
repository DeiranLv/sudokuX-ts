"""
This module provides core data structures and utility functions for Sudoku puzzles.
Includes:
- Grid type definition
- Functions to load and save Sudoku grids from/to JSON files
- Utility to generate a mask of fixed (given) cells
"""
from typing import List, Tuple
import json

Grid = List[List[int]]

# Strict validator: returns True only if grid is a valid Sudoku solution
def isValidSudoku(grid: Grid) -> bool:
    # Check rows and columns
    for i in range(9):
        row = [x for x in grid[i]]
        col = [grid[j][i] for j in range(9)]
        if set(row) != set(range(1, 10)):
            return False
        if set(col) != set(range(1, 10)):
            return False
    # Check blocks
    for bi in range(3):
        for bj in range(3):
            block = [grid[bi*3 + i][bj*3 + j] for i in range(3) for j in range(3)]
            if set(block) != set(range(1, 10)):
                return False
    # Check diagonals (Sudoku X)
    diag1 = [grid[i][i] for i in range(9)]
    diag2 = [grid[i][8-i] for i in range(9)]
    if set(diag1) != set(range(1, 10)):
        return False
    if set(diag2) != set(range(1, 10)):
        return False
    return True

def loadPuzzle(path: str) -> Grid:
    """Load puzzle from JSON file: 9x9 list of lists with 0 = empty"""
    with open(path, 'r') as f:
        data = json.load(f)
    assert len(data) == 9 and all(len(row) == 9 for row in data)
    return data

def saveGrid(path: str, grid: Grid):
    with open(path, 'w') as f:
        json.dump(grid, f)

def fixedMask(puzzle: Grid):
    """Return boolean mask of fixed cells (True if fixed)"""
    return [[cell != 0 for cell in row] for row in puzzle]

def printGrid(grid: Grid):
    sep = "+-------+-------+-------+"
    for i, row in enumerate(grid):
        if i % 3 == 0:
            print(sep)
        row_str = "| "
        for j, val in enumerate(row):
            ch = "." if val == 0 else str(val)
            row_str += ch + " "
            if (j + 1) % 3 == 0:
                row_str += "| "
        print(row_str)
    print(sep)

def isSolved(grid: Grid) -> bool:
    return computeCost(grid) == 0

def computeCost(grid: Grid) -> int:
    """Cost for Sudoku X: number of conflicts in columns, blocks, and both diagonals.
       Lower is better; 0 means valid solution."""
    c = 0
    # columns
    for j in range(9):
        col = [grid[i][j] for i in range(9)]
        c += 9 - len(set(col))
    # blocks
    for bi in range(3):
        for bj in range(3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(grid[bi*3+i][bj*3+j])
            c += 9 - len(set(block))
    # diagonals (Sudoku X)
    diag1 = [grid[i][i] for i in range(9)]
    diag2 = [grid[i][8-i] for i in range(9)]
    c += 9 - len(set(diag1))
    c += 9 - len(set(diag2))
    return c

# alias to match earlier names
cost = computeCost
