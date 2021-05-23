from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
import game_config


def movement_translator(key):
    if key[K_UP]:
        return game_config.Movements.UP
    elif key[K_DOWN]:
        return game_config.Movements.DOWN
    elif key[K_LEFT]:
        return game_config.Movements.LEFT
    elif key[K_RIGHT]:
        return game_config.Movements.RIGHT
    return None
