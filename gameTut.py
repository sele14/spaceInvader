import pygame
from random import randint
import math
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('background.jpg')

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
# change per preferrence
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('terrorist.png'))
    # want to spawn random places
    enemyX.append(randint(0, 735))
    enemyY.append(randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet1.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# ready means cant see bullet on scrn
# fire means bullet is moving
bullet_state = "ready"
score = 0 # to keep score
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

    # enemy movement:
    for i in range(num_of_enemies):
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
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)
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
    pygame.display.update()

# https://www.youtube.com/watch?v=FfWpgLFMI7w
# ON 1:48:00