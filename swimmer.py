import time

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self,x , y):
        super().__init__()
        self.player_swim_1 = pygame.image.load('level1bass1.png').convert_alpha()
        self.player_swim_2 = pygame.image.load('level1bass2.png').convert_alpha()
        self.player_respawn = pygame.image.load('respawn.png').convert_alpha()
        self.player_swim = [self.player_swim_1, self.player_swim_2]
        self.player_index = 0
        self.player_eat = pygame.image.load('level1bassEat.png').convert_alpha()
        self.lives = 3
        self.score = 0
        self.collision_time = -4000
        self.invincible = False

        self.image = self.player_swim[self.player_index]
        self.rect = self.image.get_rect(bottomleft = (x,y))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += 10
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -=10
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += 10

    def boundaries(self):
        if self.rect.x >= 900:
            self.rect.x = 900
        if self.rect.x <=0:
            self.rect.x = 0
        if self.rect.y <= 12:
            self.rect.y = 12
        if self.rect.y >= 400:
            self.rect.y = 400

    def animation_state(self):

            self.player_index += 0.1
            if self.player_index >= len(self.player_swim):
                self.player_index = 0
            self.image = self.player_swim[int(self.player_index)]


    def eat(self):
        self.image = self.player_eat

    def setlives(self):
        self.lives -= 1


    def display_lives(self):
        life1 = pygame.image.load('lillyLife.png').convert_alpha()
        life1_rect = life1.get_rect(center=(25, 25))
        life2 = pygame.image.load('lillyLife.png').convert_alpha()
        life2_rect = life2.get_rect(center = (55, 25))
        life3 = pygame.image.load('lillyLife.png').convert_alpha()
        life3_rect = life3.get_rect(center = (85, 25))
        lives = [life1, life2, life3]
        life_rects = [life1_rect, life2_rect, life3_rect]
        for i in range(self.lives):
            screen.blit(lives[i] , life_rects[i])


    def set_collision_time(self):
        self.collision_time = pygame.time.get_ticks()

    def test_respawn(self, curr_time):
        if (curr_time - self.collision_time) < 3000:
            self.invincible = True
            self.player_swim = [self.player_swim_1, self.player_respawn]
        else:
            self.invincible = False
            self.player_swim = [self.player_swim_1, self.player_swim_2]

    def set_score(self):
        self.score += randint(2,5)/10
        self.score = round(self.score, 2)
        return self.score


    def update(self):
        self.player_input()
        self.animation_state()
        self.boundaries()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()

        self.obstacle_type = obstacle_type

        if self.obstacle_type ==  'boss':
            boss_frame_1 = pygame.image.load('enemyBass1.png').convert_alpha()
            boss_frame_2 = pygame.image.load('enemyBass2.png').convert_alpha()
            self.frames = [boss_frame_1, boss_frame_2]
            y_pos = randint(150,450)


        elif self.obstacle_type == 'tree':
            tree_frame = pygame.image.load('Dead tree 2.png').convert_alpha()
            self.frames = [tree_frame]
            y_pos = 510

        elif self.obstacle_type == 'jb':
            jb_frame1 = pygame.image.load('johnBoat1.png').convert_alpha()
            jb_frame2 = pygame.image.load('johnBoat2.png').convert_alpha()
            self.frames = [jb_frame1 , jb_frame2]

            y_pos = 55

        else:
            spinner_frame1 = pygame.image.load('spinnerbait1.png').convert_alpha()
            spinner_frame2 = pygame.image.load('spinnerbait2.png').convert_alpha()
            self.frames = [spinner_frame1, spinner_frame2]
            y_pos = randint(25,300)

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1500, 1600), y_pos))

    def boss_eat(self):
        if self.obstacle_type == 'boss' :
            self.image = pygame.image.load('enemyBassEat.png').convert_alpha()

    def boss_follow(self, player_centery, player_x):
        if self.obstacle_type == 'boss' :
            if self.rect.x - player_x < 700 and self.rect.x > player_x:
                if self.rect.centery > player_centery:
                    self.rect.y -= 1
                elif self.rect.centery < player_centery:
                    self.rect.y += 1


    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        if self.obstacle_type == 'boss' :
            self.rect.x -= 7
        elif self.obstacle_type == 'tree':
            self.rect.x -= 5
        elif self.obstacle_type == 'jb':
            self.rect.x -= 1
        else:
            self.rect.x -= 8
        self.destroy()


    def destroy(self):
        if self.rect.x <= -500:
            self.kill()

