"""
Este módulo define a home screen.
"""
# PyGame
import pygame

# DIY
import game_config

# Outros
import os

class HomeScreen:
    """
    Esta classe define a home screen.
    """
    def __init__(self, window):
        """
        Este construtor cria uma nova instância da home screen.
        :@param window: Tela de jogo do PyGame
        """
        # Setup geral
        self.window = window

    def update(self):
        """
        Este método atualiza a home screen. Além de renderizar a tela,
        este método é responsável por detectar a intenção do jogador iniciar
        o jogo ou ver o placar.
        """
        # Background
        self.window.blit(pygame.image.load("assets/home.png"), (0, 0))
        pygame.display.flip()

        key = pygame.key.get_pressed()

        # Aperte c para jogar
        if key[pygame.K_c]:
            return game_config.GameStatus.game

        # Aperte h para ver o placa
        elif key[pygame.K_h]:
            return game_config.GameStatus.highScore

        # Ou continue nessa tela...
        else:
            return game_config.GameStatus.home
