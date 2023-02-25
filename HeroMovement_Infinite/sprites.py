import pygame
import os.path


class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x, self.y = x, y
        self.cell_size = 50

        unscaled_texture = pygame.image.load(
            os.path.join('assets', 'sprites', 'Mario.png')
        ).convert_alpha()

        w, h = unscaled_texture.get_size()
        self.image = pygame.transform.scale(
            unscaled_texture, (50 * w / 50, 50 * h / 50)
        ).convert_alpha()

        self.rect = self.image.get_rect(
            center=(x * 50 + 50 / 2, y * 50 + 50 / 2)
        )

    def move(self, coords):
        deltaX = coords[0] - self.x
        deltaY = coords[1] - self.y
        self.x = coords[0]
        self.y = coords[1]

        self.rect.move_ip(deltaX * self.cell_size, deltaY * self.cell_size)


class Camera(pygame.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)
        self.surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.surface.get_width() // 2
        self.half_h = self.surface.get_height() // 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def draw(self):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_pos)


class Board:
    def __init__(self):
        self.grass = pygame.image.load(
            os.path.join("assets", "sprites", "Grass.png")
        ).convert()

        self.box = pygame.image.load(
            os.path.join("assets", "sprites", "Box.png")
        ).convert()

    def generate_surface(self, layout):
        field = pygame.Surface((500, 500))
        for x, row in enumerate(layout):
            for y, column in enumerate(row):
                texture = self.box if column == 1 else self.grass
                field.blit(texture, (50 * x, 50 * y, 50, 50))

        field_sprite = pygame.sprite.Sprite()
        field_sprite.image = field
        field_sprite.rect = pygame.Rect(0, 0, *field.get_size())

        return field_sprite

    def load_layout(self, filename):
        game_map = list()
        with open(filename) as f:
            has_open_space = False
            for line in f.readlines():
                row = list()
                for letter in line.strip():
                    letter = int(letter)
                    assert letter in (0, 1), \
                        f'Нераспозанный фрагмент карты "{letter}"! Допустимы (0, 1)'
                    row.append(letter)
                    if letter == 0:
                        has_open_space = True
                game_map.append(row)

        assert len(game_map) == len(game_map[0]) == 10, \
            "Карта должна иметь равно количество рядов и столбцов!"
        assert has_open_space, \
            "Марио негде встать! Вся карта в коробках."
        return game_map

