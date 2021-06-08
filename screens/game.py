# PyGame
from screens.gameover import *
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
        self.level = 0
        self.point_balls_eaten = 0
        
        # Sprites
        self.sprites = {}
        self.pellets = PointBallGroup("assets/bolinhas.txt")
        self.sprites["pacman-1"] = Pacman(self.nodes)
        self.sprites["pacman-2"] = Pacman(self.nodes)
        self.sprites["pinky"] = Pinky(self.nodes)
        self.sprites["blinky"] = Blinky(self.nodes)
        self.sprites["inky"] = Inky(self.nodes)
        self.sprites["clyde"] = Clyde(self.nodes)

        # Ghosts
        self.ghosts = [self.sprites["pinky"],
                       self.sprites["blinky"], self.sprites["inky"],
                       self.sprites["clyde"]]

        # PacMans
        self.pacmans = [self.sprites["pacman-1"], self.sprites["pacman-2"]]

        # Other stuff
        self.gOver = GameOverScreen(window)
        self.Over = False

        # Lógica do PacMan assassino
        self.last_super_points = self.pellets.super_point_balls

        # Musica
        music = pygame.mixer.music.load('assets/home_track.ogg')
        pygame.mixer.music.play(1)

    def update(self):
        """
        Atualiza o status de todos os sprites
        """

        if self.Over != True:
        # Aqui definimos um delta de tempo entre um update e outro.
        # Isso, na prática, se traduz ao número de Frames por Segundo (FPS)
            dt = self.clock.tick(game_config.GameDimensions.fps) / 1000.0

            # Agora vamos propagar a mudança de tempo nos sprites
            for sprite in self.sprites.values():
                sprite.update(dt)

            for pacman in self.pacmans.values():
                pacman.collide_with_ghost(self.ghosts)

            # E atualizar os outros componentes do jogo
            self.pellets.update(dt)
            self.check_point_ball_events()
            self.check_pacman_mode()
            self.Death()

            # Finalmente, vamos mostrar o objeto atualizado na tela
            self.render()

        else:
            self.gOver.update()
            return self.music()


    def music(self):
        if self.Over != True:
            # Musica de Game Over
            music = pygame.mixer.music.load('assets/home_track.ogg')
            pygame.mixer.music.play(1)            

    def check_point_ball_events(self):
        """
        Este método verifica os eventos com PointBalls e atualiza a nossa lista
        de PointBalls dentro da nossa instância do point_balls_list
        """
        point_ball = self.pacman.eat_point_balls(self.pellets.point_balls_list, self.pellets.super_point_balls,
                                                 self.ghosts)

        # Será que precisamos remover alguma point_ball???
        if point_ball:
            self.pellets.point_balls_list.remove(point_ball)
            eatball = pygame.mixer.Sound("assets/barulinho_comer.ogg")
            eatball.play()

    def resetLevel(self):
        Pacman.resetPacman(self.nodes)
        PointBallGroup.resetPointball('assets/bolinhas.txt')
        Blinky.resetBlinky(self.nodes)
        Pinky.resetPinky(self.nodes)
        Inky.resetInky(self.nodes)
        Clyde.resetClyde(self.nodes)

    def levelController(self):
        if self.pellets.is_empty():
            self.level += 1
            self.resetLevel()
            print(self.level)

    def check_pacman_mode(self):

        # O self.clock % 12 define um tempo relativamente aleatório para quanto tempo
        # o Pac-Man ficará assassino pois nunca saberemos o self.clock atual
        # Ex. Pode ser que o modo dure 1 segundo ou 12
        if pygame.time.get_ticks() % 1000 == 0:

            self.reset_victim_pacman()

    def reset_victim_pacman(self):
       self.pacman.mode = game_config.PacManStatus.Victim

       for ghost in self.ghosts:
           ghost.color = ghost.defaultcolor

    def Death(self):
        if self.pacman.lives == -1:
            self.Over = True

    def render(self):
        """
        Este método serve apenas para renderizar os nossos objetos na GUI
        """
        # Vamos apagar a tela
        # Background
        self.window.blit(pygame.image.load("assets/tabuleiro.png"), (0, 0))

        # E agora renderizar o jogo
        self.nodes.render(self.window)
        self.pellets.render(self.window)
        self.pacman.render(self.window)
        self.pinky.render(self.window)
        self.blinky.render(self.window)
        self.inky.render(self.window)
        self.clyde.render(self.window)
        pygame.display.update()