class Food(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.move_speed = 0

        if type == 'bluegill':
            bluegill_frame_1 = pygame.image.load('Bluegill1.png').convert_alpha()
            bluegill_frame_2 = pygame.image.load('Bluegill2.png').convert_alpha()
            self.frames = [bluegill_frame_1, bluegill_frame_2]
            y_pos = randint(150, 450)
            self.move_speed = randint(6, 10)
        elif type == 'shiner':
            shiner_frame_1 = pygame.image.load('Shiner1.png').convert_alpha()
            shiner_frame_2 = pygame.image.load('Shiner2.png').convert_alpha()
            self.frames = [shiner_frame_1, shiner_frame_2]
            y_pos = randint(150, 450)
            self.move_speed = randint(6, 10)
        else:
            frog_frame_1 = pygame.image.load('Frog1.png').convert_alpha()
            frog_frame_2 = pygame.image.load('Frog2.png').convert_alpha()
            self.frames = [frog_frame_1, frog_frame_2]
            y_pos = randint(25, 75)
            self.move_speed = 4



        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1200, 1300), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.move_speed
        self.destroy()
        self.rectleft()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def rectleft(self):
        return self.rect.left

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.big_boss_frame1 = pygame.image.load('bossBass1.png').convert_alpha()
        self.big_boss_frame2 = pygame.image.load('bossBass2.png').convert_alpha()
        self.frames = [self.big_boss_frame1, self.big_boss_frame2]

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (2000, 250))
        self.attack = False

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def boss_movement(self, player_y):

        if self.rect.left > 610:
            self.rect.left -= 2
        elif self.rect.left < 600 and not self.attack:
            self.rect.left += 8
        elif self.rect.centery > player_y + 5 and not self.attack:
            self.rect.y -= 5
        elif self.rect.centery < player_y - 5 and not self.attack:
            self.rect.y += 5
        else:
            self.attack = True
            self.boss_attack()

    def boss_attack(self):
        if self.attack:
            self.rect.left -= 15
            self.frames = [pygame.image.load('bossBassEat.png').convert_alpha()]

        if self.rect.left <= 60:
            self.frames = [self.big_boss_frame1, self.big_boss_frame2]
            self.attack = False

