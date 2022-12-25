import pygame
import sys
import os.path


class Creature(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'creature.png'))
        self.rect = self.image.get_rect()

    def update(self, move) -> None:
        self.rect.move_ip(*map(lambda x: x * 10, move))


class Window:
    FPS = 30

    keys = {
        pygame.K_RIGHT: (1, 0),
        pygame.K_LEFT: (-1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_w: (0, -1),
        pygame.K_a: (-1, 0),
        pygame.K_s: (0, 1),
        pygame.K_d: (1, 0)
    }

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption('Пипец')
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.movingObjects = pygame.sprite.Group(Creature())
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.keys:
                        self.movingObjects.update(self.keys[event.key])

            self.screen.fill((255, 255, 255))
            self.movingObjects.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    window = Window(400, 400)
    window.run()
