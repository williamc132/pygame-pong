import pygame
import random
import math
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
        self.new_speed = BALL_SPEED
        self.angle = None
        self.randomize_direction()
        self.moving = True

    # randomize ball direction
    def randomize_direction(self):
        # range of angles
        angle_ranges = [(15, 60), (120, 165), (195, 240), (300, 315)]
        range_choice = random.choice(angle_ranges)
        self.angle = random.randint(*range_choice)

        # convert angle to radians
        angle_rad = math.radians(self.angle)

        # calculate ball speed along x and y
        self.speed_x = BALL_SPEED * math.cos(angle_rad)
        self.speed_y = BALL_SPEED * math.sin(angle_rad)

    # increase ball speed after collision with both paddles
    def increase_speed(self):
        if self.new_speed < self.max_speed:
            self.new_speed += 1

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
