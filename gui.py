import sys
import pygame as pg

from grid import Grid

class GUI:
    def __init__(self):
        self.grid = Grid()
        pg.init()
        self.screenWidth, self.screenHeight = 750, 750
        self.screen = pg.set_mode(self.screenSize)
    
    @property
    def screenSize(self):
        return (self.screenWidth, self.screenHeight)
    
    def initGame(self):
        self.grid.initRandomGrid()
