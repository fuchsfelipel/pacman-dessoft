# --- Imports ---
import pygame

import game_config
import screens.game

# Setup do PyGame
pygame.init()
window = pygame.display.set_mode(game_config.GameDimensions.screen_size, 0, 32)
pygame.display.set_caption('PacMan | Dessoft - Insper')

# Telas
game = screens.game.GameScreen(window)

status = game_config.GameStatus.game
while status != game_config.GameStatus.quit:
    # Ver se o usuário quer sair
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = game_config.GameStatus.quit

    game.update()
