import pygame as pg

from grid import Grid, Cell

SIZE = 600

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 200
SELECTED_COLOR = 255, 255, 200

class GUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SIZE, SIZE))
        self.grid = Grid()
        self.selectedCell: Cell | None = None
        self.font = pg.font.SysFont("Helvetica", SIZE // 20)
        self.initGrid()
    
    def initGrid(self):
        self.grid.initRandomGrid(0.4)
    
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
                    if clickedCell is None or (self.selectedCell is not None and clickedCell.pos == self.selectedCell.pos):
                        self.selectedCell = None
                    else:
                        self.selectedCell = clickedCell
                elif e.type == pg.KEYDOWN:
                    keys = [pg.K_KP1, pg.K_KP2, pg.K_KP3, pg.K_KP4, pg.K_KP5, pg.K_KP6, pg.K_KP7, pg.K_KP8, pg.K_KP9]
                    if e.key in keys and not self.selectedCell.locked:
                        if self.selectedCell.value == keys.index(e.key) + 1:
                            self.selectedCell.value = None
                        else:
                            self.selectedCell.value = keys.index(e.key) + 1
            if not running:
                break
            self.update()
            self.render()
    
    def update(self):
        ...
    
    def render(self):
        self.screen.fill(WHITE)

        if self.selectedCell is not None:
            x = (SIZE - 20) * self.selectedCell.c / 9 + 10
            y = (SIZE - 20) * self.selectedCell.r / 9 + 10
            s = (SIZE - 20) / 9
            pg.draw.rect(self.screen, SELECTED_COLOR, pg.Rect(x, y, s, s))

        for i in range(10):
            x = y = (SIZE - 20) * i / 9 + 10
            w = 9 if i % 3 == 0 else 5
            pg.draw.line(self.screen, BLACK, (x, 10), (x, SIZE - 10), w)
            pg.draw.line(self.screen, BLACK, (10, y), (SIZE - 10, y), w)
        
        for r in range(9):
            for c in range(9):
                cell = self.grid.getCell(r, c)
                x = (SIZE - 20) * c / 9 + 10 + (SIZE - 20) / 18
                y = (SIZE - 20) * r / 9 + 10 + (SIZE - 20) / 18
                text = self.font.render(str(cell), True, BLACK if cell.locked else BLUE)
                textRect = text.get_rect()
                textRect.center = (x, y)
                self.screen.blit(text, textRect)

        pg.display.flip()
