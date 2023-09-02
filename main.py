from play import *

SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("CRAZY PLANE")
icon = pygame.image.load('blue1.png')
pygame.display.set_icon(icon)


BG_withoutscale = pygame.image.load("backgroundmenu.png")
BG = pygame.transform.scale(BG_withoutscale, (WINDOW_WIDTH,WINDOW_HEIGHT))

#music button scaling
MB_w=pygame.image.load("musicbutton.png")
MB=pygame.transform.scale(MB_w,(90,90))     #(90,90)

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("decayfont.ttf", size)

def music():
    music = pygame.mixer.Sound('piratesbgm.mp3')
    if pygame.mixer.get_busy()==True:
        pygame.mixer.stop()
    else:
        music.play(-1)
def main_menu():

    pygame.init()
    while True:

        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("CRAZY PLANE",True, "#150330")
        MENU_RECT = MENU_TEXT.get_rect(center=(400,100))
        #RULE_TEXT = (pygame.font.Font("decayfont.ttf", 10)).render("PRESS SPACE TO JUMP IN GAME", True, "black")

        PLAY_BUTTON = Button(image=None, pos=(640//1.6, 350//1.5),
                             text_input="PLAY", font=get_font(55), base_color="black", hovering_color="white")
        MUSIC_BUTTON = Button(image=MB, pos=(650,280),
                                text_input="MUSIC", font=get_font(20), base_color="black", hovering_color="white")
        QUIT_BUTTON = Button(image=None, pos=(640//1.6, 550//1.5),
                             text_input="QUIT", font=get_font(55), base_color="black", hovering_color="white")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        #SCREEN.blit(RULE_TEXT,(280,440))

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
                if MUSIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                        music()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()




