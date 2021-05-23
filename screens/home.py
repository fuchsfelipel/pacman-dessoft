# PyGame
import pygame

import game_config


class HomeScreen:
    def __init__(self, window):
        # Setup geral
        self.window = window

        # Background
        self.background = pygame.surface.Surface(game_config.GameDimensions.screen_size).convert()
        self.background.fill(game_config.Colors.black)
        self.window.blit(self.background, (0, 0))

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            return game_config.GameStatus.game

        elif key[pygame.K_h]:
            return game_config.GameStatus.highScore

        else:
            return game_config.GameStatus.home
