import pygame
from settings import *


# define paddle object as player
class Paddle:
    # initialize paddle
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = pygame.Color(COLOR)
        self.v = PADDLE_SPEED
        self.score = 0

    # function for upward movement
    def move_up(self):
        self.rect.y -= self.v

    # function for downward movement
    def move_down(self):
        self.rect.y += self.v

    # update paddle object
    def update(self, win):
        pygame.draw.rect(win, self.color, self.rect)
