import pygame

import game_config
from game_config import *

"""
Este módulo implementa as bolinhas de pontuação do jogo.
Sua lógica e estrutra foi copiada do tutorial PacManCode
porém houve refatorações e otimizações significativas.
Mudanças pontuais de lógica e regras de negócio também
ocorreram
"""


class PointBall(object):
    """
    Esta classe implemente um template para as point_balls
    """
    def __init__(self, x, y):
        """
        Instancia uma nova point_ball
        :param x: Posição em X
        :param y: Posicão em Y
        """
        # Dados básicos
        self.name = "point_ball"
        self.color = game_config.Colors.tumbleweed
        self.radius = 4
        self.points = game_config.Points.point_balls

        # Dados de Posicionamenteo
        self.position = Vector2(x, y)
        self.visible = True

    def render(self, screen):
        """
        Renderiza a point_ball na tela.
        :param screen: Tela do PyGame
        """
        if self.visible:
            pygame.draw.circle(screen, self.color, self.position.asInt(), self.radius)


class SuperPointBall(PointBall):
    """
    Esta classe cria as point_balls com super poderes
    """
    def __init__(self, x, y):
        """
        Inicializa uma nova SuperPointBall
        :param x: Posição em X
        :param y: Posição em Y
        """
        # Uma SuperPointBall não deixa de ser uma PointBall
        # então vamos instanciar uma PointBall normal
        PointBall.__init__(self, x, y)

        # Dados básicos
        self.name = "super_point_ball"
        self.radius = 8
        self.points = game_config.Points.super_point_balls
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        """
        Atualiza a SuperPointBall --> Ou seja, faz ela piscar.
        :param dt:
        :return:
        """
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
                    self.point_balls_list.append(PointBall(col * game_config.GameDimensions.tile_w,
                                                           row * game_config.GameDimensions.tile_h))
                elif grid[row][col] == 'P':
                    pp = SuperPointBall(col * game_config.GameDimensions.tile_w,
                                        row * game_config.GameDimensions.tile_h)
                    self.point_balls_list.append(pp)
                    self.super_point_balls.append(pp)

    @staticmethod
    def read_point_balls_file(point_balls_file):
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
