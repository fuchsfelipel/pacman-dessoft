# PyGame
import pygame

# DIY
import game_config

# Outros
import os

class HomeScreen:
    def __init__(self, window):
        # Setup geral
        self.window = window

    def update(self):

        # Background
        self.window.blit(pygame.image.load("assets/home.png"), (0, 0))
        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            return game_config.GameStatus.game

        elif key[pygame.K_h]:
            return game_config.GameStatus.highScore

        else:
            return game_config.GameStatus.home
