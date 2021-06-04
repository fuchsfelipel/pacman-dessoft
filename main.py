# --- Imports ---
import pygame
from pygame.constants import KEYDOWN

import game_config

import screens.game
import screens.home
import screens.highscore
import screens.gameover

# Setup do PyGame
pygame.init()
window = pygame.display.set_mode(game_config.GameDimensions.screen_size, 0, 32)
pygame.display.set_caption('PacMan | Dessoft - Insper')

play = True

# Telas
game = screens.game.GameScreen(window)
home = screens.home.HomeScreen(window)
gameover = screens.gameover.GameOverScreen(window)


status = game_config.GameStatus.home
while status != game_config.GameStatus.quit:
    # Ver se o usuário quer sair
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = game_config.GameStatus.quit

    if status == game_config.GameStatus.game:
        game.update()
        # if status == game_config.GameStatus.gameOver:
        #     status == gameover.update()
    elif status == game_config.GameStatus.home:
        status = home.update()

