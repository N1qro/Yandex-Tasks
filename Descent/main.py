import sys
import pygame


class Drop(pygame.sprite.Sprite):
    y_speed = 150
    collision_mountain = None

    @classmethod
    def set_collision_object(cls, sprite):
        cls.collision_mountain = sprite

    def __init__(self, x, y, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("pt.png").convert_alpha()
        self.rect = self.image.get_rect(bottom=y, centerx=x)
        self.mask = pygame.mask.from_surface(self.image)
        self.is_descending = True

    def update(self, dt) -> None:
        if self.is_descending:
            self.rect.centery += self.y_speed * dt / 1000
            if pygame.sprite.collide_mask(self, self.collision_mountain):
                self.is_descending = False


class Mountain(pygame.sprite.Sprite):
    def __init__(self, screen_height) -> None:
        super().__init__()
        self.image = pygame.image.load("mountains.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(0, screen_height))
        self.mask = pygame.mask.from_surface(self.image)


class Game:
    FPS = 90

    def __init__(self, width, height) -> None:
        pygame.init()
        pygame.display.set_caption("Десант")
        pygame.display.set_mode((width, height))

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.drop_group = pygame.sprite.Group()
        self.background = pygame.transform.scale(
            pygame.image.load("bg.png"), (width, height)).convert()
        self.bg_rect = pygame.Rect(0, 0, width, height)

        self.mountains = Mountain(height)
        Drop.set_collision_object(self.mountains)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        # Проверка что нажатие было не на гору
                        if not (self.mountains.rect.collidepoint(event.pos)
                                and self.mountains.mask.get_at(
                                (event.pos[0] - self.mountains.rect.x,
                                 event.pos[1] - self.mountains.rect.y))):

                            Drop(*event.pos, self.drop_group)

            dt = self.clock.tick(self.FPS)
            self.screen.fill(0)
            self.screen.blit(self.background, self.bg_rect)
            self.screen.blit(self.mountains.image, self.mountains.rect)
            self.drop_group.update(dt)
            self.drop_group.draw(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    window = Game(789, 500)
    window.run()
