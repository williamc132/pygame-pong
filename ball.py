import pygame
from settings import *


# define ball object
class Ball:
    # initialize ball object
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, BALL_WIDTH, BALL_HEIGHT)
        self.color = pygame.Color(COLOR)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED

    # handle ball movement
    def movement(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    # update ball object
    def update(self, win):
        self.movement()
        pygame.draw.rect(win, self.color, self.rect)
