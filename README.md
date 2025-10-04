# Sudoku X Solver with Tabu Search
**DatZM014 : Praktiskā kombinatoriālā optimizācija**  
**MAZAIS praktiskais darbs**  
**Autors: Jevgēnijs Locs**

This project is a **Sudoku X solver** implemented in Python, utilizing the **Tabu Search** metaheuristic. Sudoku X is a Sudoku variant where both main diagonals must also contain unique digits (in addition to standard row, column, and 3x3 block constraints).

## Features

- ✅ Solves Sudoku X puzzles (rows, columns, blocks, and both diagonals)
- ✅ Tabu Search metaheuristic with random restarts
- ✅ Constraint-aware initial solution generator
- ✅ Batch testing with CSV and HTML output
- ✅ Pure Python (no external dependencies)

## Project Structure

```
sudokuX-ts/
├── src/
│   ├── init.py         # Initial solution generator
│   ├── moves.py        # Move operations (row swaps)
│   ├── sudoku.py       # Core utilities and validator
│   ├── tabuSearch.py   # Main Tabu Search algorithm
│   └── runTests.py     # CLI for experiments
├── tests/              # Test puzzles (JSON format)
├── results/            # Output folder (CSV + HTML)
└── README.md           # This file
```

## Usage

### Single Puzzle Test

```bash
python src/runTests.py --puzzle tests/easy.json
```

### Batch Testing (Multiple Puzzles)

```bash
python src/runTests.py --batch tests
```

## Input Format

Puzzles are stored as JSON files with a 9x9 array:
- `0` = empty cell
- `1-9` = fixed (given) cell

Example (`tests/empty.json`):
```json
[
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0],
 [0,0,0, 0,0,0, 0,0,0]
]
```

## Parameters

### Command Line Arguments

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--puzzle PATH` | Path to single puzzle JSON file | - |
| `--batch FOLDER` | Folder containing multiple puzzles | - |
| `--out PATH` | Output CSV path for batch mode | `results/results.csv` |
| `--repeats N` | Number of runs per puzzle (batch mode) | `3` |
| `--max_iter N` | Maximum iterations | `100000` |
| `--tabu_tenure N` | Tabu list tenure (how long moves stay forbidden) | `20` |
| `--neighbour_sample_size N` | Candidate moves evaluated per iteration | `200` |
| `--no_improve_limit N` | Iterations without improvement before restart | `30000` |
| `--seed N` | Random seed for reproducibility | `0` |

### Recommended Settings

For **easy puzzles** (many fixed cells):
```bash
--max_iter 50000 --tabu_tenure 15 --neighbour_sample_size 150 --no_improve_limit 10000
```

For **hard puzzles** (few fixed cells) or **empty grids**:
```bash
--max_iter 100000 --tabu_tenure 25 --neighbour_sample_size 500 --no_improve_limit 30000
```

## Output

### Console Output

**Single puzzle mode:**
- Puzzle name and separator line
- Initial puzzle display (with `.` for empty cells)
- Restart notifications (if any): `↻ Restart #N`
- Final result line: `✓ Cost: 0 | Time: 5.2s | Iters: 1523 | Restarts: 0`
  - `✓` = solution found, `✗` = no solution
- Final solution grid

**Batch mode:**
- For each puzzle and repeat:
  - Processing header: `Processing: puzzle_name.json (repeat N/M)`
  - Restart notifications during search
  - Final result line with statistics

Example output:
```
============================================================
Processing: empty.json (repeat 1/3)
============================================================
↻ Restart #1
↻ Restart #2
✓ Cost: 0 | Time: 8.3s | Iters: 2847 | Restarts: 2
```

### Batch Output Files

Creates a timestamped folder in `results/` with:
- **CSV file** (`results.csv`): Summary of all runs with columns:
  - `puzzle`, `repeat`, `seed`, `best_cost`, `found`, `iter`, `time_s`, `tabu_tenure`, `neighbour_sample_size`
- **HTML files**: One per run showing:
  - Test case name, repeat number, and timestamp
  - Initial puzzle grid
  - Solution grid (if found) or best grid with cost

Example output folder: `results/results_04-10-2025_14-30/`

## How It Works

### Sudoku X Constraints
A valid solution must have unique digits 1-9 in:
1. Each row
2. Each column
3. Each 3×3 block
4. Main diagonal (top-left to bottom-right)
5. Anti-diagonal (top-right to bottom-left)

### Algorithm Overview
1. **Initial Solution**: Generate row-valid grid (each row has 1-9, but may have conflicts in columns/blocks/diagonals)
2. **Move Generation**: Swap two cells within the same row (preserves row constraint)
3. **Cost Function**: Count conflicts in columns, blocks, and both diagonals
4. **Tabu List**: Track recent moves to prevent cycling
5. **Aspiration Criterion**: Accept tabu moves if they improve best solution
6. **Random Restart**: Re-initialize if stuck in local minimum

### Why Row Swaps Only?
- Maintains row uniqueness (essential for Sudoku)
- Initial solution ensures all rows are valid
- All subsequent moves preserve this property
- Cost function optimizes the remaining constraints

## About Tabu Search

Tabu Search is a metaheuristic that guides a local search procedure to explore the solution space beyond local optimality. Key features:
- **Tabu List**: Maintains a memory of recent moves to avoid cycling
- **Aspiration Criterion**: Allows breaking tabu if solution improves
- **Diversification**: Random restarts escape local minima
- **Intensification**: Focused exploration of promising regions

## Requirements

- Python 3.7 or higher
- No external dependencies (uses standard library only)

## License

Academic project for combinatorial optimization course (DatZM014).