class Baby(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        baby_frame_1 = pygame.image.load('babyBass.png').convert_alpha()

        self.frames = [baby_frame_1]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.movement_y = randint(260,300)
        self.og_y = randint(75, 310)
        self.finalx = randint(610, 800)
        self.rect = self.image.get_rect(center = (randint(2650,2750), self.og_y ))
        self.og_move = 1.3

    def baby_movement(self):
        self.rect.y -= self.og_move

        if self.rect.y <= self.movement_y:
            self.og_move -= .2
        else:
            self.og_move += .2


    def baby_place(self):
        if self.rect.x >= self.finalx:
            self.rect.x -= 5



            


def collision_sprite():
    past_time = 0
    if pygame.sprite.spritecollide(player.sprite, food_group, True):
        main_player.set_score()
        return True

    elif pygame.sprite.spritecollide(player.sprite, obstacle_group or boss, False):
        if main_player.invincible is False:
            main_player.set_collision_time()
            main_player.rect.center = (150, 250)
            main_player.setlives()

            if main_player.lives <= 0:
                obstacle_group.empty()
                food_group.empty()
                return False
            return True
        else:
            return True

    elif pygame.sprite.spritecollide(player.sprite, baby_group, True):
        return True
    else:
        invincible_group.empty()
        return True


def display_score(run):
    # Score

    if run:
        current_score = main_player.score
        scale_pic = pygame.image.load('scale.png').convert_alpha()
        scale_pic_rect = scale_pic.get_rect(center=(900, 50))
        screen.blit(scale_pic, scale_pic_rect)
        score_font = pygame.font.Font(None, 50)
        score_message = score_font.render(f'{current_score}', False, (255, 255, 255))
        score_message_rect = score_message.get_rect(center=(900, 50))
        screen.blit(score_message, score_message_rect)
    else:
        current_score = 0

# Timer
game_ended = 0




pygame.init()
screen = pygame.display.set_mode((1000,500), pygame.RESIZABLE)
pygame.display.set_caption("Swimmer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_active = True
start_time = 0
score = 0


# Groups
main_player = Player(250,600)
player = pygame.sprite.GroupSingle()
player.add(main_player)

# Game Over
game_over = pygame.image.load('gameOver.png').convert_alpha()
game_over_rect  = game_over.get_rect(bottomleft = (0 , 500))
main_boss = Boss()
boss = pygame.sprite.GroupSingle()
boss.add(main_boss)

invincible_group = pygame.sprite.GroupSingle()

obstacle_group = pygame.sprite.Group()

food_group = pygame.sprite.Group()

baby_group = pygame.sprite.Group()

for i in range(10):
    baby_group.add(Baby())




background1 = pygame.image.load('bg1.png').convert_alpha()
background_rect = background1.get_rect(topleft = (0,0))
background_rect2 = background1.get_rect(topleft = (1000,0))

foreground1 = pygame.image.load('fg1.png').convert_alpha()
fg1_rect = foreground1.get_rect(bottomright = (0,500))
fg2_rect = foreground1.get_rect(bottomright = (1000,500))
fg3_rect = foreground1.get_rect(bottomright = (2000,500))
boss_fg = pygame.image.load('bossFg.png').convert_alpha()
boss_fg_rect = boss_fg.get_rect(bottomleft = (1500,500))




end_battle = False

count = 0
# Timer

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer and pygame.time.get_ticks() - game_ended < 20000:
                obstacle_group.add(Obstacle(choice(['boss', 'tree', 'spinner', 'spinner', 'boss'])))
                food_group.add(Food(choice(['bluegill', 'shiner', 'frog'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                game_active = True

    if game_active:


        screen.blit(background1, background_rect)
        screen.blit(background1, background_rect2)

        baby_group.draw(screen)

        for baby in baby_group:
            baby.baby_movement()


        if not end_battle:
            screen.blit(foreground1, fg2_rect)
            screen.blit(foreground1, fg1_rect)
            screen.blit(foreground1, fg3_rect)

            background_rect.left -= 1
            background_rect2.left -= 1
            fg1_rect.left -= 5
            fg2_rect.left -= 5
            fg3_rect.left -= 5

            if background_rect.left <= -1000:
                background_rect.left = background_rect2.right

            if background_rect2.left <= -1000:
                background_rect2.left = background_rect.right

            if fg1_rect.left <= -1000:
                fg1_rect.left = fg3_rect.right

            if fg2_rect.left <= -1000:
                fg2_rect.left = fg1_rect.right

            if fg3_rect.left <= -1000:
                fg3_rect.left = fg2_rect.right
                count += 1
                print(count)


        if count == 2:
            boss_fg_rect.left = fg3_rect.left
            screen.blit(boss_fg, boss_fg_rect)
            boss_fg_rect.left -= 5
            for baby in baby_group:
                baby.baby_place()

            if main_player.rect.right >= 818:
                main_player.rect.right = 818

            if boss_fg_rect.right <= 1000:
                boss_fg_rect.right = 1000
                fg2_rect.right = fg3_rect.left
                end_battle = True

            main_boss.animation_state()
            main_boss.boss_movement(main_player.rect.y)
            # main_boss.boss_attack(main_player.rect.y)



        main_player.test_respawn(pygame.time.get_ticks())

        main_player.display_lives()

        player.draw(screen)
        player.update()

        boss.draw(screen)

        invincible_group.draw(screen)
        invincible_group.update()

        display_score(True)

        obstacle_group.draw(screen)
        obstacle_group.update()

        food_group.draw(screen)
        food_group.update()


        for food in food_group:
            if (food.rect.left - 100) <= main_player.rect.right and abs(food.rect.top - main_player.rect.centery) < 75:
                main_player.eat()

        for baby in baby_group:
            if (baby.rect.left - 100) <= main_player.rect.right and abs(baby.rect.top - main_player.rect.centery) < 75:
                main_player.eat()

        for obstacle in obstacle_group:
            if (obstacle.rect.left - 100) <= main_player.rect.right and abs(obstacle.rect.centery - main_player.rect.centery) < 75 :
                obstacle.boss_eat()

            obstacle.boss_follow(main_player.rect.centery, main_player.rect.x)




        game_active = collision_sprite()
    else:
        pygame.display.update()
        screen.blit(game_over, game_over_rect)

        display_score(False)
        main_player.score = 0
        main_player.lives = 3
        main_player.collision_time = -4000
        end_battle = False
        main_boss.rect.left = 2000
        main_boss.rect.y = 250
        count = 0
        boss_fg_rect.left = 2000
        game_ended = pygame.time.get_ticks()





    pygame.display.update()
    clock.tick(60)