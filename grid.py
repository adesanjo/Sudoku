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
        self.grid = [[Cell(r=r, c=c) for c in range(9)] for r in range(9)]
        self.constraints: list[Constraint] = []
    
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
        self.removeRandomCells(portionFilled)
    
    def initRandomGridWithConstraints(self, portionFilled=0.5, maxConstraints=1):
        self.initEmptyGrid()
        for _ in range(1, random.randint(1, maxConstraints) + 1):
            if random.randrange(3) != 0:
                constraintType = random.choice(DominoConstraint.allTypes())
                r = random.randrange(9)
                c = random.randrange(9)
                cellA = self.grid[r][c]
                dr, dc = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                if not (0 <= r + dr < 9 and 0 <= c + dc < 9):
                    dr = -dr
                    dc = -dc
                cellB = self.grid[r + dr][c + dc]
                args = (cellA, cellB)
            elif random.randrange(3) != 0:
                constraintType = random.choice(PathConstraint.allTypes())
                r = random.randrange(9)
                c = random.randrange(9)
                cells = [self.grid[r][c]]
                dr, dc = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                if not (0 <= r + dr < 9 and 0 <= c + dc < 9):
                    dr = -dr
                    dc = -dc
                cells.append(self.grid[(r := r + dr)][(c := c + dc)])
                n = random.randrange(8)
                triesLeft = 50
                while n > 0 and triesLeft > 0:
                    triesLeft -= 1
                    dr, dc = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                    if 0 <= r + dr < 9 and 0 <= c + dc < 9 and self.grid[r + dr][c + dc] not in cells:
                        cells.append(self.grid[(r := r + dr)][(c := c + dc)])
                        n -= 1
                args = (cells,)
            else:
                constraintType = random.choice(GeneralConstraint.allTypes())
                args = (self,)
            constraint = constraintType(*args)
            self.constraints.append(constraint)
        self._genFullRandomGrid()
        self.removeRandomCells(portionFilled)
    
    def removeRandomCells(self, portionFilled=0.5):
        cellsToEmpty = random.sample(self.flattenedGrid(), round(81 * (1 - portionFilled)))
        for cell in cellsToEmpty:
            cell.value = None
    
    def isPartialValid(self):
        for r in range(9):
            cells = [cell for i in range(9) if (cell := self.grid[r][i]).isNotEmpty()]
            if len(cells) != len(set(cells)):
                return False
        for c in range(9):
            cells = [cell for i in range(9) if (cell := self.grid[i][c]).isNotEmpty()]
            if len(cells) != len(set(cells)):
                return False
        for b in range(9):
            cells = [cell for i in range(9) if (cell := self.grid[b // 3 * 3 + i // 3][b % 3 * 3 + i % 3]).isNotEmpty()]
            if len(cells) != len(set(cells)):
                return False
        return True
    
    def isValid(self):
        for r in range(9):
            for c in range(9):
                if not self.isCellValid(r, c):
                    return False
        for constraint in self.constraints:
            if not constraint.isValid():
                return False
        return True
    
    def isCellValid(self, r: int, c: int):
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
        for constraint in self.constraints:
            if not constraint.isCellValid(self.grid[r][c]):
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
        nl = "\n"
        res += f"\n{nl.join(str(constraint) for constraint in self.constraints)}\n"
        return res

class Cell:
    def __init__(self, value=None, r=0, c=0):
        self._value = value
        self._r = r
        self._c = c

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if value in [None] + list(range(1, 10)):
            self._value = value

    @property
    def r(self):
        return self._r

    @property
    def c(self):
        return self._c
    
    @property
    def pos(self):
        return (self.r, self.c)
    
    def isEmpty(self):
        return self.value is None
    
    def isNotEmpty(self):
        return self.value is not None
    
    def __str__(self):
        return str(self.value) if self.value is not None else " "
    
    def __hash__(self):
        return hash(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.value == other.value

class Constraint:
    @staticmethod
    def allTypes() -> list[type]:
        return GeneralConstraint.allTypes() + DominoConstraint.allTypes() + PathConstraint.allTypes()
    
    def isCellValid(self, cell: Cell):
        raise NotImplemented
    
    def isValid(self):
        raise NotImplemented
    
    def __str__(self):
        return self.__class__.__name__

class GeneralConstraint(Constraint):
    def __init__(self, grid: Grid):
        self.grid = grid
    
    @staticmethod
    def allTypes() -> list[type]:
        return [KnightsMove]

class KnightsMove(GeneralConstraint):
    def isCellValid(self, cell: Cell):
        r, c = cell.r, cell.c
        for dr, dc in [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]:
            if 0 <= r + dr < 9 and 0 <= c + dc < 9 and cell == self.grid.getCell(r + dr, c + dc):
                return False
        return True
    
    def isValid(self):
        for r in range(9):
            for c in range(9):
                if not self.isCellValid(self.grid.getCell(r, c)):
                    return False
        return True

class DominoConstraint(Constraint):
    def __init__(self, cellA: Cell, cellB: Cell):
        self.cellA = cellA
        self.cellB = cellB
    
    @staticmethod
    def allTypes() -> list[type]:
        return [Vsum, Xsum, KropkiWhite, KropkiBlack]
    
    def isCellValid(self, cell: Cell):
        return cell not in [self.cellA, self.cellB] or self.isValid()
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.cellA.pos}, {self.cellB.pos})"

class Vsum(DominoConstraint):
    def isValid(self):
        if self.cellA.isEmpty() or self.cellB.isEmpty():
            return True
        return self.cellA.value + self.cellB.value == 5

class Xsum(DominoConstraint):
    def isValid(self):
        if self.cellA.isEmpty() or self.cellB.isEmpty():
            return True
        return self.cellA.value + self.cellB.value == 10

class KropkiWhite(DominoConstraint):
    def isValid(self):
        if self.cellA.isEmpty() or self.cellB.isEmpty():
            return True
        return abs(self.cellA.value - self.cellB.value) == 1

class KropkiBlack(DominoConstraint):
    def isValid(self):
        if self.cellA.isEmpty() or self.cellB.isEmpty():
            return True
        return self.cellA.value / self.cellB.value in [0.5, 2]

class PathConstraint(Constraint):
    def __init__(self, cells: list[Cell]):
        self.cells = cells
    
    @staticmethod
    def allTypes() -> list[type]:
        return [Thermometer, Arrow]
    
    def isCellValid(self, cell: Cell):
        return cell not in self.cells or self.isValid()
    
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(str(cell.pos) for cell in self.cells)})"

class Thermometer(PathConstraint):
    def isValid(self):
        lastValue = 0
        for cell in self.cells:
            if cell.isNotEmpty():
                if cell.calue <= lastValue:
                    return False
                lastValue = cell.value
        return True

class Arrow(PathConstraint):
    def isValid(self):
        if len(self.cells) < 2:
            return True
        sumValue = self.cells[0].value
        arrowCells = self.cells[1:]
        if any(cell.isEmpty() for cell in arrowCells):
            return True
        return sum(map(lambda c: c.value, arrowCells)) == sumValue
