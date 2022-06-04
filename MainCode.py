import pygame
import random
import math
import time

clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()

# WINDOW INFO
screen = pygame.display.set_mode((800,800))
GameTitle = pygame.display.set_caption("Siege 0.3")
Icon = pygame.image.load("Images/GameIcon.png")
GameIcon = pygame.display.set_icon(Icon)
BackgroundMain = pygame.image.load("Images/mainBg.jpg")

#--GAME STATS--
score = 0
stage = 0
stage2 = 0
stage3 = 0
HP = 3
Alive = True

#EVENTS
def DamageTaken():
    global HP
    screen.blit(TakingDamageIMG, (0,0))
    HP -= 1
    baseDamaged.play()
    pygame.display.update()

#---SOUNDS---
bulletSound = pygame.mixer.Sound("Audio/Fire.wav")
bulletSound.set_volume(0.4)
noAmmo = pygame.mixer.Sound("Audio/No_Ammo.wav")
stage2Ann = pygame.mixer.Sound("Audio/Stage2Ann.mp3")
stage3Ann = pygame.mixer.Sound("Audio/Stage3Ann.mp3")
baseDamaged = pygame.mixer.Sound("Audio/BaseAttacked.wav")
GameOverSFX = pygame.mixer.Sound("Audio/GameOver.wav")

musicS1v1 = pygame.mixer.Sound("Audio/MusicS1v1.mp3")
musicS1v2 = pygame.mixer.Sound("Audio/MusicS1v2.mp3")
musicS2v1 = pygame.mixer.Sound("Audio/MusicS2v1.mp3")
musicS2v2 = pygame.mixer.Sound("Audio/MusicS2v2.mp3")
musicS3v1 = pygame.mixer.Sound("Audio/MusicS3v1.mp3")
musicS3v2 = pygame.mixer.Sound("Audio/MusicS3v2.mp3")
musicS1 = [musicS1v1, musicS1v2]
musicS2 = [musicS2v1, musicS2v2]
musicS3 = [musicS3v1, musicS3v2]
music1 = random.choice(musicS1)
music1.set_volume(0.5)
music1.play()
music2 = random.choice(musicS2)
music2.set_volume(0.55)
music3 = random.choice(musicS3)
music3.set_volume(0.6)

explosion1 = pygame.mixer.Sound("Audio/explosion1.wav")
explosion2 = pygame.mixer.Sound("Audio/explosion2.wav")
explosion3 = pygame.mixer.Sound("Audio/explosion3.wav")
explosionAny = [explosion1,explosion2,explosion3]

#---IMAGES---
PlayerImg = pygame.image.load("Images/Player.png")
PlayerFireImg = pygame.image.load("Images/PlayerFire.png")
bulletImg = pygame.image.load("Images/bulletS1.png")
bulletS2_IMG = pygame.image.load("Images/bulletS2.png")
enemy1S1_IMG = pygame.image.load("Images/enemy1S1.png")
enemy1S2_IMG = pygame.image.load("Images/enemy1S2.png")
enemy1S3_IMG = pygame.image.load("Images/enemy1S3.png")
enemy2S1_IMG = pygame.image.load("Images/enemy2S1.png")
enemy2S2_IMG = pygame.image.load("Images/enemy2S2.png")
enemy2S3_IMG = pygame.image.load("Images/enemy2S3.png")
Stage2Ann_IMG = pygame.image.load("Images/stage2Ann.png")
Stage3Ann_IMG = pygame.image.load("Images/stage3Ann.png")
GameOverIMG = pygame.image.load("Images/GameOver.png")
TakingDamageIMG = pygame.image.load("Images/TakingDamage.png")

#PLAYER
playerY = 678
playerX = 330
playerXspeed = 0
def PlayerMove(X, Y):
    screen.blit(PlayerImg, (X, Y))

#Bullet
bulletState = False
bulletY = 800
bulletX = 678
bulletYspeed = -18
FireSound = 1
def BulletFire(x,y):
    global bulletState
    bulletState = True
    screen.blit(bulletImg, (x+19, y-150))

def IsCollision(enemy1X, enemy1Y, bulletX, bulletY, enemyHitbox):
    distance = math.sqrt((math.pow(enemy1X-bulletX,2)) + (math.pow(enemy1Y-bulletY,2)))
    if distance < enemyHitbox:
        return True
    else:
        return False

