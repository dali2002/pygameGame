import pygame
from pygame.locals import *
import random
import time
import math
import os
import sys
pygame.init()
pygame.mixer.init()
#crash_sound = pygame.mixer.Sound("backgroundSound.wav")
die_sound = pygame.mixer.Sound("die.wav")
food_sound = pygame.mixer.Sound("food.wav")
click_sound = pygame.mixer.Sound("new.wav")
welcome_sound = pygame.mixer.Sound("welcome.wav")
bigBoss = pygame.mixer.Sound("BogBossSound.wav")
base_dir = getattr(sys,'_MEIPASS','.')
image_path = os.path.join(base_dir,'assets','')
#welcome_sound.set_volume(1.0)
#welcome_sound.play()
#crash_sound.set_volume(0.7)
#pygame.time.wait(3000)
#crash_sound.play()
click_sound.set_volume(10)
x = 800
y = 600
fullscreen = False
screen = pygame.display.set_mode((x, y))
title = pygame.display.set_caption("Snake Game")

# Initialize the best score
best_score = 0

# Define the path for saving and loading the best score file
best_score_file = "best_score.txt"

# Load the best score if the file exists
if os.path.exists(best_score_file):
    with open(best_score_file, "r") as file:
        best_score = int(file.read())

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (x, y))

play_button = pygame.image.load("play.png")
play_button = pygame.transform.scale(play_button, (100, 50))
exit_button = pygame.image.load("exit.png")
exit_button = pygame.transform.scale(exit_button, (100, 50))
pause_button = pygame.image.load("pause.png")
pause_button = pygame.transform.scale(pause_button, (50, 50))
sound_button = pygame.image.load("sound.png")
sound_button = pygame.transform.scale(sound_button, (50, 50))
title_image = pygame.image.load("title.png")
full_screen_button = pygame.image.load("full.png")
full_screen_button = pygame.transform.scale(full_screen_button, (240, 200))

sound_playing = True

def save_best_score():
    global best_score
    with open(best_score_file, "w") as file:
        file.write(str(best_score))

def toggle_sound():
    global sound_playing
    if sound_playing:
        pygame.mixer.pause()
    else:
        pygame.mixer.unpause()
    sound_playing = not sound_playing

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

snake_x = x // 2
snake_y = y // 2
snake_length = 70
snake_speed = 5
game_started = False
game_paused = False
snake_direction = "right"
snake_body = [(snake_x, snake_y)]
score = 0

dot_x = random.randint(0, x - 10)
dot_y = random.randint(0, y - 10)
last_boss_dot_time = time.time()  # Track the last time a boss dot was spawned

def spawn_boss_dot():
    global dot_x, dot_y, last_boss_dot_time
    dot_x = random.randint(0, x - 30)
    dot_y = random.randint(0, y - 30)
    last_boss_dot_time = time.time()

def is_close_to_boss_dot():
    global snake_x, snake_y, dot_x, dot_y
    distance = math.sqrt((snake_x - dot_x) ** 2 + (snake_y - dot_y) ** 2)
    return distance < 20  # Adjust this threshold as needed

def move_snake():
    global snake_x, snake_y, snake_body, dot_x, dot_y, snake_length, snake_direction, score, run, best_score

    current_time = time.time()
    if current_time - last_boss_dot_time >= 50:
        spawn_boss_dot()

    if snake_direction == "right":
        snake_x += snake_speed
    elif snake_direction == "left":
        snake_x -= snake_speed
    elif snake_direction == "up":
        snake_y -= snake_speed
    elif snake_direction == "down":
        snake_y += snake_speed

    if snake_x <= dot_x <= snake_x + 10 and snake_y <= dot_y <= snake_y + 10:
        if current_time - last_boss_dot_time < 50:
            # It's a regular food dot
            snake_length += 10
            dot_x = random.randint(0, x - 10)
            dot_y = random.randint(0, y - 10)
            score += 1
            food_sound.play()
        else:
            # It's a boss dot
            snake_length += 30  # Boss dots give more length
            spawn_boss_dot()  # Respawn boss dot elsewhere
            score += 5  # Boss dots give more score
            bigBoss.play()

    if (snake_x, snake_y) in snake_body[1:]:
        die_sound.play()
        if score > best_score:
            best_score = score  # Update the best score
            save_best_score()  # Save the best score
        displayFinalScore()
        pygame.time.wait(1500)
        run = False

    snake_body.insert(0, (snake_x, snake_y))

    if len(snake_body) > snake_length // snake_speed:
        snake_body.pop()

    if snake_x >= x:
        snake_x = 0
    elif snake_x < 0:
        snake_x = x - 10
    if snake_y >= y:
        snake_y = 0
    elif snake_y < 0:
        snake_y = y - 10

