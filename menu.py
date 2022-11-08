import pygame

background = pygame.image.load(r'imgMenu\Background.png')
        
def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2 + 200, self.game.DISPLAY_H / 2 - 200
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        #self.game.draw_text('*', 30, self.cursor_rect.x - 10, self.cursor_rect.y)
        pygame.draw.rect(self.game.display, (0,0,0), (self.cursor_rect.x, self.cursor_rect.y - 20, 220, 40), 2)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 40
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80
        self.tutorialx, self.tutorialy = self.mid_w, self.mid_h + 120
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 160
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(background,(0,0))
            self.game.draw_text('Main Menu', 40, self.game.DISPLAY_W / 2 + 200, self.game.DISPLAY_H / 2 - 20 - 200)
            self.game.draw_text("Start Game", 30, self.startx, self.starty)
            self.game.draw_text("Options", 30, self.optionsx, self.optionsy)
            self.game.draw_text("Tutorial", 30, self.tutorialx, self.tutorialy)            
            self.game.draw_text("Credits", 30, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Tutorial'
            elif self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Tutorial'
            elif self.state == 'Tutorial':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                run("Main.py")
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Tutorial':
                self.game.curr_menu = self.game.tutorial
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.game.DISPLAY_W/2-20, self.game.DISPLAY_H/2-40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        self.volume = 1;
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(background,(0,0))
            self.game.draw_text('Options', 40, self.game.DISPLAY_W/2-20, self.game.DISPLAY_H/2 - 90)
            self.game.draw_text("Volume", 25, self.volx, self.voly)
            pygame.draw.rect(self.game.display,(0,0,0),(self.cursor_rect.x-135, self.cursor_rect.y+30,500,30),2)
            pygame.draw.rect(self.game.display,(100,100,100),(self.cursor_rect.x-135+2, self.cursor_rect.y+30+2,500*self.volume-4,30-4))
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.volume <= 0.9: self.volume += 0.1
        if keys[pygame.K_LEFT] and self.volume >= 0.1: self.volume -= 0.1 

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(background,(0,0))
            self.game.draw_text('Credits', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 110)
            self.game.draw_text('Made by Zunzun & AnkDepTrym', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40)
            self.blit_screen()

class TutorialMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.blit(pygame.image.load(r"imgMenu\Tutorial.png"),(0,0))
            self.blit_screen()