#ENEMIES enemy1
enemy1Y = -350
enemy1X = random.randint(5,695)
enemy1Yspeed = 1
enemy1Hitbox = 105
def Enemy1(X, Y):
    screen.blit(enemy1S1_IMG, (X, Y))
#enemy2
enemy2Y = -1300
enemy2X = random.randint(5,695)
enemy2Yspeed = 1.4
enemy2Hitbox = 30
def Enemy2(X, Y):
    screen.blit(enemy2S1_IMG, (X, Y))

#-----GAME LOOP-----#
GAME = True
while GAME:
    screen.blit(BackgroundMain, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        if event.type == pygame.KEYDOWN:
                #FIRING
            if event.key == pygame.K_SPACE:     
                bulletX = playerX 
                BulletFire(bulletX,bulletY)
                PlayerImg = PlayerFireImg
                if bulletY > 675:
                    bulletSound.play()
                if bulletY < 675:
                    noAmmo.play()
                # MOVEMENT CONTROLS
            if event.key == pygame.K_a:
                playerXspeed = -6
            if event.key == pygame.K_d:
                playerXspeed = 6

        if event.type == pygame.KEYUP:
            playerXspeed = 0
            PlayerImg = pygame.image.load("Images/Player.png")
    #MAP  
    if playerX > 720:
        playerX = 720
    if playerX < 0:
        playerX = 0

    if bulletState == True:
        BulletFire(bulletX, bulletY)
        bulletY += bulletYspeed
    if bulletY < 100:
        bulletY = 800
        bulletState = False
    # COLLISION
    collision = IsCollision(enemy1X, enemy1Y, bulletX, bulletY, enemy1Hitbox)
    if collision:
        bulletY = 800
        if bulletState==False:
            score=score    
        bulletState = False
        score += 1
        enemy1Y = -100
        enemy1X = random.randint(5,695)
        explosion = random.choice(explosionAny)
        explosion.play()

    collision = IsCollision(enemy2X, enemy2Y, bulletX, bulletY, enemy2Hitbox)
    if collision:
        bulletY = 800
        if bulletState==False:
            score=score   
        bulletState = False
        score += 1
        enemy2Y = -100
        enemy2X = random.randint(5,695)
        explosion = random.choice(explosionAny)
        explosion.play()

# Damage Detection
    if enemy1Y > 660:
        enemy1Y = -100
        enemy1X = random.randint(5,695)
        DamageTaken()
    if enemy2Y > 660:
        enemy2Y = -100
        enemy2X = random.randint(5,695)
        DamageTaken()

# GAME OVER
        if HP <= 0:
            GameOverSFX.play()
            Alive = False

    if Alive == False:
        pygame.mixer.pause()
        GameOverSFX.play()
        for i in range(1,200):
            screen.blit(GameOverIMG, (0,0))
            pygame.display.update()
        GAME = False

    # STAGES
    if score == 3:
        stage += 1
        music1.set_volume(0)
        enemy2S1_IMG = enemy2S2_IMG
        enemy1S1_IMG = enemy1S2_IMG
        enemy2Yspeed = 2.5
        enemy1Yspeed = 1.6
        if stage == 25:
            music2.play()
            stage2Ann.play()
            for i in range(1,70):
                screen.blit(Stage2Ann_IMG, (0,0))
                pygame.display.update()
    if score == 60:
        stage2 += 1
        music2.set_volume(0)
        enemy2S1_IMG = enemy2S3_IMG
        enemy1S1_IMG = enemy1S3_IMG
        bulletImg = bulletS2_IMG
        bulletYspeed = -23
        enemy2Yspeed = 4.2
        enemy1Yspeed = 2.7
        if stage2 == 1:
            music3.play()
            stage3Ann.play()
            for i in range(1,70):
                screen.blit(Stage3Ann_IMG, (0,0))
                pygame.display.update()
    
    enemy1Y += enemy1Yspeed
    enemy2Y += enemy2Yspeed
    playerX += playerXspeed
    PlayerMove(playerX, playerY)
    Enemy1(enemy1X, enemy1Y)
    Enemy2(enemy2X, enemy2Y)
    clock.tick(60)
    pygame.display.update()
                


