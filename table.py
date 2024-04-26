import pygame
import random
from settings import *
from player import Paddle
from ball import Ball


# define table object
class Table:
    # initialize table object
    def __init__(self, win):
        self.win = win
        self.p1 = Paddle(100, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.p2 = Paddle(WIDTH - 100 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2)
        self.game_over = False
        self.win_con = 11
        self.winner = None
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.color = pygame.Color(COLOR)

    # draw net onto table object
    def draw_net(self):
        for i in range(0, HEIGHT, 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, self.color, (WIDTH // 2, i, 1, 10))

    # handle paddle movement
    def move_paddle(self):
        keys = pygame.key.get_pressed()

        # handle left paddle movement
        if keys[pygame.K_w]:
            if self.p1.rect.top >= 15:
                self.p1.move_up()
        if keys[pygame.K_s]:
            if self.p1.rect.bottom <= HEIGHT - 15:
                self.p1.move_down()

        # handle right paddle movement
        if keys[pygame.K_UP]:
            if self.p2.rect.top >= 15:
                self.p2.move_up()
        if keys[pygame.K_DOWN]:
            if self.p2.rect.bottom <= HEIGHT - 15:
                self.p2.move_down()

    # handle collision between ball and other objects
    def ball_collision(self):
        # collision with floor and ceiling
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.speed_y *= -1

        # collision with left and right side of window
        if self.ball.rect.right <= 0:
            self.p2.score += 1
            self.ball_reset()
        if self.ball.rect.left >= WIDTH:
            self.p1.score += 1
            self.ball_reset()

        # collision with left and right border when game over
        if self.ball.rect.left <= 0 and self.game_over:
            self.ball.speed_x *= -1
        if self.ball.rect.right >= WIDTH and self.game_over:
            self.ball.speed_x *= -1

        # collision with paddles
        if self.ball.rect.colliderect(self.p1) or self.ball.rect.colliderect(self.p2):
            self.ball.speed_x *= -1

    # reset ball to center if ball moves outside window
    def ball_reset(self):
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = random.randint(0 + BALL_HEIGHT, HEIGHT - BALL_HEIGHT)

    # show score for each player
    def display_score(self):
        left_score = self.font.render(f"{self.p1.score}", False, self.color)
        right_score = self.font.render(f"{self.p2.score}", False, self.color)
        self.win.blit(left_score, (WIDTH // 4 - 10, 0))
        self.win.blit(right_score, (WIDTH * 3 // 4 - 40, 0))

    # check for event where either player reaches win condition
    def check_win_con(self):
        if self.p1.score == self.win_con:
            self.winner = "P1 WIN!"
        elif self.p2.score == self.win_con:
            self.winner = "P2 WIN!"

    # handle event for player wins game
    def end_game(self):
        if self.winner is not None:
            self.game_over = True
            declare = self.font.render(self.winner, False, 'white')
            self.win.blit(declare, (WIDTH // 2 - declare.get_width() // 2, HEIGHT // 2 - declare.get_height() // 2))

    # draw objects from table onto window
    def draw(self):
        self.draw_net()

    def update(self):
        self.p1.update(self.win)
        self.p2.update(self.win)
        self.ball.update(self.win)

        self.move_paddle()
        self.ball_collision()

        self.display_score()
        self.check_win_con()
        self.end_game()
