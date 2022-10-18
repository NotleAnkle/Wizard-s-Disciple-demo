import pygame, sys
from pygame.locals import *

class projectile(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.speed = 20
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius - 2)