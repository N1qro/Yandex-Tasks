import random


def find_free_place(game_map):
    free_space = list()
    for x, row in enumerate(game_map):
        for y, column in enumerate(row):
            if column == 0:
                free_space.append((x, y))

    return random.choice(free_space)


def is_move_valid(x, y, layout):
    if 0 <= x <= 9 and 0 <= y <= 9:
        try:
            return layout[x][y] == 0
        except IndexError:
            return False
    return False
