import game_config


def movement_translator(key, key_up, key_down, key_right, key_left):
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
    if key == 0:
        return game_config.Movements.UP
    elif key == 1:
        return game_config.Movements.DOWN
    elif key == 2:
        return game_config.Movements.LEFT
    elif key == 3:
        return game_config.Movements.RIGHT
    return None