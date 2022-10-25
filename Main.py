import pygame, sys
from pygame.locals import *
from Character import *
from Enemy import *
from Projectile import *
from Boss import *

pygame.init()
pygame.mixer.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1540, 800), 0, 32)
pygame.display.set_caption("Wizard's disciple") 
background = pygame.image.load("Img\Background.png")
icon = pygame.image.load("Img\Icon.png")
pygame.display.set_icon(icon)
lose = pygame.image.load("Img\Lose.png")
lose = pygame.transform.scale(lose, (1540, 800))
win = pygame.transform.scale(pygame.image.load("Img\Win.png"), (1540, 800))

music = pygame.mixer.music.load("Sound\BG.wav")
pygame.mixer.music.set_volume(1.1)

x = 0
y = 400
width = 64
height = 92
Wiz = player(x, y, width, height)
Boss = boss(1000, 200, Wiz)
running = True
pygame.mixer.music.play(-1)
while running:
    screen.blit(background, (0, 0))
    
    if Wiz.HP > 0 and Boss.HP > 0:
        
        if Wiz.Cooldown > 0: Wiz.Cooldown -= 1 
        if Boss.hit(): Wiz.getHit(10)
        Wiz.move()
        #Wiz.Attack()
        Wiz.draw(screen)
        for At in Wiz.Attacks:
            if At.hit(Boss, 230, 250):
                Boss.getHit(At.dame)
                Wiz.Attacks.remove(At)
            for Atb in Boss.Attacks:
                if At.hit(Atb, 64, 64):
                    Boss.Attacks.remove(Atb)
                    Wiz.Attacks.remove(At)
                    if Wiz.MP < 100: Wiz.MP += 3
        
        Boss.Attack(Wiz)
        if Boss.s1_Cd == 0:
            #Boss.skill1()
            Boss.s1_Cd = 150  
        Boss.draw(screen)
        for Atb in Boss.Attacks:
            if Atb.hit():
                Wiz.getHit(Atb.dame)
                Boss.Attacks.remove(Atb)
    elif Wiz.HP <= 0:
        screen.blit(lose, (0,0))
    elif Boss.HP <= 0:
        screen.blit(win, (0,0))  
    
    pygame.draw.rect(screen, (0,0,0), (0,0,1540,800), 1)
 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fpsClock.tick(FPS)