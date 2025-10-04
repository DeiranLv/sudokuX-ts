"""
This module implements the Tabu Search metaheuristic for solving Sudoku puzzles.
Includes:
- The main tabu_search algorithm
- Integration with initial solution and move generation modules
- Utilities for tracking search progress and best solutions
"""
import time
from typing import Tuple, List, Dict, Optional
from sudoku import Grid, computeCost, fixedMask, printGrid
from init import initialSolution
from moves import generateCandidates, normalizeMove
import random

def tabuSearch(puzzle: Grid,
                max_iter: int = 100000,
                tabu_tenure: int = 25,
                neighbour_sample_size: int = 500,
                no_improve_limit: int = 50000,
                seed: Optional[int] = None,
                verbose: bool = True):
    """Solve Sudoku X puzzle using Tabu Search with random restarts.
    
    Returns: (best_grid, best_cost, info_dict)
        best_grid: Best solution found (9x9 grid)
        best_cost: Cost of best solution (0 = valid solution)
        info_dict: Statistics (iterations, time, restarts, etc.)
    """
    rng = random.Random(seed)
    fixed = fixedMask(puzzle)
    grid = initialSolution(puzzle, seed=seed)
    best_grid = [row[:] for row in grid]
    best_cost = computeCost(grid)
    cur_grid = [row[:] for row in grid]
    cur_cost = best_cost

    tabu: Dict[Tuple, int] = {}  # Tabu list: move -> expiration iteration
    iter_no_improve = 0
    iter_count = 0
    restarts = 0
    max_restarts = 20  # Maximum random restarts allowed
    total_iter = 0
    start_time = time.perf_counter()

    from sudoku import isValidSudoku

    while iter_count < max_iter and best_cost > 0 and restarts <= max_restarts:
        # Inner loop: run until no improvement limit reached or solution found
        while iter_no_improve < no_improve_limit and iter_count < max_iter and best_cost > 0:
            iter_count += 1
            total_iter += 1
            # Generate candidate neighbor solutions
            candidates = generateCandidates(cur_grid, fixed, sampleSize=neighbour_sample_size, rng=rng)
            # Evaluate all candidates and sort by cost
            scored = []
            for g, m in candidates:
                c = computeCost(g)
                scored.append((c, g, m))
            if not scored:
                continue
            scored.sort(key=lambda x: x[0])
            moved = False
            # Select best non-tabu move, or use aspiration criterion (accept tabu if better than best)
            for c, g, m in scored:
                m_key = normalizeMove(m)
                is_tabu = (m_key in tabu and tabu[m_key] > iter_count)
                if (not is_tabu) or (c < best_cost):  # aspiration
                    cur_grid = g
                    cur_cost = c
                    tabu[m_key] = iter_count + tabu_tenure
                    moved = True
                    break
            if not moved:
                # Fallback: accept best move even if tabu (diversification)
                c, g, m = scored[0]
                cur_grid = g
                cur_cost = c
                tabu[normalizeMove(m)] = iter_count + tabu_tenure

            # Update best solution found so far
            if cur_cost < best_cost:
                best_cost = cur_cost
                best_grid = [row[:] for row in cur_grid]
                iter_no_improve = 0
            else:
                iter_no_improve += 1

            # Early exit if valid solution found
            if best_cost == 0 and isValidSudoku(best_grid):
                break

        # Random restart: escape local minimum by re-initializing
        if best_cost > 0 and iter_no_improve >= no_improve_limit and restarts < max_restarts:
            restarts += 1
            if verbose:
                print(f"↻ Restart #{restarts}")
            cur_grid = initialSolution(puzzle, seed=(seed + restarts) if seed is not None else None)
            cur_cost = computeCost(cur_grid)
            tabu = {}
            iter_no_improve = 0
            # Update best if restart produces better initial solution
            if cur_cost < best_cost:
                best_cost = cur_cost
                best_grid = [row[:] for row in cur_grid]

    elapsed = time.perf_counter() - start_time
    found = (best_cost == 0 and isValidSudoku(best_grid))
    
    if verbose:
        status = "✓" if found else "✗"
        print(f"{status} Cost: {best_cost} | Time: {elapsed:.1f}s | Iters: {total_iter} | Restarts: {restarts}")
    
    info = {
        'iter': total_iter,
        'time_s': elapsed,
        'best_cost': best_cost,
        'found': found,
        'no_improve': iter_no_improve,
        'restarts': restarts
    }
    return best_grid, best_cost, info

if __name__ == "__main__":
    # simple self-test
    from sudoku import loadPuzzle
    p = loadPuzzle('../tests/easy.json')
    best, bc, info = tabuSearch(p, max_iter=5000, tabu_tenure=15, neighbour_sample_size=150, seed=0)
    print("Result cost:", bc, info)
    print("Best grid:")
    printGrid(best)
