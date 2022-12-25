import pygame
import sys
import os.path


class Car(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join('data', 'car2.png'))
        self.rect = self.image.get_rect()
        self.speedX = 10

    def rotate(self) -> None:
        self.speedX *= -1
        self.image = pygame.transform.flip(self.image, True, True)

    def update(self) -> None:
        self.rect.move_ip(self.speedX, 0)


class Window:
    FPS = 30

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption('Mochina')
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.car = Car()
        self.movingObjects = pygame.sprite.Group(self.car)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            
            self.screen.fill((255, 255, 255))
            self.movingObjects.update()

            if self.car.rect.left < 0 or self.car.rect.right > self.width:
                self.car.rotate()

            self.movingObjects.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    window = Window(600, 95)
    window.run()
