import pygame

import game_config
from game_config import *


class PointBall(object):
    def __init__(self, x, y):
        self.name = "pellet"
        self.position = Vector2(x, y)
        self.color = game_config.Colors.tumbleweed
        self.radius = 4
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class PowerPointBall(PointBall):
    def __init__(self, x, y):
        PointBall.__init__(self, x, y)
        self.name = "powerpellet"
        self.radius = 8
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        # self.pelletSymbols = ["p", "n", "Y"]
        # self.powerpelletSymbols = ["P", "N"]
        self.createPelletList(pelletfile)

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def createPelletList(self, pelletfile):
        grid = self.readPelletfile(pelletfile)
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 'p':
                    self.pelletList.append(PointBall(col * game_config.GameDimensions.tile_w, row * game_config.GameDimensions.tile_h))
                elif grid[row][col] == 'P':
                    pp = PowerPointBall(col * game_config.GameDimensions.tile_w, row * game_config.GameDimensions.tile_h)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
