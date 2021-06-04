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

        # Musica
        music = pygame.mixer.music.load('assets/gameover_SFX.mp3')
        pygame.mixer.music.play(1)

        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            return game_config.GameStatus.game

        elif key[pygame.K_h]:
            return game_config.GameStatus.highScore

        else:
            return game_config.GameStatus.gameOver