def countNumbers():
    start = 5
    end = 500
    interval = 10
    numbers = list(range(start, end + 1, interval))
    return numbers

def snake():
    for segment in snake_body:
        pygame.draw.rect(screen, black, pygame.Rect(segment[0], segment[1], 10, 10))

def displayFinalScore():
    fontcoder = pygame.font.Font(None, 36)
    text = fontcoder.render(f"Your final score is: {score}", True, black)
    screen.blit(text, (100, 100))

def draw_dot():
    pygame.draw.rect(screen, red, pygame.Rect(dot_x, dot_y, 10, 10))

def drawBossDots():
    pygame.draw.rect(screen, red, pygame.Rect(dot_x, dot_y, 30, 30))

def displaydevCoder():
    fontcoder = pygame.font.Font(None, 36)
    text = fontcoder.render("This Game is created by Mohamed Ali Mabrouk", True, black)
    screen.blit(text, (100, 550))

def display_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, black)
    screen.blit(text, (10, 10))

def display_best_score():
    font = pygame.font.Font(None, 24)
    text = font.render(f"Best Score: {best_score}", True, black)
    screen.blit(text, (10, 40))

run = True
clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == KEYDOWN:
            if not game_started:
                game_started = True
            elif game_paused:
                game_paused = False
            elif game_started and not game_paused:
                if event.key == K_RIGHT:
                    snake_direction = "right"
                elif event.key == K_LEFT:
                    snake_direction = "left"
                elif event.key == K_UP:
                    snake_direction = "up"
                elif event.key == K_DOWN:
                    snake_direction = "down"
                if event.key == K_f:
                    if fullscreen:
                        screen = pygame.display.set_mode((x, y))
                        fullscreen = False
                    else:
                        screen = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
                        fullscreen = True
                if event.key == K_ESCAPE:
                    screen = pygame.display.set_mode((x, y))
                    fullscreen = False

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not game_started:
                if (x // 2 - 50 < mouse_x < x // 2 + 50) and (y // 2 - 25 < mouse_y < y // 2 + 25):
                    game_started = True
                    click_sound.set_volume(1.0)
                    click_sound.play()
                elif (x // 2 - 50 < mouse_x < x // 2 + 50) and (y // 2 + 25 < mouse_y < y // 2 + 75):
                    click_sound.play()
                    pygame.time.wait(1000)
                    run = False

            elif game_started and not game_paused:
                if (x - 60 < mouse_x < x - 10) and (10 < mouse_y < 60):
                    game_paused = True
                    click_sound.play()
                elif (x - 130 < mouse_x < x - 80) and (10 < mouse_y < 60):
                    click_sound.play()
                    pygame.time.wait(500)
                    toggle_sound()
    if not game_started:
        screen.blit(background_image, (0, 0))
        screen.blit(play_button, (x // 2 - 50, y // 2 - 25))
        screen.blit(exit_button, (x // 2 - 50, y // 2 + 25))
        displaydevCoder()
        #screen.blit(full_screen_button, (635, -50))
        screen.blit(title_image, (250, 100))
    elif not game_paused:
        move_snake()
        screen.blit(background_image, (0, 0))
        screen.blit(pause_button, (x - 60, 10))
        if sound_playing:
            screen.blit(sound_button, (x - 130, 10))
        else:
            screen.blit(sound_button, (x - 130, 10))
        snake()
        draw_dot()
        if score % 10 == 0 and score > 0:
            if is_close_to_boss_dot():
                score += 5
                food_sound.play()
                dot_x = random.randint(0, x - 10)
                dot_y = random.randint(0, y - 10)
            else:
                drawBossDots()

        display_score()
        display_best_score()
    else:
        screen.blit(pause_button, (x - 60, 10))
    pygame.display.flip()
    if not game_paused:
        clock.tick(15)

# After the game loop exits, quit the game
pygame.quit()
