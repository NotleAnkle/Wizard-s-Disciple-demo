import pygame, sys
from pygame.locals import *
from Projectile import *

pygame.mixer.init()
SkeImg = pygame.image.load("Img\Ske.png")
SkeImg = pygame.transform.scale(SkeImg, (64, 102))
SkuImg = pygame.image.load("Img\Skull.png")
SkehandImg = pygame.image.load("Img\Ske_hand.png")

SkuSound = pygame.mixer.Sound("Sound\laugh.wav")
SkuSound.set_volume(1)
class skull(object):
    def __init__(self, x, y, width, height, target):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target = target
        self.speed = 5
        self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.walkCount = 0
        self.dame = 5
        pygame.mixer.Channel(4).play(SkuSound)
    def draw(self,screen):
       if self.x < self.target.x: self.x += min(self.speed, abs(self.x - self.target.x))
       else: self.x -= min(self.speed, abs(self.x - self.target.x))
       if self.y < self.target.y - 7: self.y += min(self.speed, abs(self.y - self.target.y + 10))
       else: self.y -= min(self.speed, abs(self.y - self.target.y + 10))
       screen.blit(SkuImg, (self.x, self.y))
       self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)
       if ColiderBoxOn: pygame.draw.rect(screen, (255,0,0), self.hitBox, 2)

    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox): return True
        return False

class ske_hand(object):
    def __init__(self, x, y, facing, target):
        self.x = x
        self.y = y
        self.facing = facing
        self.speed = 8
        self.rotate = 0
        self.hitBox = pygame.Rect(self.x, self.y, 34, 120)
        self.target = target
        self.dame = 3
        
    def draw(self, screen):
        self.x += 8*self.facing
        self.rotate += 90
        if(self.rotate >= 360): self.rotate = 0
        if self.rotate == 0:
            screen.blit(SkehandImg, (self.x, self.y - 60))
            self.hitBox = pygame.Rect(self.x, self.y - 60, 34, 120)
        if self.rotate == 90: 
            screen.blit((pygame.transform.rotate(SkehandImg, -90)), (self.x - 60, self.y - 17))
            self.hitBox = pygame.Rect(self.x - 60, self.y - 17, 120, 34)
        if self.rotate == 180:
            screen.blit(pygame.transform.flip(SkehandImg, True, True), (self.x , self.y - 60))
            self.hitBox = pygame.Rect(self.x, self.y - 60, 34, 120)
        if self.rotate == 270:
            screen.blit((pygame.transform.rotate(SkehandImg, 90)), (self.x - 30, self.y - 7))
            self.hitBox = pygame.Rect(self.x - 30, self.y - 7, 120, 34)
        
        if ColiderBoxOn: pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)
    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox): return True
        return False
            
        
        

        