"""
Este método consiste em uma ferramenta para traduzir
um keypress no teclado em um vetor de movimentação para
qualquer sprite.
"""

import game_config


def movement_translator(key, key_up, key_down, key_right, key_left):
    """
    Este método serve para traduzir os movimentos do Pac-Man
    :param key
    @param key: A tecla apertada
    @param key_up: A tecla para o sprite subir
    @param key_down: A tecla para o sprite ir para baixo
    @param key_right: A tecla para o sprite ir para a direita
    @param key_left: A tecla para o sprite ir para a esqueda
    @return: O retorna o vetor 2D de movimentação
    """
    if key[key_up]:
        return game_config.Movements.UP
    elif key[key_down]:
        return game_config.Movements.DOWN
    elif key[key_left]:
        return game_config.Movements.LEFT
    elif key[key_right]:
        return game_config.Movements.RIGHT
    return None

def movement_ghosts(key):
    """
    Este método serve para traduzir os movimentos dos fantasmas
    :param key
    @param key: A tecla apertada
    @param key_up: A tecla para o sprite subir
    @param key_down: A tecla para o sprite ir para baixo
    @param key_right: A tecla para o sprite ir para a direita
    @param key_left: A tecla para o sprite ir para a esqueda
    @return: O retorna o vetor 2D de movimentação
    """
    if key == 0:
        return game_config.Movements.UP
    elif key == 1:
        return game_config.Movements.DOWN
    elif key == 2:
        return game_config.Movements.LEFT
    elif key == 3:
        return game_config.Movements.RIGHT
    return None