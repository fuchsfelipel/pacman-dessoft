"""
Este módulo define a tela de jogo.
"""
# PyGame
from screens.gameover import *
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_w, K_s, K_d

# Módulos DIY
import game_config
from sprites.pacman import Pacman
from sprites.ghost import Ghost
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
        self.sprites["pacman-1"] = Pacman(self.nodes, K_UP, K_DOWN, K_RIGHT, K_LEFT, game_config.Colors.yellow, 5)
        self.sprites["pacman-2"] = Pacman(self.nodes, K_w, K_s, K_d, K_a, game_config.Colors.orange, 150)
        self.sprites["pinky"] = Ghost(self.nodes, game_config.Colors.red, 10)
        self.sprites["blinky"] = Ghost(self.nodes, game_config.Colors.pink, 20)
        self.sprites["inky"] = Ghost(self.nodes, game_config.Colors.brown, 30)
        self.sprites["clyde"] = Ghost(self.nodes, game_config.Colors.green, 40)

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

    def reset(self):
        """
        Este método reseta as point_balls. Ele faz parte do PacMan mudar de nível.
        """
        # Se todas as point_balls tiverem sido comidas
        if self.point_balls_eaten == 250:
            for sprite in self.sprites.values():
                sprite.reset(self.nodes)

            self.pellets.resetPointball('assets/bolinhas.txt')
            self.point_balls_eaten = 0

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

            for pacman in self.pacmans:
                pacman.collide_with_ghost(self.ghosts)

            # E atualizar os outros componentes do jogo
            self.pellets.update(dt)
            self.check_point_ball_events()
            self.check_pacman_mode()
            self.death()
            self.reset()

            # Finalmente, vamos mostrar o objeto atualizado na tela
            self.render()

        else:
            self.gOver.update()

    def check_point_ball_events(self):
        """
        Este método verifica os eventos com PointBalls e atualiza a nossa lista
        de PointBalls dentro da nossa instância do point_balls_list
        """
        for pacman in self.pacmans:
            point_ball = pacman.eat_point_balls(self.pellets.point_balls_list, self.pellets.super_point_balls,
                                                self.ghosts)

            # Será que precisamos remover alguma point_ball???
            if point_ball:
                self.pellets.point_balls_list.remove(point_ball)
                eatball = pygame.mixer.Sound("assets/barulinho_comer.ogg")
                eatball.play()

    def reset_level(self):
        """
        Este método reseta o tabuleiro de jogo e todos os sprites
        @return:
        """
        for sprite in self.sprites:
            sprite.reset(self.nodes)

        PointBallGroup.resetPointball('assets/bolinhas.txt')

    def level_controller(self):
        """
        Este método server para controlar o nível do jogo.
        Quando não há mais point_balls ele invoca os outros métodos
        envolvidos no reset
        """
        if self.pellets.is_empty():
            self.level += 1
            self.reset_level()
            print(self.level)

    def check_pacman_mode(self):
        """
        Este método faz com que os Pacmans voltem de a ser vítimas e homogieniza o status.
        """

        # Se algum dos Pacmans tiver comida uma super point ball
        # vamos fazer com que o outro também vire assassino.
        for pacman in self.pacmans:
            if pacman.mode is game_config.PacManStatus.Assassin:
                for pacman in self.pacmans:
                    pacman.mode = game_config.PacManStatus.Assassin

        # O self.clock % 12 define um tempo relativamente aleatório para quanto tempo
        # o Pac-Man ficará assassino pois nunca saberemos o self.clock atual
        # Ex. Pode ser que o modo dure 1 segundo ou 12
        if pygame.time.get_ticks() % 1000 == 0:
            for pacman in self.pacmans:
                pacman.mode = game_config.PacManStatus.Victim

            for ghost in self.ghosts:
                ghost.color = ghost.defaultcolor

    def death(self):
        """
        Este método define o que é um gameover e checa se ele ocorreu.
        @return:
        """
        for pacman in self.pacmans:
            if pacman.lives == -1:
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
        for sprite in self.sprites.values():
            sprite.render(self.window)
        pygame.display.update()
