import sys
import os.path
import pygame

from sprites import Camera, Mario, Board
from pathfinding import is_move_valid, find_free_place


class Game:
    FPS = 60

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption("Marijo")
        pygame.display.set_mode((width, height))

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.layout = None
        self.camera = None
        self.player = None

        pygame.display.update()

    def show_menu(self):
        menu_image = pygame.image.load(
            os.path.join('assets', 'images', 'Background-image.jpg')).convert()
        self.screen.blit(pygame.transform.scale(
            menu_image, (500, 500)), (0, 0))

        font = pygame.font.SysFont(None, 22)
        text_surface = font.render(
            'Нажмите на любую кнопку чтобы влиться в этот экшоновый мир', True, 'White'
        )
        self.screen.blit(text_surface, (5, 10))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return True

            pygame.display.update()
            self.clock.tick(10)

    def run(self):
        self.show_menu()
        self.camera.center_target_camera(self.player)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
                        is_valid = is_move_valid(*coords, self.layout)
                        if is_valid:
                            self.player.move(coords)
                            self.camera.center_target_camera(self.player)

                self.clock.tick(self.FPS)
                self.screen.fill(0)
                camera.draw()
                pygame.display.update()


if __name__ == "__main__":
    filename = input('Введите имя файла: ')
    try:
        assert filename.endswith('.txt'), 'Передан не текстовый файл'
        assert os.path.isfile(filename), 'Такого файла не существует'
    except AssertionError as e:
        print(str(e))
        sys.exit(0)

    game = Game(500, 500)
    board = Board()
    layout = board.load_layout(filename)
    game_map = board.generate_surface(layout)

    player = Mario(*find_free_place(layout))
    camera = Camera(game_map, player)

    game.camera = camera
    game.player = player
    game.layout = layout
    game.run()
