import sys
import pygame


class Window:
    def __init__(self, width, height) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Шахматная доска')

    def drawEverything(self, sqPerScreen):
        width = self.screen.get_width() // sqPerScreen
        height = self.screen.get_height() // sqPerScreen

        colorBlack = True
        for x in range(sqPerScreen):
            for y in range(sqPerScreen):
                rect = pygame.rect.Rect(width * x, height * y, width, height)
                color = pygame.Color(
                    'black') if colorBlack else pygame.Color('white')
                pygame.draw.rect(self.screen, color, rect)
                colorBlack = not colorBlack
            if sqPerScreen % 2 == 0:
                colorBlack = not colorBlack

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    width, _ = height, squareCount = tuple(map(int, input().split()))
    win = Window(width, height)
    win.drawEverything(squareCount)
    win.run()
