import pygame, sys
from pygame.locals import *
from Projectile import *

clone = pygame.image.load("Img\Clone.png")
idle = [pygame.image.load("Img\Idle_1.png"),pygame.image.load("Img\Idle_2.png"),pygame.image.load("Img\Idle_1.png"),pygame.image.load("Img\Idle_4.png")]
walkDown = [pygame.image.load("Img\WalkDown_1.png"),pygame.image.load("Img\WalkDown_2.png")]
walkUp = [pygame.image.load("Img\WalkUp_1.png"),pygame.image.load("Img\WalkUp_2.png")]
walkRight = [pygame.image.load("Img\WalkRight_1.png"),pygame.image.load("Img\WalkRight_2.png"), pygame.image.load("Img\WalkRight_3.png"), pygame.image.load("Img\WalkRight_1.png")]
walkLeft = [pygame.image.load("Img\WalkLeft_1.png"),pygame.image.load("Img\WalkLeft_2.png"), pygame.image.load("Img\WalkLeft_3.png"), pygame.image.load("Img\WalkLeft_1.png")]
ChaImg = pygame.image.load('Img\Idle_1.png')
AttackAnimation = [pygame.image.load("Img\AttackLeft.png"),pygame.image.load("Img\AttackRight.png"),pygame.image.load("Img\AttackUp.png"),pygame.image.load("Img\AttackDown.png")]

x = 0
y = 400
clone_x = 0
clone_y = 439
width = 64
height = 92
speed = 7
isJump = False
jumpCount = 8
walk = False

def inRock(x, y):
    if x >= 35 and x <= 277 and y >= 80 and y <=200:
        return True
    return False

class player(object):
    def __init__(self, x, y, width, height):
        self.HP = 100
        self.MP = 100
        self.clone_x = x
        self.clone_y = y + 39
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.isJump = False
        self.walk = False
        self.direction = "left"
        self.walkYCount = 0
        self.walkXCount = 0
        self.idleCount = 0
        self.jumpCount = 8
        self.Attacks = []
        self.Cooldown = 0
        self.isAt = False
        self.AtCount = 0
    
    def move(self):
        keys = pygame.key.get_pressed()
        self.walk = False
        self.direction = "" 
        if keys[pygame.K_LEFT] and self.x > 0:
            self.walk = True
            self.direction = "left"
            self.x -= speed
            self.clone_x -= speed
            if inRock(self.x, self.y):
                self.x += speed
                self.clone_x += speed
        if keys[pygame.K_RIGHT] and self.x < 1476:
            self.walk = True
            self.direction = "right"
            self.x += speed
            self.clone_x += speed
            if inRock(self.x, self.y):
                self.x -= speed
                self.clone_x -= speed
        if keys[pygame.K_UP] and self.y > 140:
            self.walk = True
            self.direction = "up"
            self.y -= speed
            self.clone_y -= speed
            if inRock(self.x, self.y):
                self.y += speed
                self.clone_y += speed
        if keys[pygame.K_DOWN] and self.y < 700:
            self.walk = True
            self.y += speed
            self.clone_y += speed
            self.direction = "down"
        if not(self.isJump):
            if keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -8:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else: 
                self.jumpCount = 8
                self.isJump = False
            if self.y > 700: 
                self.y = 700
                self.clone_y = 732
        
    def draw(self, screen):
        screen.blit(clone, (self.clone_x, self.clone_y))
        #Heal bar
        pygame.draw.rect(screen, (0,0,0), (0, 2, 100 * 2 + 2, 22))
        pygame.draw.rect(screen, (255,255,255), (0, 3, 100 * 2 , 20))
        pygame.draw.rect(screen, (50,50,50), (0, 3, self.HP * 2 , 20))
        pygame.draw.rect(screen, (0,0,0), (0, 24, 100 * 2 + 2, 22))
        pygame.draw.rect(screen, (255,255,255), (0, 25, 100 * 2 , 20))
        pygame.draw.rect(screen, (128,128,128), (0, 25, self.MP * 2 , 20))
        
        # Character animation
        if not(self.isAt):
            if self.idleCount + 1 >= 48:
                self.idleCount = 0
            if self.walkYCount + 1 >= 20:
                self.walkYCount = 0
            if self.walkXCount + 1 >= 20:
                self.walkXCount = 0    
            if not(self.walk):
                screen.blit(idle[self.idleCount//12], (self.x,self.y)) 
                self.idleCount += 1
            elif self.direction == "down":
                screen.blit(walkDown[self.walkYCount//10], (self.x,self.y))
                self.walkYCount += 1
            elif self.direction == "up":
                screen.blit(walkUp[self.walkYCount//10], (self.x,self.y))
                self.walkYCount += 1
            elif self.direction == "right":
                screen.blit(walkRight[self.walkXCount//5], (self.x,self.y))
                self.walkXCount += 1
            elif self.direction == "left":
                screen.blit(walkLeft[self.walkXCount//5], (self.x,self.y))
                self.walkXCount += 1
        else:
            if self.direction == "left":
                screen.blit(AttackAnimation[0], (self.x,self.y))
            if self.direction == "right":
                screen.blit(AttackAnimation[1], (self.x,self.y))
            if self.direction == "up":
                screen.blit(AttackAnimation[2], (self.x,self.y))
            if self.direction == "down":
                screen.blit(AttackAnimation[3], (self.x,self.y))
            self.AtCount += 1
            if self.AtCount == 3:
                self.isAt = False
                self.AtCount = 0
                
        #Bolt
        for Bolt in self.Attacks:
            if Bolt.x < 1500 and Bolt.x > 0 and Bolt.y > 150 and Bolt.y < 800:
                if Bolt.direction == "left":
                    Bolt.x -= Bolt.speed
                elif Bolt.direction == "right":
                    Bolt.x += Bolt.speed
                elif Bolt.direction == "up" :
                    Bolt.y -= Bolt.speed
                elif Bolt.direction == "down" :
                    Bolt.y += Bolt.speed                
            else:
                self.Attacks.pop(self.Attacks.index(Bolt))
        for Bolt in self.Attacks:
            Bolt.draw(screen)
            
    def Attack(self):        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  
            if self.Cooldown == 0 and self.MP > 0 and self.direction != "":
                self.isAt = True
                self.MP -= 1
                self.Attacks.append(projectile(round(self.x + self.width //2), round(self.y + self.height//2), 15, (0,0,0), self.direction))
                self.Cooldown = 15