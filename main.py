import pygame

pygame.init()  # Run this whenever you import pygame

WIDTH, HEIGHT, = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
WINNING_SCORE = 10

SCORE_FONT = pygame.font.SysFont("timesnewroman", 50)


# Handle paddles for pong
class Paddle:
    COLOUR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL  # as y value decreases we are going up
        else:
            self.y += self.VEL  # as y value increases we are going down

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5
    COLOUR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


# Handle drawing
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)  # Changes background colour to white

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)  # 1 argumemt is for anti-aliasing
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)  # 1 argumemt is for anti-aliasing
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

# Middle division line
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:  # if i is an even number
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    pygame.display.update()  # In order to actually change the display, we need to run this method update to reflect that
    # .update() is intensive , so only do it after doing all the colour updates


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:  # If ball is gonna hit the bottom , reverse direction
        # need to add ball.radius so that the edge of the ball is what triggers this and not just the edge
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:  # If ball is gonna hit the top, reverse direction
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


# Event loop - main loop when pygame in running which will do everything related to the game
def main():
    run = True
    clock = pygame.time.Clock()  # Regulates the speed
    # Want to get the middle of the rectangle exactly at the middle of the window, so you cannot drawing the rectangle
    # from the middle as then the whole rectangle wouldn't be at the centre of the window
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    # Taking width and subtracting from it 10 (the padding we want) and then subtracting width of rectangle gives us x
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        clock.tick(FPS)  # Makes it so that the game will only run 60 times per second; regulates speed of while loop
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # if we stop the program by clicking the 'x' we will stop the main program
                break

        keys = pygame.key.get_pressed()  # Get keys that user pressed
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False

        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left player won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right player won"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (
            WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # Text appears at middle
            pygame.display.update()  # Update so it instantly shows
            pygame.time.delay(5000)  # Delay by 5 seconds
            # reset everything
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':  # if we import this module, this would not run, only run this function if you run this file
    main()
