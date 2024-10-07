# CTR + ALT + L
from pickle import GLOBAL, FALSE

import pygame
import random
import math
import Menu
import time

pygame.init()

# Inserting background image
background = pygame.image.load('img.png')

# First line sets display name the other two set an icon next to the display name, top left
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)

game_paused = False
menu_state = 'main'
power_up_status = False

# Pause keys
resume_img = pygame.image.load("button_resume.png")
quit_img = pygame.image.load("button_quit.png")
options_img = pygame.image.load("button_options.png")
keys_img = pygame.image.load("button_keys.png")
video_img = pygame.image.load("button_video.png")
back_img = pygame.image.load("button_back.png")
audio_img = pygame.image.load("button_audio.png")
restart_img = pygame.image.load("Restart.png")

# Where buttons are placed
resume_button = Menu.Button(304, 125, resume_img, 1)
quit_button = Menu.Button(336, 375, quit_img, 1)
options_button = Menu.Button(297, 250, options_img, 1)
keys_button = Menu.Button(246, 325, keys_img, 1)
video_button = Menu.Button(226, 75, video_img, 1)
back_button = Menu.Button(332, 450, back_img, 1)
audio_button = Menu.Button(225, 200, audio_img, 1)
restart_button = Menu.Button(350, 350, restart_img, 1)

# Player
player_image = pygame.image.load('Player.png')
PlayerX = 370  # coordinates Y and X axis (X across, Y UP and Down)
PlayerY = 480
PlayerX_change = 0
PlayerY_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
saved_enemyX_change = []  # Save the current X movement when paused
saved_enemyY_change = []  # Save the current Y movement when paused
num_enemys = 6

# Speed boost
speed_image = pygame.image.load('speed.png')
speedX = random.randint(0, 735)
speedY = random.randint(0, 480)

# Black line
line_image = pygame.image.load('line.png')
lineX = 670
lineY = 390
lineX2 = 506  # 40 gap
lineX3 = 342
lineX4 = 178
lineX5 = 14
# Reset enemy power
reset_image = pygame.image.load('Reset_enemy.png')
resetX = random.randint(0, 735)
resetY = random.randint(0, 480)

for i in range(num_enemys):
    enemy_image.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, 735))  # Makes the enemy appear randomly between the pixels listed
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)

# Bullet: Ready means you cannot see bullet on screen, fire means it is currently moving
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = 'ready'

# score

previous_score = 0
high_score = 0
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 22)  # First variable is font, second is size of it
score_font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10

overX = 190
overY = 250

previous_x = 10
previous_y = 75

high_x = 10
high_y = 45

game_over = False


def game_over_text(overX, overY):
    font = pygame.font.Font('freesansbold.ttf', 64)
    game_over = font.render("GAME OVER", True, (255, 255, 255))
    window.blit(game_over, (overX, overY))


def show_score(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))


def show_previous_score(previous_x, previous_y):
    score = font.render("Last Score : " + str(previous_score), True, (255, 255, 255))
    window.blit(score, (previous_x, previous_y))


def show_high_score(high_x, high_y):
    score = font.render("High Score : " + str(high_score), True, (255, 255, 255))
    window.blit(score, (high_x, high_y))


def player(x, y):
    window.blit(player_image, (x, y))  # blit means to draw


def enemy(x, y, i):
    window.blit(enemy_image[i], (x, y))


def speed_boost(speedX, speedY):
    window.blit(speed_image, (speedX, speedY))


def line(lineX, lineY):
    window.blit(line_image, (lineX, lineY))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    window.blit(bullet_image, (x + 16, y + 10))  # +16 to center, +10 to appear above the ship


def power_collision(speedX, speedY, PlayerX, PlayerY):
    distance = math.sqrt((math.pow(PlayerX - speedX, 2)) + (math.pow(PlayerY - speedY, 2)))  # Distance formula
    if distance <= 40:
        return True
    return False


def reset_collision(resetX, resetY, PlayerX, PlayerY):
    window.blit(reset_image, (resetX, resetY))
    distance = math.sqrt((math.pow(PlayerX - resetX, 2)) + (math.pow(PlayerY - resetY, 2)))  # Distance formula
    if distance <= 40:
        return True
    return False


def iscollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))  # Distance formula
    if distance <= 27:
        return True
    return False


def playercollision(PlayerX, PlayerY, enemyX, enemyY):
    distance = math.sqrt((math.pow(enemyX - PlayerX, 2)) + (math.pow(enemyY - PlayerY, 2)))  # Distance formula
    if distance <= 40:
        return True
    return False


# Set alpha (transparency) values
def set_transparency(surface, alpha_value):
    surface.set_alpha(alpha_value)


# Displays Window screen
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

