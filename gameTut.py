import pygame
from random import randint
import math
from pygame import mixer
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('background.jpg')

# music:
# rats:
#mixer.music.load('background.mp3') 
# dance macabre:
mixer.music.load('background2.mp3') 
mixer.music.play(-1)

# Caption and logo:
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(randint(0, 736))
    enemyY.append(randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# ready means cant see bullet on scrn
# fire means bullet is moving
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    score = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(score, (200, 250))

def player(x, y):
    # blit draws on our screen, here we draw the player image
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    # blit draws on our screen, here we draw the player image
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # draw bullet on screen
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # using the distance between two points formula:
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop:
running = True
while running:
    # fill with RGB (colors)
    screen.fill((0, 0, 0))
    # add background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_UP:
                if bullet_state is "ready":     
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # check whether key is released (KEYUP, as opposed to KEYDOWN; pressed)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # moving the player by the incremental value above (|0.1|)
    playerX += playerX_change

    # make sure player doesnt go off screen:
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736: # 800 - 64
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over text
        if enemyY[i] > 440:
            # when one of the enemies exceeds this, collect all enemies and move out of screen
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]  = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
    
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # respawning the enemy when show
            enemyX[i] = randint(0, 735)
            enemyY[i] = randint(50,150)
        
        # calling enemy function (that draws (blit) the enemies on scrn)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # draw player:
    player(playerX, playerY)

    # show score on screen
    show_score(textX, textY)

    pygame.display.update()


# https://www.youtube.com/watch?v=FfWpgLFMI7w
# ON 1:55:08 (adding text etc.)