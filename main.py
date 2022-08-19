from grid import Grid
from solver import Solver

if __name__ == "__main__":
    grid = Grid()
    grid.initRandomGrid(0.4)
    print(grid)
    Solver(grid).bruteForce()
    print(grid)