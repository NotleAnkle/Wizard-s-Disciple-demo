import random
import pygame, sys
from pygame.locals import *
from Enemy import *
from Projectile import *

pygame.init()
pygame.mixer.init()

Boss = pygame.image.load("Img\Boss.png")
Boss_getHit = pygame.image.load("Img\Boss_getHit.png")
Boss_shadow = pygame.image.load("Img\Boss_shadow.png")
Boss_side = pygame.image.load("Img\Boss_side.png")
Boss_s1Ac = pygame.image.load("Img\Boss_s1Ac.png")
Boss = pygame.transform.scale(Boss, (250, 250))
Boss_getHit = pygame.transform.scale(Boss_getHit, (250, 250))
Boss_shadow = pygame.transform.scale(Boss_shadow, (230, 250/6))
Boss_side = pygame.transform.scale(Boss_side, (250, 250))
Boss_s1Ac = pygame.transform.scale(Boss_s1Ac, (250, 250))

Skill1Sound = pygame.mixer.Sound("Sound\Boss_Skill1.wav")
Skill1Sound.set_volume(0.5)
BSound_hurt = pygame.mixer.Sound("Sound\Boss_hurt.wav")
BSound_hurt.set_volume(0.6)

class boss(object):
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.sha_x = x
        self.sha_y = y + 250
        self.width = 250
        self.height = 250
        self.HP = 100
        self.hitBox = pygame.Rect(x + 10, y, 230, 250)
        self.GetHit = 0
        self.floatCount = 0
        self.Attacks = []
        self.Cooldown = 0
        self.Acskill = False
        self.facing = -1
        self.target = target
        
        #Skill 1
        self.s1_Ac = 0
        self.s1_Sp = 0
        self.s1_Cd = 0
        #Skill 2
        self.s2_Cd = 0
        #skill 3
        self.s3_cd = 0

    def draw(self,screen):
        #Cooldown
        if self.Cooldown > 0: self.Cooldown -= 1
        if self.s1_Cd > 0: self.s1_Cd -= 1
        if self.s2_Cd > 0: self.s2_Cd -= 1
        if self.s3_cd > 0: self.s3_cd -= 1
        
        
        if not(self.Acskill):
            #Idle
            if self.floatCount  >= -1:
                    self.y -= (self.floatCount  * abs(self.floatCount )) * 0.5
                    self.floatCount  -= 0.1
            else: 
                self.floatCount  = 1
            
            if self.GetHit > 0: 
                screen.blit(Boss_getHit, (self.x, self.y))
                self.GetHit -= 1
            else: screen.blit(Boss, (self.x, self.y))
        else:
            #Skill 1
            if(self.s1_Ac > 0):
                if self.s1_Ac > 30:
                    if self.y + 250 != self.target.y + 92:
                        if self.y + 250 > self.target.y + 92: self.y -= self.s1_Sp
                        else: self.y += self.s1_Sp
                    screen.blit(Boss, (self.x, self.y))
                elif self.s1_Ac > 25:
                    screen.blit(Boss_s1Ac, (self.x, self.y)) 
                else:
                    #Skill1Sound.play()
                    self.x += 30*self.facing
                    if self.facing == -1: screen.blit(Boss_side, (self.x, self.y))
                    else:  screen.blit(pygame.transform.flip(Boss_side, True, False), (self.x, self.y))
                self.s1_Ac -= 1
            else: self.Acskill = False
            self.sha_x = self.x
            self.sha_y = self.y + 250
        
        for At in self.Attacks:
                At.draw(screen)
        
        ScreenLimit(self)
        screen.blit(Boss_shadow, (self.sha_x, self.sha_y))
        
        #HP
        pygame.draw.rect(screen, (10,10,10), (1480, 200, 50, 100*5 + 4))
        pygame.draw.rect(screen, (200,200,200), (1480 + 2, 200 + 2 + (100 -self.HP)*5, 50 - 4, self.HP*5))
        
        #ColiderBox
        self.hitBox = pygame.Rect(self.x + 10, self.y, 230, 250)
        if ColiderBoxOn : pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)
            
    def getHit(self, dame):
        pygame.mixer.Channel(2).play(BSound_hurt)
        self.HP -= dame
        self.GetHit = 2
    
    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox): return True
        return False
    
    def Attack(self, Player):
                
        if self.s1_Cd == 0:
            self.skill1()
            self.s1_Cd = 120
            
        if self.s2_Cd == 0 and self.HP < 30:
            self.skill2()
            self.s2_Cd = 50
        
        if self.Cooldown == 0:
            #self.skill1()
            self.Attacks.append(skull(self.x, self.y, 64, 64,Player))
            self.Cooldown = 100
            
        if self.s3_cd == 0 and self.HP < 60:
            self.skill3()
            self.s3_cd = 150
    
    def skill1(self):
        
        if self.x - self.target.x > 0: self.facing = -1
        else: self.facing = 1
        pygame.mixer.Channel(1).play(Skill1Sound)
        self.s1_Sp = abs(self.target.y + 92 - self.y - 250)/10
        self.s1_Ac = 40
        self.Acskill = True
        self.s1_Cd = 10
        
    def skill2(self):
        x = random.randrange(-100, 100)
        if self.facing == 1: 
            self.Attacks.append(ske_hand(0, 200 + x, 1, self.target))
            self.Attacks.append(ske_hand(100, 450 + x, 1, self.target))
            self.Attacks.append(ske_hand(0, 700 + x, 1, self.target))
        else: 
            self.Attacks.append(ske_hand(1500, 200 + x, -1, self.target))
            self.Attacks.append(ske_hand(1400, 450 + x, -1, self.target))
            self.Attacks.append(ske_hand(1300, 700 + x, -1, self.target))
    
    def skill3(self):
        self.Attacks.clear()
        self.Attacks.append(floating_skull(self, self.target, 0))
        self.Attacks.append(floating_skull(self, self.target, 1))
        self.Attacks.append(floating_skull(self, self.target, 2))
        self.Attacks.append(floating_skull(self, self.target, 3))