"""
This script provides a command-line interface for running Tabu Search experiments on Sudoku puzzles.
Includes:
- Argument parsing for experiment configuration
- Functions to run single or batch tests
- Output of results to console and CSV files
"""
import argparse
import time
import csv
import os
from pathlib import Path
from sudoku import loadPuzzle, printGrid
from tabuSearch import tabuSearch

def runSingle(puzzlePath, params):
    """Run Tabu Search on a single puzzle and display results."""
    puzzle = loadPuzzle(puzzlePath)
    puzzle_name = Path(puzzlePath).name
    print("="*60)
    print(f"Processing: {puzzle_name}")
    print("="*60)
    print("Initial puzzle:")
    printGrid(puzzle)
    print()
    best, best_cost, info = tabuSearch(puzzle,
                                       max_iter=params.max_iter,
                                       tabu_tenure=params.tabu_tenure,
                                       neighbour_sample_size=params.neighbour_sample_size,
                                       no_improve_limit=params.no_improve_limit,
                                       seed=params.seed)
    print("Finished. Best cost:", best_cost, "info:", info)
    printGrid(best)
    return best, best_cost, info

def runBatch(folder, outCsv, repeats, params):
    """Run Tabu Search on multiple puzzles with repeats, save results to CSV and HTML."""
    import datetime
    import random
    now = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')
    results_dir = Path(f'results/results_{now}')
    results_dir.mkdir(parents=True, exist_ok=True)
    outCsv = results_dir / 'results.csv'
    folder = Path(folder)
    puzzles = sorted([p for p in folder.glob("*.json")])
    
    # Determine if we're using random seeds
    use_random_seed = params.use_random_seed
    
    with open(outCsv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['puzzle','repeat','seed','best_cost','found','iter','time_s','tabu_tenure','neighbour_sample_size'])
        for p in puzzles:
            found_solution = False
            for r in range(1, repeats+1):  # Start with rep 1
                if found_solution:
                    break
                
                # Generate seed for this run
                if use_random_seed:
                    seed = random.randint(0, 999999)
                elif params.seed is not None:
                    seed = params.seed + r
                else:
                    seed = None
                puzzle_grid = loadPuzzle(str(p))
                print("\n" + "="*60)
                print(f"Processing: {p.name} (repeat {r}/{repeats})")
                if use_random_seed:
                    print(f"Using random seed: {seed}")
                print("="*60)
                best, best_cost, info = tabuSearch(puzzle_grid,
                                                   max_iter=params.max_iter,
                                                   tabu_tenure=params.tabu_tenure,
                                                   neighbour_sample_size=params.neighbour_sample_size,
                                                   no_improve_limit=params.no_improve_limit,
                                                   seed=seed)
                writer.writerow([p.name, r, seed, info['best_cost'], info['found'], info['iter'], info['time_s'], params.tabu_tenure, params.neighbour_sample_size])
                # Save HTML visualization for every run
                html_path = results_dir / f"{p.name}_rep{r}.html"
                timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
                with open(html_path, 'w', encoding='utf-8') as htmlf:
                    htmlf.write('<html><head><meta charset="utf-8"><title>Sudoku Solution</title>')
                    htmlf.write('<style>table{border-collapse:collapse;}td{width:30px;height:30px;text-align:center;font-size:18px;border:1px solid #888;} .block{border:2px solid #000;}</style></head><body>')
                    htmlf.write(f'<h2>Test case: {p.name} (repeat {r}) - {timestamp}</h2>')
                    htmlf.write('<h3>Initial puzzle</h3>')
                    htmlf.write('<table>')
                    for i, row in enumerate(puzzle_grid):
                        htmlf.write('<tr>')
                        for j, val in enumerate(row):
                            htmlf.write(f'<td class="block">{val if val != 0 else ""}</td>')
                        htmlf.write('</tr>')
                    htmlf.write('</table>')
                    if info['found']:
                        htmlf.write('<h3>Solution</h3>')
                        htmlf.write('<table>')
                        for i, row in enumerate(best):
                            htmlf.write('<tr>')
                            for j, val in enumerate(row):
                                htmlf.write(f'<td class="block">{val}</td>')
                            htmlf.write('</tr>')
                        htmlf.write('</table>')
                        found_solution = True
                    else:
                        htmlf.write(f'<h3>No solution found. Best cost: {info["best_cost"]}</h3>')
                        htmlf.write('<h4>Best grid found:</h4>')
                        htmlf.write('<table>')
                        for i, row in enumerate(best):
                            htmlf.write('<tr>')
                            for j, val in enumerate(row):
                                htmlf.write(f'<td class="block">{val}</td>')
                            htmlf.write('</tr>')
                        htmlf.write('</table>')
                    htmlf.write('</body></html>')

def parseArgs():
    """Parse command-line arguments for Tabu Search experiments."""
    p = argparse.ArgumentParser()
    p.add_argument('--puzzle', type=str, help='path to single puzzle (json)')
    p.add_argument('--batch', type=str, help='folder with puzzles (json)')
    p.add_argument('--out', type=str, default='results/results.csv', help='output CSV for batch')
    p.add_argument('--repeats', type=int, default=3)
    p.add_argument('--max_iter', type=int, default=100000)
    p.add_argument('--tabu_tenure', type=int, default=20)
    p.add_argument('--neighbour_sample_size', type=int, default=200)
    p.add_argument('--no_improve_limit', type=int, default=30000)
    p.add_argument('--seed', type=int, default=0, help='random seed (use -1 for truly random)')
    return p.parse_args()

if __name__ == "__main__":
    params = parseArgs()
    
    # Handle random seed
    params.use_random_seed = False
    if params.seed == -1:
        params.use_random_seed = True
        params.seed = None  # Will generate new random seed for each run
        print("Using random seeds for each run")
    
    if params.puzzle:
        # For single puzzle mode with random seed
        if params.use_random_seed:
            import random
            params.seed = random.randint(0, 999999)
            print(f"Using random seed: {params.seed}")
        runSingle(params.puzzle, params)
    elif params.batch:
        runBatch(params.batch, params.out, params.repeats, params)
    else:
        print("Specify --puzzle <path> or --batch <folder>")