# Main game loop
while running:
    window.fill((250, 250, 250))  # RGB Red, Green, Blue
    window.blit(background, (0, 0))

    if game_paused:
        # Set transparency when the menu is active
        # Makes everything transparent
        window.fill((11, 51, 112))
        set_transparency(background, 0)  # Background transparency
        set_transparency(player_image, 0)  # Player transparency
        set_transparency(bullet_image, 0)
        set_transparency(reset_image, 0)
        set_transparency(speed_image, 0)
        set_transparency(line_image, 0)
        for i in range(num_enemys):
            saved_enemyX_change.append(enemyX_change[i])  # Save enemy X movement
            saved_enemyY_change.append(enemyY_change[i])  # Save enemy Y movement
            enemyX_change[i] = 0  # Stop movement
            enemyY_change[i] = 0
            set_transparency(enemy_image[i], 0)  # Enemy transparency

        # Check menu state
        if menu_state == 'main':
            if resume_button.draw(window):
                game_paused = False
                # Restore full visibility when the game resumes
                set_transparency(background, 255)
                set_transparency(player_image, 255)
                set_transparency(bullet_image, 255)
                set_transparency(speed_image, 255)
                set_transparency(reset_image, 255)
                set_transparency(line_image, 255)

                for i in range(num_enemys):
                    enemyX_change[i] = saved_enemyX_change[i]
                    enemyY_change[i] = saved_enemyY_change[i]

                    set_transparency(enemy_image[i], 255)
                    # Clear saved values
                saved_enemyX_change.clear()
                saved_enemyY_change.clear()

            if options_button.draw(window):
                menu_state = 'options'
            if quit_button.draw(window):
                running = False

        if menu_state == 'options':
            if audio_button.draw(window):
                print("Audio")
            if video_button.draw(window):
                print("Video")
            if keys_button.draw(window):
                print('Keys')
            if back_button.draw(window):
                menu_state = 'main'

    else:
        # Restore normal rendering when not paused
        player(PlayerX, PlayerY)
        for i in range(num_enemys):
            enemy(enemyX[i], enemyY[i], i)

    # Makes sure when you hit the X in top right the application closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # The movement of the character
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                PlayerX_change = -6
                if power_up_status == True:
                    PlayerX_change = -9
            if event.key == pygame.K_d:
                PlayerX_change = +6
                if power_up_status == True:
                    PlayerX_change = +9
            if event.key == pygame.K_w:
                PlayerY_change = -6
                if power_up_status == True:
                    PlayerY_change = -9
            if event.key == pygame.K_s:
                PlayerY_change = +6
                if power_up_status == True:
                    PlayerY_change = +9
            if event.key == pygame.K_ESCAPE:
                game_paused = True
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bulletX = PlayerX
                bulletY = PlayerY
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_w:
                PlayerX_change = 0
                PlayerY_change = 0
    PlayerX += PlayerX_change
    PlayerY += PlayerY_change

    # Barrier for the player to prevent going off-screen
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736
    if PlayerY <= 0:
        PlayerY = 0
    elif PlayerY >= 500:
        PlayerY = 500

    # Enemy movement
    for i in range(num_enemys):
        if enemyY[i] > 410:
            for j in range(num_enemys):
                enemyY[j] = 2000
            game_over = True
            game_over_text(overX, overY)
            previous_score = score_value
            if score_value > high_score:
                high_score = score_value

            # Check if restart button is clicked
            if game_over:
                if restart_button.draw(window):
                    # Reset the game state
                    power_up_status = FALSE
                    game_over = False
                    bulletY_change = 15
                    PlayerX = 370
                    PlayerX_change = 0
                    PlayerY = 480
                    PlayerY_change = 0
                    bullet_state = 'ready'
                    bulletY = 480
                    score_value = 0

                    # Reset enemies
                    enemyX.clear()
                    enemyY.clear()
                    enemyX_change.clear()
                    enemyY_change.clear()

                    for i in range(num_enemys):
                        enemyX.append(random.randint(0, 735))
                        enemyY.append(random.randint(50, 150))
                        enemyX_change.append(4)
                        enemyY_change.append(40)

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3.5
            enemyY[i] += enemyY_change[i]

        # Collision detection
        collision = iscollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        playcoll = playercollision(PlayerX, PlayerY, enemyX[i], enemyY[i])
        if playcoll == True:
            for j in range(num_enemys):
                enemyY[j] = 2000
            game_over = True
            game_over_text(overX, overY)
            speedX = 2000
            resetX = 2000
            previous_score = score_value
            if score_value > high_score:
                high_score = score_value

        power_up = power_collision(speedX, speedY, PlayerX, PlayerY)
        if power_up:
            speedY = 1000
            power_up_status = True
            if power_up_status == True:
                bulletY_change = 20
        enemy(enemyX[i], enemyY[i], i)

        reset_up = reset_collision(resetX, resetY, PlayerX, PlayerY)
        if reset_up:
            resetY = 1000
            for i in range(num_enemys):
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

    # Bullet movement
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    line(lineX, lineY)
    line(lineX2, lineY)
    line(lineX3, lineY)
    line(lineX4, lineY)
    line(lineX5, lineY)
    reset_collision(resetX, resetY, PlayerX, PlayerY)
    speed_boost(speedX, speedY)
    player(PlayerX, PlayerY)
    show_score(textX, textY)
    show_high_score(high_x, high_y)
    show_previous_score(previous_x, previous_y)

    pygame.display.update()
