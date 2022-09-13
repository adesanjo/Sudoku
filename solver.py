from grid import Grid

class Solver:
    def __init__(self, grid: Grid):
        self.grid = grid
    
    def bruteForce(self):
        isGridComplete = self._bruteForce(0, 0)
        if not isGridComplete:
            print("Sudoku has no solution")
    
    def _bruteForce(self, r, c):
        if not self.grid.isCellValid(r - (c <= 0), c - 1 if c > 0 else 8):
            return False
        if r >= 9:
            return True
        if self.grid.getCell(r, c).isEmpty():
            digits = list(range(1, 10))
            for d in digits:
                self.grid.getCell(r, c).value = d
                isGridComplete = self._bruteForce(r + (c >= 8), c + 1 if c < 8 else 0)
                if isGridComplete:
                    return True
                self.grid.getCell(r, c).value = None
        else:
            isGridComplete = self._bruteForce(r + (c >= 8), c + 1 if c < 8 else 0)
            if isGridComplete:
                return True
        return False
