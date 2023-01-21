import pygame
from sys import exit as sys_exit
from random import choice
from os.path import join as join_path


def find_free_place(game_map):
    free_space = list()
    for x, row in enumerate(game_map):
        for y, column in enumerate(row):
            if column == 0:
                free_space.append((x, y))

    return choice(free_space)


def is_move_valid(x, y, board):
    try:
        return board[x][y] == 0
    except IndexError:
        return False


class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size, *groups) -> None:
        super().__init__(*groups)
        self.x, self.y = x, y
        self.cell_size = cell_size

        unscaled_texture = pygame.image.load(
            join_path('assets', 'sprites', 'Mario.png')
        ).convert_alpha()

        w, h = unscaled_texture.get_size()
        self.image = pygame.transform.scale(
            unscaled_texture, (cell_size * w / 50, cell_size * h / 50)
        ).convert_alpha()

        self.rect = self.image.get_rect(
            center=(x * cell_size + cell_size / 2, y * cell_size + cell_size / 2)
        )

    def move(self, coords):
        deltaX = coords[0] - self.x
        deltaY = coords[1] - self.y
        self.x = coords[0]
        self.y = coords[1]

        self.rect.move_ip(deltaX * self.cell_size, deltaY * self.cell_size)


class Board:
    initialized = False
    tile_size = None

    @classmethod
    def init(cls, tile_size):
        assert not cls.initialized, 'board class is already initialized!'
        grass_texture = pygame.image.load(
            join_path('assets', 'sprites', 'Grass.png')
        ).convert()
        box_texture = pygame.image.load(
            join_path('assets', 'sprites', 'Box.png')
        ).convert()

        cls.grass_texture = pygame.transform.scale(
            grass_texture, (tile_size, tile_size)
        )
        cls.box_texture = pygame.transform.scale(
            box_texture, (tile_size, tile_size)
        )
        cls.cells = (cls.grass_texture, cls.box_texture)

        cls.tile_size = tile_size
        cls.initialized = True

    def __init__(self, width, height):
        assert self.initialized, 'board class is not initialized!'
        self.screen = pygame.display.get_surface()
        self.width = width // self.tile_size
        self.height = height // self.tile_size
        self.board = [[0] * (width // self.tile_size)
                      for _ in range(height // self.tile_size)]

    def load_layout(self, layout):
        self.board = layout

    def render(self):
        t_size = self.tile_size
        for x in range(self.width):
            for y in range(self.height):
                texture = self.cells[self.board[x][y]]
                self.screen.blit(
                    texture, (x * t_size, y * t_size, t_size, t_size)
                )


class Game:
    FPS = 60

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption('Перемещения героя')
        pygame.display.set_mode((width, height))

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.width, self.height = width, height
        self.board = None
        self.player = None

    def set_board(self, width, height):
        self.board = Board(width, height)

    def spawn_mario(self, x, y):
        assert self.board, 'Map haven\'t been created yet!'
        self.player = Mario(x, y, self.board.tile_size)

    def show_menu(self):
        menu_image = pygame.image.load(
            join_path('assets', 'images', 'Background-image.jpg')).convert()
        self.screen.blit(pygame.transform.scale(
            menu_image, (self.width, self.height)), (0, 0))

        font = pygame.font.SysFont(None, 22)
        text_surface = font.render(
            'Нажмите на любую кнопку чтобы влиться в этот экшоновый мир', True, 'White'
        )
        self.screen.blit(text_surface, (5, 10))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys_exit()
                elif event.type == pygame.KEYDOWN:
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return True

            pygame.display.update()
            self.clock.tick(10)

    def run(self):
        self.show_menu()
        self.screen.fill(0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys_exit()
                elif event.type == pygame.KEYDOWN:
                    coords = None
                    if event.key == pygame.K_w:
                        coords = self.player.x, self.player.y - 1
                    elif event.key == pygame.K_a:
                        coords = self.player.x - 1, self.player.y
                    elif event.key == pygame.K_s:
                        coords = self.player.x, self.player.y + 1
                    elif event.key == pygame.K_d:
                        coords = self.player.x + 1, self.player.y

                    if coords:
                        is_valid = is_move_valid(*coords, self.board.board)
                        if is_valid:
                            self.player.move(coords)

            self.board.render()
            if self.player:
                self.screen.blit(self.player.image, self.player.rect)
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    window_size = 500
    width = height = window_size

    game_map = list()
    with open('map.txt') as f:
        has_open_space = False
        for line in f.readlines():
            row = list()
            for letter in line.strip():
                letter = int(letter)
                assert letter in (
                    0, 1), f'Нераспозанный фрагмент карты "{letter}"! Допустимы (0, 1)'
                row.append(letter)
                if letter == 0:
                    has_open_space = True
            game_map.append(row)

    assert 16 > len(
        game_map) > 3, 'Карта должна быть минимум 4x4 и максимум 15x15!'
    assert has_open_space, 'Марио негде встать! Вся карта в коробках.'
    assert len(game_map) == len(
        game_map[0]), 'Карта должна иметь равно количество рядов и столбцов!'

    tile_size = window_size // len(game_map)
    window = Game(window_size, window_size)
    Board.init(tile_size)
    window.set_board(window_size, window_size)
    window.board.load_layout(game_map)
    window.spawn_mario(*find_free_place(game_map))
    window.run()
