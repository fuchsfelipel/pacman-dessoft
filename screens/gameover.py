# PyGame
import pygame

# DIY
import game_config

# Outros
import os

class GameOverScreen:
    def __init__(self, window):
        self.window = window
        self.lives = game_config.Points.pacman_lives

    def update(self):
        self.window.blit(pygame.image.load("assets/gameover_screen.jpg"), (0, 0))
        pygame.display.flip()

