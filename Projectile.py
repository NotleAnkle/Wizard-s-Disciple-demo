import pygame, sys
from pygame.locals import *

ShieldImg = pygame.image.load("Img\shield.png")
def drawBar(screen):
    pygame.draw.rect(screen, (0,0,0), (0, 2, 100 * 2 + 2, 22))
    pygame.draw.rect(screen, (255,255,255), (0, 3, 100 * 2 , 20))
    pygame.draw.rect(screen, (0,0,0), (0, 24, 100 * 2 + 2, 22))
    pygame.draw.rect(screen, (255,255,255), (0, 25, 100 * 2 , 20))
def ScreenLimit(target):
    if target.x + target.width > 1540:
        target.x = 1540 - target.height
    if target.x < 0:
        target.x = 0
    if target.y + target.height > 800:
        target.y = 800 - target.height
    if target.y < 140:
        target.y = 140


class projectile(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.speed = 20
        self.dame = 1
        self.hitBox = (x, y, radius)
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (100, 100, 100), (self.x, self.y), self.radius - 2)
        pygame.draw.circle(screen, (250, 250, 250), (self.x, self.y), self.radius - 3)
        pygame.draw.circle(screen, (255,0,0), (self.x, self.y), self.radius, 2)
    def hit(self, enemy, width, height):
        if self.x >= enemy.x and self.y >= enemy.y and self.x <= enemy.x + width and self.y <= enemy.y + height : return True
        return False
        
class shield(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.Cooldown = 2
        self.hitBox = (x,y, 16, 92)
    def draw(self, screen):
        if self.direction == "right":
            self.hitBox = ((self.x + 64, self.y, 16, 92))
            pygame.draw.ellipse(screen, (150, 150, 150), (self.x + 64, self.y, 16, 92))
        elif self.direction == "left":
            self.hitBox = (self.x - 16, self.y, 16, 92)
            pygame.draw.ellipse(screen, (150, 150, 150), (self.x - 16, self.y, 16, 92))
        elif self.direction == "up":
            self.hitBox = (self.x - 14, self.y - 16, 92, 16)
            pygame.draw.ellipse(screen, (150, 150, 150), (self.x - 14, self.y - 16, 92, 16))   
        elif self.direction == "down":
            self.hitBox = (self.x - 14, self.y + 94, 92, 16)
            pygame.draw.ellipse(screen, (150, 150, 150), (self.x - 14, self.y + 94, 92, 16))
        pygame.draw.rect(screen, (255,0,0), self.hitBox, 2)




    