"""
Este módulo define um fantasma.
"""
# --- Imports ---
# PyGame
import time
import random
import pygame

# Módulo DIY
import game_config
import utils.movement_translator


class Ghost:
    """
    Esta classe define um fantasma.
    """
    def __init__(self, nodes, color:game_config.Colors, start_node:int, image):
        """
        Este contrutor retorna um novo fantasma
        @param nodes: Os nós do tabuleiro (a malha)
        @param color: Cor do fantasma
        @param start_node: Posição inicial do fantasma
        """
        # Dados básicos do Pac-Man
        self.collideRadius = 5
        self.radius = 10
        self.defaultcolor = color
        self.color = color
        self.start_position = start_node
        self.image = image
        self.default_image = image

        # Loading do ambiente
        self.nodes = nodes

        # Define a posição inicial
        self.node = nodes.node_list[start_node]

        # Dados de movimentação
        self.direction = utils.movement_translator.movement_ghosts(random.randint(0,3))
        self.speed = 100
        self.position = self.node.position.copy()
        self.target = self.node
        self.set_position()

    def reset(self, nodes):
        """
        Este método reseta o fantasma para seu status original
        @param nodes: Nós da malha (tabuleiro)
        """
        self.node = nodes.node_list[self.start_position]
        self.speed += 0.5 * self.speed
        self.set_position()
        self.target = self.node
        self.direction = utils.movement_translator.movement_ghosts(random.randint(0,3))

    def set_position(self):
        """
        Define a posição do Ghost para algo discreto na malha
        """
        self.position = self.node.position.copy()

    def portal(self):
        """
        Este método serve para teleportar o Ghost de um lado
        da malha para o outro.
        """
        if self.node.portal_node:
            # Prepara o Pac-Man para a mudança de posição
            self.node = self.node.portal_node
            self.set_position()

    tempDt = 0
    
    def update(self, dt):
        """
        Este é o método que precisa ser invocado pelo loop de jogo.
        Ele faz todos os update necessários no Ghost
        :param dt: Delta de tempo
        """
        # Mudança de posição usando a forma vetorial de S = v*t
        self.position += self.direction * self.speed * dt

        # Verificar a nova direção do Pac-Man
        self.tempDt += dt

        # Se houver nova direção --> iniciar novo movimento
        
        if self.direction:
            self.move_by_key(self.direction)

        # Ou continuar o último...
        else:
            self.move_by_self()

    def move_by_self(self):
        """
        Este método faz com que o Pac-Man continue seu último movimento
        """
        if (self.direction is not game_config.Movements.STOP) and self.overshot_target():
            self.node = self.target

            # Bati em um portal?
            self.portal()

            # Será que o Ghost bateu com o nariz na parede?
            if self.node.neighbors[self.direction] is not None:
                self.target = self.node.neighbors[self.direction]
            else:
                self.set_position()
                self.direction = utils.movement_translator.movement_ghosts(random.randint(0,3))

    def move_by_key(self, direction):
        """
        Este método inicia um novo movimento no Ghost
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
                        self.direction = utils.movement_translator.movement_ghosts(random.randint(0,3))

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

    def be_eaten(self):
        self.node = self.nodes.node_list[0]
        self.set_position()

    def eat_point_balls(self, point_list):
        """
        Este método faz com que o Pac-Man coma bolinhas
        :param point_list:
        """
        for ball in point_list:
            # Se de fato o Pac-Man colidiu com o ponto
            if (self.position - ball.position).magnitudeSquared() <= (ball.radius + self.collideRadius) ** 2:
                # Soma os pontos ao placar atual
                self.points += game_config.Points.point_balls


                return ball

        pygame.mixer.music.stop()
        return None

    def render(self, screen):
        """
        (Re)desenha o Pac-Man na tela com os dados atualizados.
        :param screen: Tela do PyGame
        """
        # Desenha um círculo na tela
        #pygame.draw.circle(screen, self.color, self.position.asInt(), self.radius)
        screen.blit(pygame.image.load(self.image), (self.position.x-10, self.position.y-10))
