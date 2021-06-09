"""
Este módulo define as configurações do jogo.
Ele se trata de uma coleção de classes estáticas, sem construtores. Apenas constantes.
"""
from utils.vector import Vector2


class GameDimensions:
    """
    Especificações da tela de jogo.
    """
    # Vamos usar um sistema de colunas e fileiras
    # Ou seja, uma tabela
    tile_w = 16     # Altura de uma célula
    tile_h = 16     # Largura de uma célular
    row_num = 36    # Número de Fileiras
    col_num = 28    # Número de Colunas

    # Configurações de Display
    fps = 60    # FPS do Jogo --> Usado para o Clock.tick
    screen_w = tile_w * col_num # Largura da Tela
    screen_h = tile_h * row_num # Altura da Tela
    screen_size = (screen_w, screen_h)
    screen_center = (screen_w // 2, screen_h // 2)

# Cores: https://www.schemecolor.com/pac-man-game-colors.php


class Colors:
    # Google ´nome da cor hex
    """"Paleta de cores do jogo"""
    brown = "#964B00"  # Clyde
    green = "#00FF00"
    orange = '#FFA500'
    red = "#FD0000"  # Blink
    tumbleweed = "#DEA185"
    bluebonnet = "#2121DE"
    neonBlue = "#1919A6"  # Inky
    yellow = "#FFFF00"  # Pac-Man
    black = "#000000"
    pink = "#FF007F"  # Pinky


class GameStatus:
    """Status possíveis para o jogo"""
    quit = "QUIT"
    game = "GAME"
    home = "HOME"
    highScore = "HIGH"
    gameOver = "OVER"


class Movements:
    """
    Define todos os movimentos possíveis com Vetores 2-D
    """
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    STOP = Vector2(0, 0)

    # O método abaixo não foi transformado em uma função
    # por uma questão de organização. Desta maneira, sinalizei-o
    # como estático para o interpretador
    @staticmethod
    def reverse(direction):
        """
        Retorna o inverso da direção
        :param direction: Direção
        :type direction: Movements
        :return: Nova direção
        """
        if direction is Movements.UP:
            return Movements.DOWN
        elif direction is Movements.DOWN:
            return Movements.UP
        elif direction is Movements.LEFT:
            return Movements.RIGHT
        elif direction is Movements.RIGHT:
            return Movements.LEFT


class Points:
    """
    Define os pontos de cada coisa
    """
    point_balls = 10
    pacman_lives = 3  # o Pac-Man vai começar com 3 vidas
    super_point_balls = 50
    ghost_point = 100


class PacManStatus:
    """
    A qualquer momento o Pac-Man pode estar em dois estados:
    - Assasino: Ele come os fantasmas
    - Vítima: Ele é comido pelos fantasmas
    """
    Victim = 0
    Assassin = 1
