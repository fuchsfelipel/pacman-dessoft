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
        self.portalNode = None
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
        self.nodeList = []
        self.level = level
        self.grid = None
        self.nodeStack = Stack()
        self.portalSymbols = ["1"]
        self.nodeSymbols = ["+"] + self.portalSymbols
        self.create_node_list(level, self.nodeList)
        self.setup_portal_nodes()

    @staticmethod
    def read_maze_file(textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    def create_node_list(self, textFile, nodeList):
        self.grid = self.read_maze_file(textFile)
        startNode = self.find_first_node(len(self.grid), len(self.grid[0]))
        self.nodeStack.push(startNode)
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.add_node(node, nodeList)
            leftNode = self.get_path_node(game_config.Movements.LEFT, node.row, node.column - 1, nodeList)
            rightNode = self.get_path_node(game_config.Movements.RIGHT, node.row, node.column + 1, nodeList)
            upNode = self.get_path_node(game_config.Movements.UP, node.row - 1, node.column, nodeList)
            downNode = self.get_path_node(game_config.Movements.DOWN, node.row + 1, node.column, nodeList)
            node.neighbors[game_config.Movements.LEFT] = leftNode
            node.neighbors[game_config.Movements.RIGHT] = rightNode
            node.neighbors[game_config.Movements.UP] = upNode
            node.neighbors[game_config.Movements.DOWN] = downNode
            self.add_node_to_stack(leftNode, nodeList)
            self.add_node_to_stack(rightNode, nodeList)
            self.add_node_to_stack(upNode, nodeList)
            self.add_node_to_stack(downNode, nodeList)

    def find_first_node(self, rows, cols):
        nodeFound = False
        for row in range(rows):
            for col in range(cols):
                if self.grid[row][col] in self.nodeSymbols:
                    node = Node(row, col)
                    if self.grid[row][col] in self.portalSymbols:
                        node.portalVal = self.grid[row][col]
                    return node
        return None

    @staticmethod
    def get_node(x, y, nodeList=[]):
        for node in nodeList:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    @staticmethod
    def get_node_from_node(node, nodeList):
        if node is not None:
            for inode in nodeList:
                if node.row == inode.row and node.column == inode.column:
                    return inode
        return node

    def get_path_node(self, direction, row, col, nodeList):
        tempNode = self.follow_path(direction, row, col)
        return self.get_node_from_node(tempNode, nodeList)

    def add_node(self, node, nodeList):
        nodeInList = self.node_in_list(node, nodeList)
        if not nodeInList:
            nodeList.append(node)

    def add_node_to_stack(self, node, nodeList):
        if node is not None and not self.node_in_list(node, nodeList):
            self.nodeStack.push(node)

    @staticmethod
    def node_in_list(node, nodeList):
        for inode in nodeList:
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
        tempSymbols = [path] + self.nodeSymbols
        if self.grid[row][col] in tempSymbols:
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
        portalDict = {}
        for i in range(len(self.nodeList)):
            if self.nodeList[i].portalVal != 0:
                if self.nodeList[i].portalVal not in portalDict.keys():
                    portalDict[self.nodeList[i].portalVal] = [i]
                else:
                    portalDict[self.nodeList[i].portalVal] += [i]
        for key in portalDict.keys():
            node1, node2 = portalDict[key]
            self.nodeList[node1].portalNode = self.nodeList[node2]
            self.nodeList[node2].portalNode = self.nodeList[node1]

    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)
