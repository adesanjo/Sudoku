from typing import Literal

from select import select
import pygame as pg

from grid import *

SIZE = 600

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 200
# SELECTED_COLOR = 255, 255, 200
SELECTED_COLOR = 220, 250, 250
SELECTED_BORDER_COLOR = 0, 100, 255
THERMO_COLOR = 150, 150, 150
ARROW_COLOR = 50, 50, 50

NUM_KEYS = {
    pg.K_KP1: 1,
    pg.K_KP2: 2,
    pg.K_KP3: 3,
    pg.K_KP4: 4,
    pg.K_KP5: 5,
    pg.K_KP6: 6,
    pg.K_KP7: 7,
    pg.K_KP8: 8,
    pg.K_KP9: 9,
}

class GUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SIZE, SIZE))
        self.grid = Grid()
        self.selectedCells: list[Cell] = []
        self.mouseAction: Literal["select"] | Literal["deselect"] | None = None
        self.isCenterMark = False
        self.isCornerMark = False
        self.font = pg.font.SysFont("Helvetica", SIZE // 20)
        self.smallFont = pg.font.SysFont("Helvetica", SIZE // 45)
        self.initGrid()
    
    def initGrid(self):
        # self.grid.initRandomGrid(0.4)
        self.grid.initEmptyGrid()
        self.grid.constraints.append(Vsum(self.grid.getCell(0, 0), self.grid.getCell(0, 1)))
        self.grid.constraints.append(Vsum(self.grid.getCell(0, 2), self.grid.getCell(1, 2)))
        self.grid.constraints.append(Xsum(self.grid.getCell(2, 0), self.grid.getCell(2, 1)))
        self.grid.constraints.append(Xsum(self.grid.getCell(2, 2), self.grid.getCell(3, 2)))
        self.grid.constraints.append(KropkiWhite(self.grid.getCell(0, 3), self.grid.getCell(0, 4)))
        self.grid.constraints.append(KropkiWhite(self.grid.getCell(0, 5), self.grid.getCell(1, 5)))
        self.grid.constraints.append(KropkiBlack(self.grid.getCell(2, 3), self.grid.getCell(2, 4)))
        self.grid.constraints.append(KropkiBlack(self.grid.getCell(2, 5), self.grid.getCell(3, 5)))
        self.grid.constraints.append(Thermometer([self.grid.getCell(4, 4), self.grid.getCell(4, 5), self.grid.getCell(5, 6), self.grid.getCell(6, 6), self.grid.getCell(7, 5), self.grid.getCell(6, 5)]))
        self.grid.constraints.append(Arrow([self.grid.getCell(5, 5), self.grid.getCell(5, 6), self.grid.getCell(6, 7), self.grid.getCell(7, 7), self.grid.getCell(8, 6), self.grid.getCell(7, 6)]))
        # self.grid._genFullRandomGrid()
        # self.grid.removeRandomCells(0.4)
    
    def run(self):
        running = True
        while running:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False
                    break
                if e.type == pg.MOUSEBUTTONDOWN:
                    mx, my = pg.mouse.get_pos()
                    r = (my - 10) * 9 // (SIZE - 20)
                    c = (mx - 10) * 9 // (SIZE - 20)
                    if 0 <= r < 9 and 0 <= c < 9:
                        clickedCell = self.grid.getCell(r, c)
                    else:
                        clickedCell = None
                    if clickedCell is None:
                        if self.mouseAction is None:
                            self.mouseAction = "deselect"
                        self.selectedCells.clear()
                    elif self.isCenterMark or self.isCornerMark:
                        if clickedCell in self.selectedCells:
                            if self.mouseAction is None:
                                self.mouseAction = "deselect"
                            self.selectedCells.remove(clickedCell)
                        else:
                            if self.mouseAction is None:
                                self.mouseAction = "select"
                            self.selectedCells.append(clickedCell)
                    else:
                        if clickedCell in self.selectedCells:
                            if len(self.selectedCells) > 1:
                                if self.mouseAction is None:
                                    self.mouseAction = "select"
                                self.selectedCells.clear()
                                self.selectedCells.append(clickedCell)
                            else:
                                if self.mouseAction is None:
                                    self.mouseAction = "deselect"
                                self.selectedCells.clear()
                        else:
                            if self.mouseAction is None:
                                self.mouseAction = "select"
                            self.selectedCells.clear()
                            self.selectedCells.append(clickedCell)
                elif e.type == pg.MOUSEBUTTONUP:
                    self.mouseAction = None
                elif e.type == pg.MOUSEMOTION:
                    mx, my = pg.mouse.get_pos()
                    r = (my - 10) * 9 // (SIZE - 20)
                    c = (mx - 10) * 9 // (SIZE - 20)
                    if 0 <= r < 9 and 0 <= c < 9:
                        clickedCell = self.grid.getCell(r, c)
                    else:
                        clickedCell = None
                    if clickedCell is not None:
                        if self.mouseAction == "select" and clickedCell not in self.selectedCells:
                            self.selectedCells.append(clickedCell)
                        elif self.mouseAction == "deselect" and clickedCell in self.selectedCells:
                            self.selectedCells.remove(clickedCell)
                elif e.type == pg.KEYDOWN:
                    self.isCenterMark = self.isCenterMark or e.key == pg.K_LCTRL
                    self.isCornerMark = self.isCornerMark or e.key == pg.K_LALT
                    if e.key in NUM_KEYS:
                        num = NUM_KEYS[e.key]
                        if self.isCenterMark:
                            if not all(num in cell.centerMarks for cell in self.selectedCells if not cell.locked):
                                for cell in self.selectedCells:
                                    if not cell.locked and num not in cell.centerMarks:
                                        cell.centerMarks.append(num)
                            else:
                                for cell in self.selectedCells:
                                    if not cell.locked and num in cell.centerMarks:
                                        cell.centerMarks.remove(num)
                        elif self.isCornerMark:
                            if not all(num in cell.cornerMarks for cell in self.selectedCells if not cell.locked):
                                for cell in self.selectedCells:
                                    if not cell.locked and num not in cell.cornerMarks:
                                        cell.cornerMarks.append(num)
                            else:
                                for cell in self.selectedCells:
                                    if not cell.locked and num in cell.cornerMarks:
                                        cell.cornerMarks.remove(num)
                        else:
                            if not all(cell.value == num for cell in self.selectedCells if not cell.locked):
                                for cell in self.selectedCells:
                                    if not cell.locked:
                                        cell.value = num
                            else:
                                for cell in self.selectedCells:
                                    if not cell.locked and cell.value == num:
                                        cell.value = None
                elif e.type == pg.KEYUP:
                    if e.key == pg.K_LCTRL:
                        self.isCenterMark = False
                    if e.key == pg.K_LALT:
                        self.isCornerMark = False
            if not running:
                break
            self.update()
            self.render()
    
    def update(self):
        ...
    
    def render(self):
        self.screen.fill(WHITE)

        for cell in self.selectedCells:
            x = (SIZE - 20) * cell.c / 9 + 10
            y = (SIZE - 20) * cell.r / 9 + 10
            s = (SIZE - 20) / 9
            pg.draw.rect(self.screen, SELECTED_COLOR, pg.Rect(x, y, s, s))

        for i in range(10):
            x = y = (SIZE - 20) * i / 9 + 10
            w = 9 if i % 3 == 0 else 5
            pg.draw.line(self.screen, BLACK, (x, 10), (x, SIZE - 10), w)
            pg.draw.line(self.screen, BLACK, (10, y), (SIZE - 10, y), w)
        
        for constraint in self.grid.constraints:
            self.renderConstraint(constraint)
        
        for r in range(9):
            for c in range(9):
                cell = self.grid.getCell(r, c)
                x = (SIZE - 20) * c / 9 + 10 + (SIZE - 20) / 18
                y = (SIZE - 20) * r / 9 + 10 + (SIZE - 20) / 18
                if cell.value is not None:
                    text = self.font.render(str(cell.value), True, BLACK if cell.locked else BLUE)
                    textRect = text.get_rect()
                    textRect.center = (x, y)
                    self.screen.blit(text, textRect)
                else:
                    text = self.smallFont.render("".join(map(str, cell.centerMarks)), True, BLACK if cell.locked else BLUE)
                    textRect = text.get_rect()
                    textRect.center = (x, y)
                    self.screen.blit(text, textRect)

                    text = self.smallFont.render("".join(map(str, cell.cornerMarks)), True, BLACK if cell.locked else BLUE)
                    textRect = text.get_rect()
                    textRect.size = ((SIZE - 20) / 9 - 10, (SIZE - 20) / 9 - 10)
                    textRect.center = (x, y)
                    self.screen.blit(text, textRect)

        for cell in self.selectedCells:
            x = (SIZE - 20) * cell.c / 9 + 10
            y = (SIZE - 20) * cell.r / 9 + 10
            s = (SIZE - 20) / 9
            pg.draw.line(self.screen, SELECTED_BORDER_COLOR, (x, y), (x + s, y), 10)
            pg.draw.line(self.screen, SELECTED_BORDER_COLOR, (x, y), (x, y + s), 10)
            pg.draw.line(self.screen, SELECTED_BORDER_COLOR, (x + s, y), (x + s, y + s), 10)
            pg.draw.line(self.screen, SELECTED_BORDER_COLOR, (x, y + s), (x + s, y + s), 10)

        pg.display.flip()

    def drawRoundedLine(self, c, p1, p2, w):
        p1v = pg.math.Vector2(p1)
        p2v = pg.math.Vector2(p2)
        lv = (p2v - p1v).normalize()
        lnv = pg.math.Vector2(-lv.y, lv.x) * w / 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
        pg.draw.polygon(self.screen, c, pts)
        pg.draw.circle(self.screen, c, p1, w / 2)
        pg.draw.circle(self.screen, c, p2, w / 2)
    
    def renderConstraint(self, constraint):
        if isinstance(constraint, GeneralConstraint):
            return
        elif isinstance(constraint, Vsum):
            x = (SIZE - 20) * (constraint.cellA.c + constraint.cellB.c + 1) / 18 + 10
            y = (SIZE - 20) * (constraint.cellA.r + constraint.cellB.r + 1) / 18 + 10
            text = self.smallFont.render("V", True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.center = (x, y)
            self.screen.blit(text, textRect)
        elif isinstance(constraint, Xsum):
            x = (SIZE - 20) * (constraint.cellA.c + constraint.cellB.c + 1) / 18 + 10
            y = (SIZE - 20) * (constraint.cellA.r + constraint.cellB.r + 1) / 18 + 10
            text = self.smallFont.render("X", True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.center = (x, y)
            self.screen.blit(text, textRect)
        elif isinstance(constraint, KropkiWhite):
            x = (SIZE - 20) * (constraint.cellA.c + constraint.cellB.c + 1) / 18 + 10
            y = (SIZE - 20) * (constraint.cellA.r + constraint.cellB.r + 1) / 18 + 10
            pg.draw.circle(self.screen, BLACK, (x, y), 9)
            pg.draw.circle(self.screen, WHITE, (x, y), 7)
        elif isinstance(constraint, KropkiBlack):
            x = (SIZE - 20) * (constraint.cellA.c + constraint.cellB.c + 1) / 18 + 10
            y = (SIZE - 20) * (constraint.cellA.r + constraint.cellB.r + 1) / 18 + 10
            pg.draw.circle(self.screen, BLACK, (x, y), 8)
        elif isinstance(constraint, Thermometer):
            cell = constraint.cells[0]
            x = (SIZE - 20) * cell.c / 9 + 10 + (SIZE - 20) / 18
            y = (SIZE - 20) * cell.r / 9 + 10 + (SIZE - 20) / 18
            pg.draw.circle(self.screen, THERMO_COLOR, (x, y), 25)
            for nextCell in constraint.cells[1:]:
                x = (SIZE - 20) * cell.c / 9 + 10 + (SIZE - 20) / 18
                y = (SIZE - 20) * cell.r / 9 + 10 + (SIZE - 20) / 18
                nx = (SIZE - 20) * nextCell.c / 9 + 10 + (SIZE - 20) / 18
                ny = (SIZE - 20) * nextCell.r / 9 + 10 + (SIZE - 20) / 18
                dx = nx - x
                dy = ny - y
                self.drawRoundedLine(THERMO_COLOR, (x, y), (nx, ny), 20)
                cell = nextCell
        elif isinstance(constraint, Arrow):
            cell = constraint.cells[0]
            startX = (SIZE - 20) * cell.c / 9 + 10 + (SIZE - 20) / 18
            startY = (SIZE - 20) * cell.r / 9 + 10 + (SIZE - 20) / 18
            for nextCell in constraint.cells[1:]:
                x = (SIZE - 20) * cell.c / 9 + 10 + (SIZE - 20) / 18
                y = (SIZE - 20) * cell.r / 9 + 10 + (SIZE - 20) / 18
                nx = (SIZE - 20) * nextCell.c / 9 + 10 + (SIZE - 20) / 18
                ny = (SIZE - 20) * nextCell.r / 9 + 10 + (SIZE - 20) / 18
                dx = nx - x
                dy = ny - y
                self.drawRoundedLine(ARROW_COLOR, (x, y), (nx, ny), 3)
                cell = nextCell
            dx = 0 if dx == 0 else 1 if dx > 0 else -1
            dy = 0 if dy == 0 else 1 if dy > 0 else -1
            """
            -1, -1   ->    0,  1    1,  0
            -1,  0   ->    1,  1    1, -1
            -1,  1   ->    1,  0    0, -1
             0,  1   ->    1, -1   -1, -1
             1,  1   ->    0, -1   -1,  0
             1,  0   ->   -1, -1   -1,  1
             1, -1   ->   -1,  0    0,  1
             0, -1   ->   -1,  1    1,  1
            """
            dx = 15 * (dy - dx) / abs(dy - dx)
            dy = 15 * (-dy - dx) / abs(dy + dx)
            pg.draw.line(self.screen, ARROW_COLOR, (nx, ny), (nx + dx, ny + dy), 3)
            pg.draw.line(self.screen, ARROW_COLOR, (nx, ny), (nx + dy, ny - dx), 3)
            pg.draw.circle(self.screen, ARROW_COLOR, (startX, startY), 27)
            pg.draw.circle(self.screen, WHITE, (startX, startY), 24)
