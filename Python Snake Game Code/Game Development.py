import pygame
import random
import os
import sys

pygame.init()

# ---------- SAFE MIXER INIT ----------
try:
    pygame.mixer.init()
except:
    print("Audio device error")
    sys.exit()

# ---------- SCREEN ----------
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes SMP")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# ---------- FILE NAMES ----------
BG_IMAGE = "background.jpg"
BG_MUSIC = "bg_music.mp3"
BEEP_SOUND = "beep.mp3"
GAMEOVER_SOUND = "gameover.mp3"

# ---------- FILE CHECK ----------
files = [BG_IMAGE, BG_MUSIC, BEEP_SOUND, GAMEOVER_SOUND]
for f in files:
    if not os.path.exists(f):
        print(f" Missing file: {f}")
        sys.exit()

# ---------- LOAD ASSETS ----------
bgimg = pygame.image.load(BG_IMAGE).convert()
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height))

snake_beep = pygame.mixer.Sound(BEEP_SOUND)
gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND)

# ---------- HIGHSCORE ----------
if not os.path.exists("highscore.txt"):
    open("highscore.txt", "w").write("0")

# ---------- FUNCTIONS ----------
def text_screen(text, color, x, y):
    img = font.render(text, True, color)
    gameWindow.blit(img, (x, y))

def plot_snake(color, snk_list, size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, size, size])

# ---------- WELCOME ----------
def welcome():
    pygame.mixer.music.load(BG_MUSIC)
    pygame.mixer.music.play(-1)

    while True:
        gameWindow.blit(bgimg, (0, 0))
        text_screen("WELCOME TO S.N.A.K.E",(0,0, 0), 275, 250)
        text_screen("Press SPACE to Play", (0,0,0), 300, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameloop()

        pygame.display.update()
        clock.tick(60)

# ---------- GAME LOOP ----------
def gameloop():
    snake_x, snake_y = 45, 55
    vx, vy = 0, 0
    snk_list = []
    snk_len = 1
    size = 30
    score = 0

    food_x = random.randint(50, 800)
    food_y = random.randint(50, 500)

    game_over = False
    over_played = False

    while True:
        if game_over:
            pygame.mixer.music.stop()
            if not over_played:
                gameover_sound.play()
                over_played = True

            gameWindow.blit(bgimg, (0,0))
            text_screen("GAME OVER", (255,0,0), 370, 260)
            text_screen("Made by Sreedev Sreekumar", (0, 0, 0), 280, 550)
            text_screen("Press ENTER", (0,0,0), 370, 310)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        vx, vy = 5, 0; snake_beep.play()
                    if event.key == pygame.K_LEFT:
                        vx, vy = -5, 0; snake_beep.play()
                    if event.key == pygame.K_UP:
                        vx, vy = 0, -5; snake_beep.play()
                    if event.key == pygame.K_DOWN:
                        vx, vy = 0, 5; snake_beep.play()

            snake_x += vx
            snake_y += vy

            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                score += 10
                food_x = random.randint(50, 800)
                food_y = random.randint(50, 500)
                snk_len += 5

            gameWindow.blit(bgimg, (0,0))
            text_screen(f"Score: {score}", (255,0,0), 5, 5)
            pygame.draw.rect(gameWindow, (255,0,0), [food_x, food_y, size, size])

            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_len:
                del snk_list[0]

            if head in snk_list[:-1] or snake_x < 0 or snake_x > 870 or snake_y < 0 or snake_y > 570:
                game_over = True

            plot_snake((0,0,0), snk_list, size)

        pygame.display.update()
        clock.tick(30)

# ---------- START ----------
welcome()

#A Game using Python by Sreedev...


