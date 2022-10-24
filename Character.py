import pygame, sys
from pygame.locals import *
from Projectile import *
pygame.mixer.init()

clone = pygame.image.load("Img\Clone.png")
idle = [pygame.image.load("Img\Idle_1.png"),pygame.image.load("Img\Idle_2.png"),pygame.image.load("Img\Idle_1.png"),pygame.image.load("Img\Idle_4.png")]
walkDown = [pygame.image.load("Img\WalkDown_1.png"),pygame.image.load("Img\WalkDown_2.png")]
walkUp = [pygame.image.load("Img\WalkUp_1.png"),pygame.image.load("Img\WalkUp_2.png")]
walkRight = [pygame.image.load("Img\WalkRight_1.png"),pygame.image.load("Img\WalkRight_2.png"), pygame.image.load("Img\WalkRight_3.png"), pygame.image.load("Img\WalkRight_1.png")]
walkLeft = [pygame.image.load("Img\WalkLeft_1.png"),pygame.image.load("Img\WalkLeft_2.png"), pygame.image.load("Img\WalkLeft_3.png"), pygame.image.load("Img\WalkLeft_1.png")]
ChaImg = pygame.image.load('Img\Idle_1.png')
AttackAnimation = [pygame.image.load("Img\AttackLeft.png"),pygame.image.load("Img\AttackRight.png"),pygame.image.load("Img\AttackUp.png"),pygame.image.load("Img\AttackDown.png")]
Player_getHit = pygame.image.load("Img\Player_getHit.png")
ShieldImg = pygame.image.load("Img\shield.png")

Sound_At = pygame.mixer.Sound("Sound\main_attack.wav")
Sound_Move = pygame.mixer.Sound("Sound\main_move_glass.wav")
Sound_Move.set_volume(0.3)
Sound_At.set_volume(0.1)

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
        self.hitBox = pygame.Rect(self.x + 2, self.y, width - 4, height)
        self.GetHit = 0
        # dash
        self.dashCooldown = 0
        self.dashDirection = "left"
    
    def move(self):
        keys = pygame.key.get_pressed()
        self.walk = False
        if keys[pygame.K_a] and self.dashCooldown == 0:
            self.dash()
        elif self.dashCooldown <= 20:
            if keys[pygame.K_d]:  
                if self.Cooldown == 0 and self.MP > 0 and self.direction != "":
                    self.isAt = True
                    self.MP -= 1
                    self.Attacks.append(projectile(round(self.x + self.width //2), round(self.y + self.height//2), 15, (50,50,50), self.direction))
                    self.Cooldown = 15
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
        
        
        #Heal bar
        drawBar(screen)
        pygame.draw.rect(screen, (50,50,50), (0, 3, self.HP * 2 , 20))
        pygame.draw.rect(screen, (128,128,128), (0, 25, self.MP * 2 , 20))
        
        
        # Character animation
        if self.dashCooldown <= 20:
            screen.blit(clone, (self.clone_x, self.clone_y))
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
                else:
                    if self.direction == "down":
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
                    Sound_Move.play()
            else:
                Sound_At.play()
                pygame.mixer.init()
                if self.direction == "left":
                    screen.blit(AttackAnimation[0], (self.x,self.y))
                if self.direction == "right":
                    screen.blit(AttackAnimation[1], (self.x,self.y))
                if self.direction == "up":
                    screen.blit(AttackAnimation[2], (self.x,self.y))
                if self.direction == "down":
                    screen.blit(AttackAnimation[3], (self.x,self.y))
                self.AtCount += 1
                
                if self.AtCount == 4:
                    self.isAt = False
                    self.AtCount = 0
        else:
            if self.dashDirection == "left":
               self.x -= self.speed * 3
               self.clone_x = self.x
               screen.blit(clone, (self.clone_x, self.clone_y))
               screen.blit(walkLeft[2], (self.x, self.y)) 
            elif self.dashDirection == "right":
               self.x += self.speed * 3
               self.clone_x = self.x
               screen.blit(clone, (self.clone_x, self.clone_y))
               screen.blit(walkRight[2], (self.x, self.y))
            elif self.dashDirection == "up":
               self.y -= self.speed * 3
               self.clone_y = self.y + 39
               screen.blit(clone, (self.clone_x, self.clone_y))
               screen.blit(walkUp[1], (self.x, self.y))
            elif self.dashDirection == "down":
               self.y += self.speed * 3
               self.clone_y = self.y + 39
               screen.blit(clone, (self.clone_x, self.clone_y))
               screen.blit(walkDown[1], (self.x, self.y))
        
        if self.GetHit > 0: 
            if(self.GetHit % 20 == 0): screen.blit(Player_getHit, (self.x, self.y))
            self.GetHit -= 1
        
        self.hitBox = pygame.Rect(self.x + 5, self.y, width - 10, height)
        pygame.draw.rect(screen, (255,0,0), self.hitBox, 2)
         
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
        
        ScreenLimit(self)
        self.clone_x = self.x
        self.clone_y = self.y + 39
        if self.dashCooldown > 0: self.dashCooldown -= 1
            
    def Attack(self):        
        keys = pygame.key.get_pressed()
        
        
    def getHit(self, dame):
        if(self.GetHit == 0):
            self.HP -= dame
            self.GetHit = 40
            
    def dash(self):
        if self.dashCooldown == 0:
            self.dashCooldown = 26
            self.dashDirection = self.direction