import pygame, sys
from pygame.locals import *
from Projectile import *

SkeImg = pygame.image.load("Img\Ske.png")
SkeImg = pygame.transform.scale(SkeImg, (64, 102))
SkuImg = pygame.image.load("Img\Skull.png")
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
    def draw(self,screen):
       if self.x < self.target.x: self.x += min(self.speed, abs(self.x - self.target.x))
       else: self.x -= min(self.speed, abs(self.x - self.target.x))
       if self.y < self.target.y - 10: self.y += min(self.speed, abs(self.x - self.target.x))
       else: self.y -= min(self.speed, abs(self.x - self.target.x))
       screen.blit(SkuImg, (self.x, self.y))
       self.hitBox = pygame.Rect(self.x, self.y, self.width, self.height)
       pygame.draw.rect(screen, (255,0,0), self.hitBox, 2)
    def hit(self):
        if self.hitBox.colliderect(self.target.hitBox): return True
        return False

        