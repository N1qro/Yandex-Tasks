import pygame
import sys
import os.path


class Crosshair(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'arrow.png'))
        self.rect = self.image.get_rect(topleft=(-200, -200))

    def update(self, pos) -> None:
        self.rect.topleft = pos


class Window:
    FPS = 30

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption('Курсор')
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.crosshair = pygame.sprite.Group(Crosshair())
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_focused():
                        self.crosshair.update(event.pos)
                    else:
                        self.crosshair.update((self.width, self.height))

            self.screen.fill(0)
            self.crosshair.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    window = Window(400, 400)
    window.run()
