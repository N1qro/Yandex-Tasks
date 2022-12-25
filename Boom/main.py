import pygame
import random
import sys
import os.path


class Bomb(pygame.sprite.Sprite):
    undetonated = pygame.image.load(os.path.join('data', 'bomb.png'))
    detonated = pygame.image.load(os.path.join('data', 'boom.png'))

    def __init__(self, x=0, y=0) -> None:
        super().__init__()
        self.image = self.undetonated.convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.isDetonated = False

    def detonate(self) -> None:
        if not self.isDetonated:
            self.isDetonated = True
            self.image = self.detonated.convert_alpha()
            self.rect = self.detonated.get_rect(center=self.rect.center)

    def update(self, pos) -> None:
        if self.rect.collidepoint(pos):
            self.detonate()


class Window:
    FPS = 30

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption('Boom')
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.bombs = self.spawnBombs(20)

    def spawnBombs(self, bombAmount):
        group = pygame.sprite.Group()
        bombSize = Bomb.undetonated.get_size()
        bombSpawnzone = self.screen.get_rect(
        ).inflate(-bombSize[0] // 2, -bombSize[1] // 2)

        while bombAmount > 0:
            x = random.randint(bombSpawnzone.left,
                               bombSpawnzone.left + bombSpawnzone.width)
            y = random.randint(bombSpawnzone.top,
                               bombSpawnzone.top + bombSpawnzone.height)
            bomb = Bomb(x, y)
            bombAmount -= 1
            group.add(bomb)

        return group

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.bombs.update(event.pos)

            self.screen.fill((255, 255, 255))
            self.bombs.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    window = Window(600, 600)
    window.run()
