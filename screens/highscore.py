# PyGame
import pygame

# JSON
import json

# DIY
import game_config

class HighscoreScreen:
    def __init__(self, window):
        self.window = window
        self.nodes = NodeGroup('assets/tabuleiro.txt')
        self.pont = Pacman(self.nodes).points
       
    def update(self):
        # Background
        self.window.blit(pygame.image.load("assets/highscore.png"), (0, 0))
        pygame.display.flip()

        # Abre o arquivo JSON para leitura
        with open('score.json', 'r') as file:
            score = file.read()

        # Converte o arquivo de JSON para Python
        pont = json.loads(score)
        
        # TODO: Printa a pontuação na tela
        white = (255, 255, 255)
        font = pygame.font.SysFont(None, 40)
        hi = font.render(str(pont), True, white)
        self.window.blit(hi, (224, 288))

        # Converte o arquivo de Python para JSON
        tojson = json.dumps(pont)

        # Salva o arquivo em JSON
        with open('score.json', 'w') as arquivo_json:
            arquivo_json.write(tojson)

        key = pygame.key.get_pressed()
        if key[pygame.K_e]:
            return game_config.GameStatus.home
        else:
            return game_config.GameStatus.highScore

        
