import random
from time import sleep

class Grid:
    def __init__(self):
        self.initEmptyGrid()
    
    def getCell(self, r, c):
        return self.grid[r][c]
    
    def flattenedGrid(self):
        return [self.grid[r][c] for r in range(9) for c in range(9)]
    
    def initEmptyGrid(self):
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]
    
    def initFullRandomGrid(self):
        self.initEmptyGrid()
        self._genFullRandomGrid()
    
    def _genFullRandomGrid(self, r=0, c=0):
        if not self.isCellValid(r - (c <= 0), c - 1 if c > 0 else 8):
            return False
        if r >= 9:
            return True
        digits = list(range(1, 10))
        random.shuffle(digits)
        for d in digits:
            self.grid[r][c].value = d
            isGridComplete = self._genFullRandomGrid(r + (c >= 8), c + 1 if c < 8 else 0)
            if isGridComplete:
                return True
            self.grid[r][c].value = None
        return False
    
    def initRandomGrid(self, portionFilled=0.5):
        self.initFullRandomGrid()
        cellsToEmpty = random.sample(self.flattenedGrid(), round(81 * (1 - portionFilled)))
        for cell in cellsToEmpty:
            cell.value = None
    
    def isValid(self):
        for r in range(9):
            for c in range(9):
                if not self.isCellValid(r, c):
                    return False
        return True
    
    def isCellValid(self, r, c):
        if r < 0:
            return True
        cell = self.grid[r][c]
        if cell.isEmpty():
            return True
        if [self.grid[r][i] for i in range(9)].count(cell) > 1:
            return False
        if [self.grid[i][c] for i in range(9)].count(cell) > 1:
            return False
        if [self.grid[r // 3 * 3 + i // 3][c // 3 * 3 + i % 3] for i in range(9)].count(cell) > 1:
            return False
        return True
    
    def __str__(self):
        res = ""
        for rr in range(3):
            res += " ".join(["-" * 13] * 3) + "\n"
            for r in range(rr * 3, rr * 3 + 3):
                for rc in range(3):
                    res += "|"
                    for c in range(rc * 3, rc * 3 + 3):
                        res += " " + str(self.grid[r][c]) + " |" + " " * (c % 3 == 2 and rc < 2)
                res += "\n" + " ".join(["-" * 13] * 3) + "\n"
        return res

class Cell:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if value in [None] + list(range(1, 10)):
            self._value = value
    
    def isEmpty(self):
        return self.value is None
    
    def __str__(self):
        return str(self.value) if self.value is not None else " "
    
    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.value == other.value
