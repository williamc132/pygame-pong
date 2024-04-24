import pygame
import sys
import random
from settings import *

# initialize pygame
pygame.init()

# initialize window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# set font
font = pygame.font.Font(FONT_NAME, FONT_SIZE)


# main function
def main():
    # create paddles and ball
    p1 = pygame.Rect(100, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    p2 = pygame.Rect(WIDTH - 100 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_WIDTH//2, HEIGHT//2 - BALL_HEIGHT//2, BALL_WIDTH, BALL_HEIGHT)

    # initialize player movement as paddles
    left_paddle_v = 0
    right_paddle_v = 0

    # initialize ball speed
    ball_speed_x = BALL_SPEED
    ball_speed_y = BALL_SPEED

    # implement score system
    p1_score = 0
    p2_score = 0

    # implement win condition
    game_over = False
    winner = None

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # connect keys pressed to paddle movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_paddle_v -= PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_paddle_v += PADDLE_SPEED
                if event.key == pygame.K_UP:
                    right_paddle_v -= PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right_paddle_v += PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    left_paddle_v += PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_paddle_v -= PADDLE_SPEED
                if event.key == pygame.K_UP:
                    right_paddle_v += PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right_paddle_v -= PADDLE_SPEED

        # update ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # update paddle movement
        p1.y += left_paddle_v
        p2.y += right_paddle_v
        if p1.top <= 15:
            p1.top = 15
        if p1.bottom >= HEIGHT - 15:
            p1.bottom = HEIGHT - 15
        if p2.top <= 15:
            p2.top = 15
        if p2.bottom >= HEIGHT - 15:
            p2.bottom = HEIGHT - 15

        # ball collision with borders
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.left <= 0 or ball.right >= WIDTH and game_over:
            ball_speed_x *= -1
        if ball.left <= 0 and not game_over:
            p2_score += 1
            ball.center = (WIDTH // 2, random.randint(0 + BALL_HEIGHT, HEIGHT - BALL_HEIGHT))
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))
        if ball.right >= WIDTH and not game_over:
            p1_score += 1
            ball.center = (WIDTH // 2, random.randint(0 + BALL_HEIGHT, HEIGHT - BALL_HEIGHT))
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))

        # ball collision with paddles
        if ball.colliderect(p1) or ball.colliderect(p2):
            ball_speed_x *= -1

        # check if either player reaches winning score
        if p1_score >= 11:
            game_over = True
            winner = 'P1 WIN!'
        if p2_score >= 11:
            game_over = True
            winner = 'P2 WIN!'

        # draw objects
        win.fill('black')
        pygame.draw.rect(win, 'white', p1)
        pygame.draw.rect(win, 'white', p2)
        pygame.draw.rect(win, 'white', ball)
        for i in range(0, HEIGHT, 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(win, 'white', (WIDTH//2 - 5, i, 1, 10))

        # draw score
        left_score = font.render(f"{p1_score}", False, 'white')
        win.blit(left_score, (WIDTH//4 - 10, 0))
        right_score = font.render(f"{p2_score}", False, 'white')
        win.blit(right_score, (WIDTH * 3//4 - 40, 0))

        # declare winner if either player reaches winning score
        if game_over:
            declare = font.render(winner, False, 'white')
            win.blit(declare, (WIDTH//2 - declare.get_width()//2, HEIGHT//2 - declare.get_height()//2))

        # update window
        pygame.display.flip()
        clock.tick(FPS)


# call main function
if __name__ == '__main__':
    main()
