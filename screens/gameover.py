"""
Este módulo define a tela de gameover.
"""
# PyGame
import pygame

# DIY
import game_config

# Outros
import os

class GameOverScreen:
    """
    Esta classe define a tela de gameover.
    """
    def __init__(self, window):
        """
        Este construtor criar uma nova instância da tela de gameove.
        Para fazer isso é necessário passar o argumento windows
        @param window: Tela do PyGame
        """
        self.window = window
        self.lives = game_config.Points.pacman_lives

    def update(self):
        """
        Esse método atualiza a tela de jogo. Neste caso a única mudança é
        renderizá-la novamente.
        """
        self.window.blit(pygame.image.load("assets/gameover_screen.jpg"), (0, 0))
        pygame.display.flip()

