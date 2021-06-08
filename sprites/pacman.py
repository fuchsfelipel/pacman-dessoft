# --- Imports ---
# PyGame
import random
import time

import pygame
import json

# Módulo DIY
import game_config
import utils.movement_translator
from sprites import inky, blinky, pinky, clyde

class Pacman(object):
    """
    Esta classe define o Pac-Man.
    Em grande parte, sua lógica deve-se ao tutorial pacmancode
    Dito isso, existe uma boa quantidade de código original ou refatorado/otimizado
    Mudanças pontuais de lógica e regras de negócio também ocorreram
    """

    def __init__(self, nodes, key_up, key_down, key_right, key_left):
        """
        Cria uma nova instância do Pac-Man
        :param nodes: Nós da malha de movimentação
        """
        # Dados básicos do Pac-Man
        self.name = "pacman"
        self.collideRadius = 5
        self.radius = 10
        self.color = game_config.Colors.yellow

        # Por padrão o Pac-Man é comido por fantasmas
        self.mode = game_config.PacManStatus.Victim

        # Loading do ambiente
        self.nodes = nodes
        self.node = nodes.node_list[0]

        # Dados de movimentação
        self.direction = game_config.Movements.STOP
        self.speed = 100
        self.position = self.node.position.copy()
        self.target = self.node
        self.set_position()

        # Coisas de Placar
        self.points = 4500
        self.lives = game_config.Points.pacman_lives

        # Exibição das Vidas
        self.livesh = game_config.GameDimensions.tile_h
        self.livesr = game_config.GameDimensions.row_num

        # Teclas
        self.key_up = key_up
        self.key_down = key_down
        self.key_right = key_right
        self.key_left = key_left

    def set_position(self):
        """
        Define a posição do Pac-Man para algo discreto na malha
        """
        self.position = self.node.position.copy()

    def portal(self):
        """
        Este método serve para teleportar o Pac-Man de um lado
        da malha para o outro.
        """
        if self.node.portal_node:
            # Prepara o Pac-Man para a mudança de posição
            self.node = self.node.portal_node
            self.set_position()

    def update(self, dt):
        """
        Este é o método que precisa ser invocado pelo loop de jogo.
        Ele faz todos os update necessários no Pac-Man
        :param dt: Delta de tempo
        """
        # Mudança de posição usando a forma vetorial de S = v*t
        self.position += self.direction * self.speed * dt

        # Verificar a nova direção do Pac-Man
        direction = utils.movement_translator.movement_translator(pygame.key.get_pressed(), self.key_up, self.key_down, self.key_right, self.key_left)

        # Se houver nova direção --> iniciar novo movimento
        if direction:
            self.move_by_key(direction)

        # Ou continuar o último...
        else:
            self.move_by_self()

    def resetPacman(self, nodes):
        self.node = nodes.node_list[0]
        self.speed += 0.3 * self.speed
        self.set_position()
        self.target = self.node
        self.direction = game_config.Movements.STOP
        
    def move_by_self(self):
        """
        Este método faz com que o Pac-Man continue seu último movimento
        """
        if (self.direction is not game_config.Movements.STOP) and self.overshot_target():
            self.node = self.target

            # Bati em um portal?
            self.portal()

            # Será que o Pac-Man bateu com o nariz na parede?
            if self.node.neighbors[self.direction] is not None:
                self.target = self.node.neighbors[self.direction]
            else:
                self.set_position()
                self.direction = game_config.Movements.STOP

    def move_by_key(self, direction):
        """
        Este método inicia um novo movimento no Pac-Man
        (Ou seja, muda de direção)
        """
        # Se o Pac-Man estiver parado
        if (self.direction is game_config.Movements.STOP) and (self.node.neighbors[direction] is not None):
            self.target = self.node.neighbors[direction]
            self.direction = direction

        # Toda reversão de direção é permitida, pois é impossível colidir com a parede.
        elif direction == self.direction * -1:
            self.reverse_direction()

        # Se o Pac-Man passou do alvo definido
        elif self.overshot_target():
            # Vamos redefinir sua posição atual para a meta estabelecida
            # na ultima iteração
            self.node = self.target

            # Pode ser que ele passou do ponto por causa de um portal
            self.portal()

            # Agora sim vamos mudar sua posição
            # Se houver uma nova direção nesta iteração
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                if self.direction != direction:
                    self.set_position()
                    self.direction = direction

            else:
                # Vamos usar o try para descartar teclas inválidas
                try:
                    # Se a direção não for None vamos mudar o target
                    if self.node.neighbors[self.direction] is not None:
                        self.target = self.node.neighbors[self.direction]

                    # ou parar o Pac-Man
                    else:
                        self.set_position()
                        self.direction = game_config.Movements.STOP
                except:
                    pass

    def overshot_target(self):
        """
        Aqui nós verificamos se o Pac-Man passou de seu alvo,
        O que é um alvo? Bom, neste projeto estamos trabalhando
        com uma malha discreta de "quadradinhos". Como o PyGame
        trabalha com pixeis, a cada iteração temos que verificar
        se o Pac-man encontra-se em um dos pontos discretos da malha
        ou se ele o ultrapassou. Como sabemos se ele ultrapassou?
        A cada iteração nós definimos um novo alvo (target).
        """
        # Null-safety
        if self.target is not None:
            v_1 = self.target.position - self.node.position
            v_2 = self.position - self.node.position
            return v_2.magnitudeSquared() >= v_1.magnitudeSquared()

        return False

    def reverse_direction(self):
        """
        Este método inverte a direção do Pac-Man
        """
        # Calcular e armazenar o inverso da direção
        self.direction = game_config.Movements.reverse(self.direction)

        # Vamos inverter o alvo
        self.node, self.target = self.target, self.node

    def eat_point_balls(self, point_list, superpoint_list, ghosts):
        """
        Este método faz com que o Pac-Man coma bolinhas
        :param point_list:
        """
        for ball in point_list:
            # Se de fato o Pac-Man colidiu com o ponto
            if (self.position - ball.position).magnitudeSquared() <= (ball.radius + self.collideRadius) ** 2:
                # Soma os pontos ao placar atual
                self.points += game_config.Points.point_balls
                if (ball in superpoint_list):
                    # Soma os pontos ao placar atual
                    self.points += game_config.Points.super_point_balls
                    self.mode = game_config.PacManStatus.Assassin
                    for ghost in ghosts:
                        ghost.color = "navy"
                return ball
        if self.points == 5000:
            self.lives += 1
            self.points = 0
        pygame.mixer.music.stop()
        return None

    def collide_with_ghost(self, ghosts):
        """
        Este método faz com que o Pac-Man morra ao tocar em um fantasma
        :param point_list:
        """
        for ghost in ghosts:
            # Se de fato o Pac-Man colidiu com o ponto
            if (self.position - ghost.position).magnitudeSquared() <= (ghost.radius + self.collideRadius) ** 2:
                # PacMan morre
                if self.mode == game_config.PacManStatus.Victim:
                    self.node = self.nodes.node_list[random.choice([5, 15, 25, 35])]
                    self.set_position()
                    self.lives -= 1
                else:
                    self.points += game_config.Points.ghost_point
                    ghost.be_eaten()
 

    def render(self, screen):
        """
        (Re)desenha o Pac-Man na tela com os dados atualizados.
        :param screen: Tela do PyGame
        """
        # Desenha um círculo na tela
        pygame.draw.circle(screen, self.color, self.position.asInt(), self.radius)
        
        # Escreve o Score na tela
        x = 5 + self.radius + (2 * self.radius + 5) * 10
        y = (self.livesh - 1) * self.livesr

        white = (255, 255, 255)
        font = pygame.font.SysFont(None, 40)
        Hi = font.render('HI', True, white)
        screen.blit(Hi, (x, y))

        score = font.render(str(self.points), True, white)
        screen.blit(score, (x + 60, y))

        # Desenha as vidas na tela
        for i in range(self.lives):
            x = 5 + self.radius + (2 * self.radius + 5) * i
            y = self.livesh * (self.livesr - 1)
            pygame.draw.circle(screen, self.color, (x, y), self.radius)
