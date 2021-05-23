import pygame

import game_config
from game_config import *


class PointBall(object):
    """
    Esta classe implementa as bolinhas de pontuação do jogo.
    Sua lógica e estrutra foi copiada do tutorial PacManCode
    porém houve refatorações e otimizações significativas.
    Mudanças pontuais de lógica e regras de negócio também
    ocorreram
    """
    def __init__(self, x, y):
        self.name = "point_ball"
        self.position = Vector2(x, y)
        self.color = game_config.Colors.tumbleweed
        self.radius = 4
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class SuperPointBall(PointBall):
    def __init__(self, x, y):
        PointBall.__init__(self, x, y)
        self.name = "super_point_ball"
        self.radius = 8
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class PointBallGroup(object):
    def __init__(self, point_balls_file):
        self.point_balls_list = []
        self.super_point_balls = []
        self.create_point_balls_list(point_balls_file)

    def update(self, dt):
        for super_point_balls in self.super_point_balls:
            super_point_balls.update(dt)

    def create_point_balls_list(self, point_balls_file):
        grid = self.read_point_balls_file(point_balls_file)
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 'p':
                    self.point_balls_list.append(PointBall(col * game_config.GameDimensions.tile_w, row * game_config.GameDimensions.tile_h))
                elif grid[row][col] == 'P':
                    pp = SuperPointBall(col * game_config.GameDimensions.tile_w, row * game_config.GameDimensions.tile_h)
                    self.point_balls_list.append(pp)
                    self.super_point_balls.append(pp)

    def read_point_balls_file(self, point_balls_file):
        f = open(point_balls_file, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    def is_empty(self):
        if len(self.point_balls_list) == 0:
            return True
        return False

    def render(self, screen):
        for point_ball in self.point_balls_list:
            point_ball.render(screen)
