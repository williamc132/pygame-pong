import pygame
import random
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
        self.max_speed = BALL_MAX_SPEED
        self.direction = None
        self._randomize_direction()
        self.moving = True

    # randomize ball direction
    def _randomize_direction(self):
        direction = ("left", "right")
        self.direction = random.choice(direction)

        if self.direction == "left":
            self.speed_x = BALL_SPEED * -1
        else:
            self.speed_x = BALL_SPEED

    # handle ball movement
    def _movement(self):
        if self.moving:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    # update ball object
    def update(self, win):
        if self.moving:
            self._movement()
            pygame.draw.rect(win, self.color, self.rect)
