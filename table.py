import pygame
import random
import math
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
        self.score_font = pygame.font.Font(SCORE_FONT, FONT_SIZE)
        self.text_font = pygame.font.Font(TEXT_FONT, FONT_SIZE)
        self.color = pygame.Color(COLOR)
        self.score_time = pygame.time.get_ticks() - 2000
        self.RESET_BALL = pygame.USEREVENT + 1
        self.paddle_collision_count = 0

    # draw net onto table object
    def _draw_net(self):
        for i in range(0, HEIGHT, 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, self.color, (WIDTH // 2, i, 1, 10))

    # handle paddle movement
    def _move_paddle(self):
        # get state of all keyboard buttons
        keys = pygame.key.get_pressed()

        # handle left paddle movement
        if keys[pygame.K_w]:
            if self.p1.rect.top >= PADDLE_LIMIT:
                self.p1.move_up()
        if keys[pygame.K_s]:
            if self.p1.rect.bottom <= HEIGHT - PADDLE_LIMIT:
                self.p1.move_down()

        # handle right paddle movement
        if keys[pygame.K_UP]:
            if self.p2.rect.top >= PADDLE_LIMIT:
                self.p2.move_up()
        if keys[pygame.K_DOWN]:
            if self.p2.rect.bottom <= HEIGHT - PADDLE_LIMIT:
                self.p2.move_down()

    # handle collision between ball and walls
    def _wall_collision(self):
        # collision with top and bottom of window
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.speed_y *= -1

        # collision with left and right side of window while game over
        if self.game_over:
            if self.ball.rect.left <= 0 or self.ball.rect.right >= WIDTH:
                self.ball.speed_x *= -1

        # collision with left and right side of window
        if self.ball.rect.right <= 0 and pygame.time.get_ticks() - self.score_time > RESET_DELAY:
            self.p2.score += 1
            self.score_time = pygame.time.get_ticks()
            self._hide_ball()
            self._reset_ball_speed()
            self._check_score()
        if self.ball.rect.left >= WIDTH and pygame.time.get_ticks() - self.score_time > RESET_DELAY:
            self.p1.score += 1
            self.score_time = pygame.time.get_ticks()
            self._hide_ball()
            self._reset_ball_speed()
            self._check_score()

    # collision between ball and paddles
    def _paddle_collision(self):
        self._handle_paddle_collision(self.ball, self.p1, self.ball.speed_x)
        self._handle_paddle_collision(self.ball, self.p2, self.ball.speed_x)

    # handle collision between ball and paddles
    def _handle_paddle_collision(self, ball, paddle, ball_direction):
        if self.ball.rect.colliderect(paddle):
            # collision with right paddle
            if abs(ball.rect.right - paddle.rect.left) < COLLISION_TOLERANCE and ball_direction > 0:
                if abs(ball.rect.centery - paddle.rect.centery) < 1 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(180))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(180))

                elif 0 < ball.rect.centery - paddle.rect.centery <= 5 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(160))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(160))

                elif 5 < ball.rect.centery - paddle.rect.centery <= 10 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(140))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(140))

                elif 10 < ball.rect.centery - paddle.rect.centery <= 15 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(120))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(120))

                elif 0 > ball.rect.centery - paddle.rect.centery >= -5 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(200))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(200))

                elif -5 > ball.rect.centery - paddle.rect.centery >= -10 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(220))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(220))

                elif -10 > ball.rect.centery - paddle.rect.centery >= -15 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(240))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(240))

                else:
                    if not self.game_over:
                        self._check_ball_speed()
                    ball.speed_x *= -1

            # collision with left paddle
            elif abs(ball.rect.left - paddle.rect.right) < COLLISION_TOLERANCE and ball_direction < 0:
                if abs(ball.rect.centery - paddle.rect.centery) < 1 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(0))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(0))

                elif 0 < ball.rect.centery - paddle.rect.centery <= 5 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(20))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(20))

                elif 5 < ball.rect.centery - paddle.rect.centery <= 10 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(40))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(40))

                elif 10 < ball.rect.centery - paddle.rect.centery <= 15 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(60))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(60))

                elif 0 > ball.rect.centery - paddle.rect.centery >= -5 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(340))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(340))

                elif -5 > ball.rect.centery - paddle.rect.centery >= -10 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(320))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(320))

                elif -10 > ball.rect.centery - paddle.rect.centery >= -15 and not self.game_over:
                    self._check_ball_speed()
                    ball.speed_x = self.ball.new_speed * math.cos(math.radians(300))
                    ball.speed_y = self.ball.new_speed * math.sin(math.radians(300))

                else:
                    if not self.game_over:
                        self._check_ball_speed()
                    ball.speed_x *= -1

            # collision between top of paddle and bottom of ball
            elif abs(ball.rect.bottom - paddle.rect.top) < COLLISION_TOLERANCE and self.ball.speed_y > 0:
                ball.speed_y *= -1
                ball.rect.bottom = paddle.rect.top

            # collision between top of ball and bottom of paddle
            elif abs(ball.rect.top - paddle.rect.bottom) < COLLISION_TOLERANCE and self.ball.speed_y < 0:
                ball.speed_y *= -1
                ball.rect.top = paddle.rect.bottom

    def _check_ball_speed(self):
        # increment count upon collision with either paddle
        self.paddle_collision_count += 1

        # increase speed after collision with both paddles
        if self.paddle_collision_count % 2 == 0:
            self.ball.increase_speed()
            self.paddle_collision_count = 0

    # reposition ball to center after scoring
    def center_ball(self):
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = random.randint(BALL_HEIGHT + PADDLE_LIMIT, HEIGHT - BALL_HEIGHT - PADDLE_LIMIT)

        if self.p1.score < self.score_limit and self.p2.score < self.score_limit:
            self.ball.randomize_direction()
        else:
            self._reset_ball_movement()

        self.ball.moving = True

    # hide ball animation after point is scored
    def _hide_ball(self):
        self.ball.rect.centerx = WIDTH // 2
        self.ball.rect.centery = HEIGHT // 2
        self.ball.moving = False

    def _reset_ball_speed(self):
        self.paddle_collision_count = 0
        self.ball.new_speed = BALL_SPEED

    # ball movement when game over
    def _reset_ball_movement(self):
        self.ball.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.ball.speed_y = BALL_SPEED * random.choice([-1, 1])

    # add delay to ball reset after each score
    def _check_score(self):
        if self.p1.score < self.score_limit and self.p2.score < self.score_limit:
            pygame.time.set_timer(self.RESET_BALL, RESET_DELAY, 1)
        else:
            self.center_ball()

    # show score for each player
    def _display_score(self):
        left_score = self.score_font.render(f"{self.p1.score}", False, self.color)
        right_score = self.score_font.render(f"{self.p2.score}", False, self.color)
        if self.p1.score < 10:
            self.win.blit(left_score, (WIDTH // 4 + 20, 0))
        else:
            self.win.blit(left_score, (WIDTH // 4, 0))
        if self.p2.score < 10:
            self.win.blit(right_score, (WIDTH * 3 // 4 - 5, 0))
        else:
            self.win.blit(right_score, (WIDTH * 3 // 4 - 55, 0))

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
            declare = self.text_font.render(f"{self.winner} WIN", False, 'white')
            self.win.blit(declare, (WIDTH//2 - declare.get_width()//2 + 30, HEIGHT//2 - declare.get_height()//2))

    # draw objects from table onto window
    def draw(self):
        self._draw_net()

    # update objects on table
    def update(self):
        self.p1.update(self.win)
        self.p2.update(self.win)
        self.ball.update(self.win)

        self._move_paddle()

        self._wall_collision()
        self._paddle_collision()

        self._display_score()
        self._check_game_over()
