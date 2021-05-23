from utils.vector import Vector2

class GameDimensions():
    tile_w = 16
    tile_h = 16
    row_num = 36
    col_num = 28
    screen_w = tile_w * col_num
    screen_h = tile_h * row_num
    screen_size = (screen_w, screen_h)

# Cores: https://www.schemecolor.com/pac-man-game-colors.php
class Colors:
    """"Paleta de cores do jogo"""
    green = "#00FF00"
    red = "#FD0000"
    tumbleweed = "#DEA185"
    bluebonnet = "#2121DE"
    neonBlue = "#1919A6"
    yellow = "#FFFF00"
    black = "#000000"


class GameStatus:
    """Status possíveis para o jogo"""
    quit = "QUIT"
    game = "GAME"
    home = "HOME"
    highScore = "HIGH"
    gameOver = "OVER"


class Movements:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    STOP = Vector2(0, 0)


class Points():
    balls = 10

