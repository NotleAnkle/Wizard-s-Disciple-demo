from game import Game
import pygame

g = Game()
icon = pygame.image.load("Img\Icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Wizard's disciple") 
music = pygame.mixer.music.load("Sound\MenuTheme.wav")
pygame.mixer.music.play(-1)
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()