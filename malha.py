import pygame

import game_config
from game_config import *
from utils.stack import Stack


class Node(object):
    """
    Esta classe define o tabuleiro de jogo.
    Ela foi adaptada tutorial pacmancode.com;
    As principais mudanças são:
    - Adaptação para seguir as convenções do projeto
    - Transformação de métodos desnecessários em funções
    - Otimizações ou simplificações pontuais
    """
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2(column * game_config.GameDimensions.tile_w, row * game_config.GameDimensions.tile_h)
        self.neighbors = {game_config.Movements.UP: None,
                          game_config.Movements.DOWN: None,
                          game_config.Movements.LEFT: None,
                          game_config.Movements.RIGHT: None}
        self.portal_node = None
        self.portalVal = 0

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, game_config.Colors.tumbleweed, line_start, line_end, 4)
                pygame.draw.circle(screen, game_config.Colors.red, self.position.asInt(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.node_list = []
        self.level = level
        self.grid = None
        self.nodeStack = Stack()
        self.portalSymbols = ["1"]
        self.nodeSymbols = ["+"] + self.portalSymbols
        self.create_node_list(level, self.node_list)
        self.setup_portal_nodes()

    @staticmethod
    def read_maze_file(maze_file):
        f = open(maze_file, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    def create_node_list(self, text_file, node_list):
        self.grid = self.read_maze_file(text_file)
        start_node = self.find_first_node(len(self.grid), len(self.grid[0]))
        self.nodeStack.push(start_node)
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.add_node(node, node_list)
            left_node = self.get_path_node(game_config.Movements.LEFT, node.row, node.column - 1, node_list)
            right_node = self.get_path_node(game_config.Movements.RIGHT, node.row, node.column + 1, node_list)
            up_node = self.get_path_node(game_config.Movements.UP, node.row - 1, node.column, node_list)
            down_node = self.get_path_node(game_config.Movements.DOWN, node.row + 1, node.column, node_list)
            node.neighbors[game_config.Movements.LEFT] = left_node
            node.neighbors[game_config.Movements.RIGHT] = right_node
            node.neighbors[game_config.Movements.UP] = up_node
            node.neighbors[game_config.Movements.DOWN] = down_node
            self.add_node_to_stack(left_node, node_list)
            self.add_node_to_stack(right_node, node_list)
            self.add_node_to_stack(up_node, node_list)
            self.add_node_to_stack(down_node, node_list)

    def find_first_node(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                if self.grid[row][col] in self.nodeSymbols:
                    node = Node(row, col)
                    if self.grid[row][col] in self.portalSymbols:
                        node.portalVal = self.grid[row][col]
                    return node
        return None

    @staticmethod
    def get_node(x, y, node_list=[]):
        for node in node_list:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    @staticmethod
    def get_node_from_node(node, node_list):
        if node is not None:
            for inode in node_list:
                if node.row == inode.row and node.column == inode.column:
                    return inode
        return node

    def get_path_node(self, direction, row, col, node_list):
        temp_node = self.follow_path(direction, row, col)
        return self.get_node_from_node(temp_node, node_list)

    def add_node(self, node, node_list):
        node_in_list = self.node_in_list(node, node_list)
        if not node_in_list:
            node_list.append(node)

    def add_node_to_stack(self, node, node_list):
        if node is not None and not self.node_in_list(node, node_list):
            self.nodeStack.push(node)

    @staticmethod
    def node_in_list(node, node_list):
        for inode in node_list:
            if node.position.x == inode.position.x and node.position.y == inode.position.y:
                return True
        return False

    def follow_path(self, direction, row, col):
        rows = len(self.grid)
        columns = len(self.grid[0])
        if direction == game_config.Movements.LEFT and col >= 0:
            return self.path_to_follow(game_config.Movements.LEFT, row, col, "-")
        elif direction == game_config.Movements.RIGHT and col < columns:
            return self.path_to_follow(game_config.Movements.RIGHT, row, col, "-")
        elif direction == game_config.Movements.UP and row >= 0:
            return self.path_to_follow(game_config.Movements.UP, row, col, "|")
        elif direction == game_config.Movements.DOWN and row < rows:
            return self.path_to_follow(game_config.Movements.DOWN, row, col, "|")
        else:
            return None

    def path_to_follow(self, direction, row, col, path):
        temp_symbols = [path] + self.nodeSymbols
        if self.grid[row][col] in temp_symbols:
            while self.grid[row][col] not in self.nodeSymbols:
                if direction is game_config.Movements.LEFT:
                    col -= 1
                elif direction is game_config.Movements.RIGHT:
                    col += 1
                elif direction is game_config.Movements.UP:
                    row -= 1
                elif direction is game_config.Movements.DOWN:
                    row += 1
            node = Node(row, col)
            if self.grid[row][col] in self.portalSymbols:
                node.portalVal = self.grid[row][col]
            return node
        else:
            return None

    def setup_portal_nodes(self):
        portal_dict = {}
        for i in range(len(self.node_list)):
            if self.node_list[i].portalVal != 0:
                if self.node_list[i].portalVal not in portal_dict.keys():
                    portal_dict[self.node_list[i].portalVal] = [i]
                else:
                    portal_dict[self.node_list[i].portalVal] += [i]
        for key in portal_dict.keys():
            node1, node2 = portal_dict[key]
            self.node_list[node1].portal_node = self.node_list[node2]
            self.node_list[node2].portal_node = self.node_list[node1]

    def render(self, screen):
        for node in self.node_list:
            node.render(screen)
