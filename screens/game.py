# PyGame
import pygame
from pygame.locals import *

# Módulos DIY
import game_config
from sprites.pacman import Pacman
from sprites.pinky import Pinky
from sprites.blinky import Blinky
from sprites.inky import Inky
from sprites.clyde import Clyde
from malha import NodeGroup
from sprites.point_balls import PointBallGroup


class GameScreen:
    """
    Define a tela de jogo
    Classe inspirada no tutorial PacManCode
    """
    def __init__(self, window):
        """
        Inicia uma novar partida do jogo
        :param window: Janela do PyGame
        """
        # Detalhes Básicos
        self.window = window

        self.background = pygame.surface.Surface(game_config.GameDimensions.screen_size).convert()
        self.background.fill(game_config.Colors.black)

        # Mapa & Ambiente
        self.clock = pygame.time.Clock()  # Define um relógio de jogo que será usado para a movimentação de sprites.
        self.nodes = NodeGroup("assets/tabuleiro.txt")

        # Sprites
        self.pellets = PointBallGroup("assets/bolinhas.txt")
        self.pacman = Pacman(self.nodes)
        self.pinky = Pinky(self.nodes)
        self.blinky = Blinky(self.nodes)
        self.inky = Inky(self.nodes)
        self.clyde = Clyde(self.nodes)
        # Musica
        music = pygame.mixer.music.load('assets/home_track.ogg')
        pygame.mixer.music.play(1)

    def update(self):
        """
        Atualiza o status de todos os sprites
        """

        # Aqui definimos um delta de tempo entre um update e outro.
        # Isso, na prática, se traduz ao número de Frames por Segundo (FPS)
        dt = self.clock.tick(game_config.GameDimensions.fps) / 1000.0

        # Agora vamos propagar a mudança de tempo nos sprites
        self.pacman.update(dt)
        self.pinky.update(dt)
        self.blinky.update(dt)
        self.inky.update(dt)
        self.clyde.update(dt)
        self.pellets.update(dt)
        self.check_point_ball_events()

        # Finalmente, vamos mostrar o objeto atualizado na tela
        self.render()

    def check_point_ball_events(self):
        """
        Este método verifica os eventos com PointBalls e atualiza a nossa lista
        de PointBalls dentro da nossa instância do point_balls_list
        """
        point_ball = self.pacman.eat_point_balls(self.pellets.point_balls_list)

        # Será que precisamos remover alguma point_ball???
        if point_ball:
            self.pellets.point_balls_list.remove(point_ball)

    def render(self):
        """
        Este método serve apenas para renderizar os nossos objetos na GUI
        """
        # Vamos apagar a tela
        # Background
        self.window.blit(pygame.image.load("assets/tabuleiro.png"), (150, 150))

        # E agora renderizar o jogo
        self.nodes.render(self.window)
        self.pellets.render(self.window)
        self.pacman.render(self.window)
        self.pinky.render(self.window)
        self.blinky.render(self.window)
        self.inky.render(self.window)
        self.clyde.render(self.window)
        pygame.display.update()
