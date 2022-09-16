import pygame as pg

from grid import Grid

WIDTH, HEIGHT = 600, 600

WHITE = 255, 255, 255
BLACK = 0, 0, 0

class GUI:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.grid = Grid()
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
            if not running:
                break
            self.update()
            self.render()
    
    def update(self):
        ...
    
    def render(self):
        self.screen.fill(WHITE)

        pg.draw.line(self.screen, BLACK, (6, 10), (WIDTH - 5, 10), 10)
        pg.draw.line(self.screen, BLACK, (6, HEIGHT - 10), (WIDTH - 5, HEIGHT - 10), 10)
        pg.draw.line(self.screen, BLACK, (10, 10), (10, HEIGHT - 10), 10)
        pg.draw.line(self.screen, BLACK, (WIDTH - 10, 10), (WIDTH - 10, HEIGHT - 10), 10)

        pg.draw.line(self.screen, BLACK, (10, HEIGHT / 3), (WIDTH - 10, HEIGHT / 3), 10)
        pg.draw.line(self.screen, BLACK, (10, HEIGHT * 2 / 3), (WIDTH - 10, HEIGHT * 2 / 3), 10)
        pg.draw.line(self.screen, BLACK, (WIDTH / 3, 10), (WIDTH / 3, HEIGHT - 10), 10)
        pg.draw.line(self.screen, BLACK, (WIDTH * 2 / 3, 10), (WIDTH * 2 / 3, HEIGHT - 10), 10)

        pg.draw.line(self.screen, BLACK, (10, HEIGHT / 9), (WIDTH - 10, HEIGHT / 9), 5)
        pg.draw.line(self.screen, BLACK, (10, HEIGHT * 2 / 9), (WIDTH - 10, HEIGHT * 2 / 9), 5)
        pg.draw.line(self.screen, BLACK, (10, HEIGHT * 4 / 9), (WIDTH - 10, HEIGHT * 4 / 9), 5)
        pg.draw.line(self.screen, BLACK, (10, HEIGHT * 5 / 9), (WIDTH - 10, HEIGHT * 5 / 9), 5)
        pg.draw.line(self.screen, BLACK, (10, HEIGHT * 7 / 9), (WIDTH - 10, HEIGHT * 7 / 9), 5)
        pg.draw.line(self.screen, BLACK, (10, HEIGHT * 8 / 9), (WIDTH - 10, HEIGHT * 8 / 9), 5)

        pg.draw.line(self.screen, BLACK, (WIDTH / 9, 10), (WIDTH / 9, HEIGHT - 10), 5)
        pg.draw.line(self.screen, BLACK, (WIDTH * 2 / 9, 10), (WIDTH * 2 / 9, HEIGHT - 10), 5)
        pg.draw.line(self.screen, BLACK, (WIDTH * 4 / 9, 10), (WIDTH * 4 / 9, HEIGHT - 10), 5)
        pg.draw.line(self.screen, BLACK, (WIDTH * 5 / 9, 10), (WIDTH * 5 / 9, HEIGHT - 10), 5)
        pg.draw.line(self.screen, BLACK, (WIDTH * 7 / 9, 10), (WIDTH * 7 / 9, HEIGHT - 10), 5)
        pg.draw.line(self.screen, BLACK, (WIDTH * 8 / 9, 10), (WIDTH * 8 / 9, HEIGHT - 10), 5)

        pg.display.flip()
