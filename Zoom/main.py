import sys
import pygame


class Game:
    FPS = 30

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption('Zoom')

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offsetVector = pygame.math.Vector2(width // 2, height // 2)
        self.needs_repaint = True

        self.origin = list()
        self.scaled = list()
        self.zoom_multiplier = 15

    def load_figure(self, filename):
        with open(filename) as f:
            for pos in f.read().strip().split(', '):
                x, y = map(float, pos[1:-1].replace(',', '.').split(';'))
                new_vector = pygame.math.Vector2(x, -y)
                self.origin.append(new_vector)
                self.scaled.append(new_vector * self.zoom_multiplier)

    def draw_figure(self):
        if self.needs_repaint:
            self.screen.fill(0)
            points = [vector + self.offsetVector for vector in self.scaled]
            pygame.draw.polygon(self.screen, 'White', points, width=2)
            self.needs_repaint = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEWHEEL:
                    self.zoom_multiplier = max(self.zoom_multiplier + event.y * self.zoom_multiplier / 15, 0)
                    self.scaled = [point * self.zoom_multiplier for point in self.origin]
                    self.needs_repaint = True

            self.draw_figure()
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game(501, 501)
    game.load_figure('figure.txt')
    game.run()
