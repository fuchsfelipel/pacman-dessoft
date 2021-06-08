# PyGame
import pygame

# JSON
import json

# DIY
import game_config

class HighscoreScreen:
    def __init__(self, window):
        self.window = window
        
    def update(self):
        # Background
        self.window.blit(pygame.image.load("assets/highscore.png"), (0, 0))
        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            return game_config.GameStatus.home
        else:
            return game_config.GameStatus.highScore
        