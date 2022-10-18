import pygame, sys
from pygame.locals import *

pygame.init()

# 72 80 304 248
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1540, 800), 0, 32)
pygame.display.set_caption('Animation')
 
background = pygame.image.load("Img\Background.png")
rock = pygame.Rect(72, 80, 232, 168)
clone = pygame.image.load("Img\Clone.png")
icon = pygame.image.load("Img\Icon.png")
pygame.display.set_icon(icon)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

idle = [pygame.image.load("Img\Idle_1.png"),pygame.image.load("Img\Idle_2.png"),pygame.image.load("Img\Idle_1.png"),pygame.image.load("Img\Idle_4.png")]
walkDown = [pygame.image.load("Img\WalkDown_1.png"),pygame.image.load("Img\WalkDown_2.png")]
walkUp = [pygame.image.load("Img\WalkUp_1.png"),pygame.image.load("Img\WalkUp_2.png")]
walkRight = [pygame.image.load("Img\WalkRight_1.png"),pygame.image.load("Img\WalkRight_2.png"), pygame.image.load("Img\WalkRight_3.png"), pygame.image.load("Img\WalkRight_1.png")]
walkLeft = [pygame.image.load("Img\WalkLeft_1.png"),pygame.image.load("Img\WalkLeft_2.png"), pygame.image.load("Img\WalkLeft_3.png"), pygame.image.load("Img\WalkLeft_1.png")]
ChaImg = pygame.image.load('Img\Idle_1.png')
#ChaImg = pygame.transform.scale(ChaImg, (64, 92))
x = 0
y = 400
clone_x = 0
clone_y = 438
width = 64
height = 92
speed = 8
isJump = False
jumpCount = 8
walk = False

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


def inRock(x, y):
    if x >= 35 and x <= 277 and y >= 80 and y <=200:
        return True
    return False

walkYCount = 0
walkXCount = 0
idleCount = 0
direction = "down"
def redrawGameWindow():
    global walkYCount
    global walkXCount
    global idleCount
    screen.blit(background, (0, 0))
    screen.blit(clone, (clone_x, clone_y))
    if idleCount + 1 >= 48:
        idleCount = 0
    if walkYCount + 1 >= 20:
        walkYCount = 0
    if walkXCount + 1 >= 20:
        walkXCount = 0    
    if not(walk):
        screen.blit(idle[idleCount//12], (x,y)) 
        idleCount += 1
    elif direction == "down":
        screen.blit(walkDown[walkYCount//10], (x,y))
        walkYCount += 1
    elif direction == "up":
        screen.blit(walkUp[walkYCount//10], (x,y))
        walkYCount += 1
    elif direction == "right":
        screen.blit(walkRight[walkXCount//5], (x, y))
        walkXCount += 1
    elif direction == "left":
        screen.blit(walkLeft[walkXCount//5], (x, y))
        walkXCount += 1 
        
while True: # the main game loop
    keys = pygame.key.get_pressed()
    walk = False 
    if keys[pygame.K_LEFT] and x > 0:
        walk = True
        direction = "left"
        x -= speed
        clone_x -= speed
        if inRock(x, y):
            x += speed
            clone_x += speed
    if keys[pygame.K_RIGHT] and x < 1476:
        walk = True
        direction = "right"
        x += speed
        clone_x += speed
        if inRock(x, y):
            x -= speed
            clone_x -= speed
    if keys[pygame.K_UP] and y > 140:
        walk = True
        direction = "up"
        y -= speed
        clone_y -= speed
        if inRock(x, y):
            y += speed
            clone_y += speed
    if keys[pygame.K_DOWN] and y < 700:
        walk = True
        y += speed
        clone_y += speed
        direction = "down"
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -8:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else: 
            jumpCount = 8
            isJump = False
        if y > 700: 
            y = 700
            clone_y = 732
    print(x, y)    
    redrawGameWindow()   
    #screen.blit(ChaImg, (x, y))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)