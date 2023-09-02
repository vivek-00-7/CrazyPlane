import sys,pygame,random
import time
from button import Button
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class  Game():
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('CRAZY PLANE')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('background.png').get_height()
        print(bg_height)
        self.scale_factor = WINDOW_HEIGHT / (bg_height)

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1300)

        # text

        self.score = 0
        self.start_offset = 0
        self.initial_time = 0
        self.score_count = 0
        self.RULE_TEXT = (pygame.font.Font("decayfont.ttf",10)).render("PRESS SPACE TO JUMP",True,"black")

        #restart button
        self.RESTART_BACK = Button(image=None, pos=(230, 400 // 1.5),
                                   text_input="RESTART",
                                   font=pygame.font.Font("decayfont.ttf",
                                                         30),
                                   base_color="Black", hovering_color="silver")
        #QUIT button
        self.QUIT_BACK =  Button(image=None, pos=(560, 400 // 1.5),
                                   text_input="QUIT",
                                   font=pygame.font.Font("decayfont.ttf",
                                                         30),
                                   base_color="Black", hovering_color="silver")

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) \
                or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            if self.score_count!=0:
                 self.score = 2*(pygame.time.get_ticks() - self.start_offset) // 1000
            else:
                self.score = 2*(pygame.time.get_ticks()-self.start_offset-self.initial_time) // 1000

            y = WINDOW_HEIGHT / 10
            self.font = pygame.font.SysFont('decayfont.ttf', 80)
            score_surf =self.font.render(str(self.score), True, "silver")
            score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
            self.display_surface.blit(score_surf, score_rect)

        else:
            y = WINDOW_HEIGHT / 7
            # display highscore:
            with open("highscore.txt", "r") as f1:
                data = f1.read()
            if self.score >= int(data):
              with open("highscore.txt","w") as f1:
                       f1.write(str(self.score))
            with open("highscore.txt","r") as f2:
                data1 = f2.read()
            self.font1 = pygame.font.SysFont('decayfont.ttf', 40)
            score_surf1 = self.font1.render(f"HIGHSCORE:{str(data1)}", True, "silver")
            score_rect1 = score_surf1.get_rect(midtop=(WINDOW_WIDTH / 2.1, y / 2.1))
            self.display_surface.blit(score_surf1, score_rect1)
            #display score
            SCORE_TEXT = pygame.font.SysFont('decayfont.ttf', 60)
            SCORE_TEXT_R = SCORE_TEXT.render(f"YOUR SCORE:{str(self.score)}", True, "silver")
            SCORE_RECT = SCORE_TEXT_R.get_rect(midtop=(WINDOW_WIDTH / 2.1, y))

            # display gameover
            GAMEOVER_TEXT = pygame.font.Font("decayfont.ttf", 45)
            GAMEOVER_TEXT_R = GAMEOVER_TEXT.render("GAME OVER!", True, "Black")
            GAMEOVER_RECT = GAMEOVER_TEXT_R.get_rect(center=(620 // 1.6, 260 // 1.5))
            SILVER_IMG = pygame.image.load("gameover.png")


            self.display_surface.blit(SILVER_IMG,(360,216))
            self.display_surface.blit(SCORE_TEXT_R, SCORE_RECT)
            self.display_surface.blit(GAMEOVER_TEXT_R, GAMEOVER_RECT)


    def run(self):
        last_time = time.time()
        self.initial_time = pygame.time.get_ticks()
        while True:
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            self.plane.jump()
                    else:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.RESTART_BACK.checkForInput(self.RESTART_MOUSE_POS):
                                self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                                self.active = True
                                self.start_offset = pygame.time.get_ticks()
                                self.score_count += 1
                            elif self.QUIT_BACK.checkForInput(self.QUIT_BACK_MOUSE_POS):
                                pygame.quit()
                                sys.exit()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            self.all_sprites.update(dt)
            self.display_score()

            if self.active:
                self.display_surface.blit(self.RULE_TEXT, (300,20))
                self.collisions()
            else:
                self.RESTART_MOUSE_POS = pygame.mouse.get_pos()
                self.RESTART_BACK.changeColor(self.RESTART_MOUSE_POS)
                self.RESTART_BACK.update(self.display_surface)
                self.QUIT_BACK_MOUSE_POS = pygame.mouse.get_pos()
                self.QUIT_BACK.changeColor(self.QUIT_BACK_MOUSE_POS)
                self.QUIT_BACK.update(self.display_surface)

            pygame.display.update()
            #self.clock.tick(FRAMERATE)




