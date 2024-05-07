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
        self.score_limit = 11
        self.winner = None
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.color = pygame.Color(COLOR)
        self.score_time = pygame.time.get_ticks() - 2000
        self.RESET_BALL = pygame.USEREVENT + 1

    # draw net onto table object
    def _draw_net(self):
        for i in range(0, HEIGHT, 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, self.color, (WIDTH // 2, i, 1, 10))

    # handle paddle movement
    def _move_paddle(self):
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
    def _ball_collision(self):
        # collision with top and bottom of window
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.speed_y *= -1

        # collision with left and right side of window
        if self.ball.rect.right <= 0 and pygame.time.get_ticks() - self.score_time > RESET_DELAY:
            self.p2.score += 1
            self.score_time = pygame.time.get_ticks()
            self.ball.rect.centerx = WIDTH // 2
            self.ball.moving = False
            self._check_score()
        if self.ball.rect.left >= WIDTH and pygame.time.get_ticks() - self.score_time > RESET_DELAY:
            self.p1.score += 1
            self.score_time = pygame.time.get_ticks()
            self.ball.rect.centerx = WIDTH // 2
            self.ball.moving = False
            self._check_score()

        # collision with left and right side of window when game over
        if self.ball.rect.left <= 0 and self.game_over:
            self.ball.speed_x *= -1
        if self.ball.rect.right >= WIDTH and self.game_over:
            self.ball.speed_x *= -1

        # collision with paddles
        if self.ball.rect.colliderect(self.p1) or self.ball.rect.colliderect(self.p2):
            self.ball.speed_x *= -1

    # reposition ball to center
    def center_ball(self):
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = random.randint(0 + BALL_HEIGHT, HEIGHT - BALL_HEIGHT)
        self.ball.speed_x *= random.choice([-1, 1])
        self.ball.speed_y *= random.choice([-1, 1])
        self.ball.moving = True

    def _check_score(self):
        if self.p1.score < self.score_limit and self.p2.score < self.score_limit:
            pygame.time.set_timer(self.RESET_BALL, RESET_DELAY, 1)
        else:
            self.center_ball()

    # show score for each player
    def _display_score(self):
        left_score = self.font.render(f"{self.p1.score}", False, self.color)
        right_score = self.font.render(f"{self.p2.score}", False, self.color)
        self.win.blit(left_score, (WIDTH // 4 - 10, 0))
        self.win.blit(right_score, (WIDTH * 3 // 4 - 40, 0))

    # check for event where either player wins
    def _check_game_over(self):
        # check if either player reaches score limit
        if self.p1.score == self.score_limit:
            self.winner = "P1"
        elif self.p2.score == self.score_limit:
            self.winner = "P2"

        # handle event for player win
        if self.winner is not None:
            self.game_over = True
            declare = self.font.render(f"{self.winner} WIN!", False, 'white')
            # TODO: adjust font to avoid overlapping net
            self.win.blit(declare, (WIDTH//2 - declare.get_width()//2, HEIGHT//2 - declare.get_height()//2))

    # draw objects from table onto window
    def draw(self):
        self._draw_net()

    def update(self):
        self.p1.update(self.win)
        self.p2.update(self.win)
        self.ball.update(self.win)

        self._move_paddle()
        self._ball_collision()

        self._display_score()
        self._check_game_over()
