import pygame
import random
import sys
import os.path


class GameoverScreen(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'gameover.png')).convert()
        self.rect = self.image.get_rect(topright=(-1, 0))
        self.moveSpeed = 900
        self.isVisible = False

    def update(self, dt) -> None:
        if not self.isVisible:
            self.rect.x += self.moveSpeed * dt / 1000
            if self.rect.right > 600:
                self.rect.right = 600
                self.isVisible = True
        

class Window:
    FPS = 120

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption('Boom')
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.gameover = pygame.sprite.Group(GameoverScreen())

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            dt = self.clock.tick(self.FPS)
            self.screen.fill((0, 0, 200))
            self.gameover.update(dt)
            self.gameover.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    window = Window(600, 300)
    window.run()
