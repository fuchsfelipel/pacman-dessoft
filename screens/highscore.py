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
        with open('score.json', 'w+') as score:
            hs = score.read()

        

        white = (255, 255, 255)

        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render('High-Score', True, white)

        center = game_config.GameDimensions.screen_center

        # Background
        self.window.blit(pygame.image.load("assets/highscore.png"), (0, 0))
        pygame.display.flip()

        self.window.blit(text, center)

        pygame.display.update()

        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            return game_config.GameStatus.home
        else:
            return game_config.GameStatus.highScore
        