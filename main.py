from grid import Grid
from solver import Solver

if __name__ == "__main__":
    grid = Grid()
    # grid.initRandomGridWithConstraints(0.4)
    grid.initRandomGridWithConstraints(portionFilled=1, maxConstraints=5)
    print(grid)
    # Solver(grid).bruteForce()
    # print(grid)
