import random


def find_free_place(game_map):
    free_space = list()
    for x, row in enumerate(game_map):
        for y, column in enumerate(row):
            if column == 0:
                free_space.append((x, y))

    return random.choice(free_space)


def transform_move(x, y, layout):

    if x == -1:
        x = 9
    elif x == 10:
        x = 0

    if y == -1:
        y = 9
    elif y == 10:
        y = 0

    try:
        if layout[x][y] == 0:
            return x, y
    except IndexError:
        return False
