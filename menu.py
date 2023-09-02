import pygame
import sys
import time
from button import Button
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from play import Game

#actual menu bar

pygame.init()

SCREEN = pygame.display.set_mode((1280//1.6, 720//1.5))
pygame.display.set_caption("Menu")

BG_withoutscale = pygame.image.load("background.png")
BG = pygame.transform.scale(BG_withoutscale, (1280//1.6,720//1.5))

#music button scaling
MB_w=pygame.image.load("musicbutton.png")
MB=pygame.transform.scale(MB_w,(90,90))

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("decayfont.ttf", size)

def music():
    music = pygame.mixer.Sound('gamebgm.wav')
    if pygame.mixer.get_busy()==True:
        pygame.mixer.stop()
    else:
        music.play(-1)
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("CRAZY PLANE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640//1.6, 150//1.5))

        PLAY_BUTTON = Button(image=None, pos=(640//1.6, 350//1.5),
                             text_input="PLAY", font=get_font(55), base_color="black", hovering_color="#b68f40")
        MUSIC_BUTTON = Button(image=MB, pos=(650,280),
                                text_input="MUSIC", font=get_font(20), base_color="black", hovering_color="#b68f40")
        QUIT_BUTTON = Button(image=None, pos=(640//1.6, 550//1.5),
                             text_input="QUIT", font=get_font(55), base_color="black", hovering_color="#b68f40")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, MUSIC_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game = Game()
                    game.run()
                    restart()
                if MUSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                        music()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()






