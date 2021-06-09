# PyGame
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_w, K_s, K_d

# JSON
import json

# DIY
import game_config
from malha import NodeGroup


class HighscoreScreen:
    def __init__(self, window):
        self.window = window
        self.nodes = NodeGroup('assets/tabuleiro.txt')

    def update(self):
        # Background
        self.window.blit(pygame.image.load("assets/highscore.png"), (0, 0))

        # Abre o arquivo JSON para leitura
        with open('highscore.json', 'r') as file:
            hs = file.read()

        with open('score.json', 'r') as file:
            s = file.read()

        # Converte o arquivo de JSON para Python
        hs = json.loads(hs)
        s = json.loads(s)

        if hs < s:
            hs = s

        white = (255, 255, 255)
        font = pygame.font.SysFont(None, 40)
        txt = font.render('High Score', True, white)
        hi = font.render(str(hs), True, white)
        self.window.blit(txt, (50, 288))
        self.window.blit(hi, (224, 288))

        # Converte o arquivo de Python para JSON
        tojson = json.dumps(hs)

        # Salva o arquivo em JSON
        with open('highscore.json', 'w') as arquivo_json:
            arquivo_json.write(tojson)

        pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            return game_config.GameStatus.home
        else:
            return game_config.GameStatus.highScore
