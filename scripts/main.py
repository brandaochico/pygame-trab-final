""" main.py """

from settings import *

class Game():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.Clock()
        self.running = True

    def run(self):
        while self.running:
            # Delta Time
            dt = self.clock.tick() / 1000

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill('darkgray')
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()