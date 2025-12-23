import pygame
import random
import os

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Screen size
screen_width = 900
screen_height = 600

# Create game window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes SMP")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# High score file
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

# Text function
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

# Snake drawing function
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Game loop
def gameloop():
    exit_game = False
    game_over = False

    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    snk_list = []
    snk_length = 1

    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)

    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 30

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(white)
            text_screen("Game Over! Press Enter to Restart", red, 150, 250)
            text_screen(f"Score: {score}", black, 350, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Food collision
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 5
                if score > highscore:
                    highscore = score

            gameWindow.fill(white)
            text_screen(f"Score: {score}  Highscore: {highscore}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Snake collision with itself
            if head in snk_list[:-1]:
                game_over = True

            # Wall collision
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

# Start the game
gameloop()



