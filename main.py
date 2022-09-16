from grid import Grid
from solver import Solver
from gui import GUI

if __name__ == "__main__":
    # grid = Grid()
    # grid.initRandomGrid(0.4)
    # grid.initRandomGridWithConstraints(0.4)
    # grid.initRandomGridWithConstraints(portionFilled=1, maxConstraints=5)
    # print(grid)
    # Solver(grid).bruteForce()
    # print(grid)
    gui = GUI()
    gui.run()
