from game import Game
import pygame

g = Game()
music = pygame.mixer.music.load("Sound\MenuTheme.wav")
pygame.mixer.music.play(-1)
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()