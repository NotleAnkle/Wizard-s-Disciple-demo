import pygame, sys
from pygame.locals import *
from Character import *
from Projectile import *

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1540, 800), 0, 32)
pygame.display.set_caption("Wizard's disciple") 
background = pygame.image.load("Img\Background.png")
icon = pygame.image.load("Img\Icon.png")
pygame.display.set_icon(icon)

boss = pygame.image.load("Img\Boss.png")
boss = pygame.transform.scale(boss, (250, 250))

x = 0
y = 400
width = 64
height = 92
Wiz = player(x, y, width, height)

while True:
    screen.blit(background, (0, 0))
    screen.blit(boss, (1000, 200))
    
    if Wiz.Cooldown > 0: Wiz.Cooldown -= 1 
    Wiz.draw(screen)
    Wiz.move()
    Wiz.Attack()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(FPS)