import pygame
import sys
from settings import *
from table import Table


# define game object
class Game:
    # initialize window
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.table = Table(self.win)

    # update window
    def update(self):
        self.table.update()
        pygame.display.flip()
        self.clock.tick(FPS)

    # draw window
    def draw(self):
        self.win.fill('black')
        self.table.draw()

    # main loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.table.RESET_BALL:
                    self.table.ball_reset()
            self.draw()
            self.update()


# call main function
if __name__ == '__main__':
    game = Game()
    game.run()
