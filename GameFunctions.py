import pygame, sys
import constants
from pygame.locals import *
from Koopa import RegularKoopa
from enemies import Goomba
from PiranhaPlant import UnderGroundPiranha
from Timer import Timer


def check_events(mario, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(event=event, mario=mario)
        elif event.type == pygame.KEYUP:
            check_keyup(event=event, mario=mario)


def check_keydown(event, mario):
    """ Respond to keypresses  """
    # Movement flags set to true
    if event.key == pygame.K_RIGHT or event.key == K_d:
        mario.moving_right = True
        mario.facing_right = True
        mario.facing_left = False
    elif event.key == pygame.K_LEFT or event.key == K_a:
        mario.moving_left = True
        mario.facing_left = True
        mario.facing_right = False
    elif event.key == pygame.K_UP or event.key == K_w or event.key == pygame.K_SPACE:
        mario.is_jumping = True
        mario.jump()
    elif event.key == pygame.K_DOWN or event.key == K_s:
        mario.crouch = True
        pass
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup(event, mario):
    """ Respond to key releases """
    if event.key == pygame.K_RIGHT or event.key == K_d:
        mario.moving_right = False
        mario.facing_right = True
    elif event.key == pygame.K_LEFT or event.key == K_a:
        mario.moving_left = False
        mario.facing_left = True
    elif event.key == pygame.K_UP or event.key == K_w or event.key == pygame.K_SPACE:
        mario.is_jumping = True
    elif event.key == pygame.K_DOWN or event.key == K_s:
        mario.crouch = False
        pass


def check_koopa_enemy_collision(enemies, koopas):
    for koopa in koopas:
        for enemy in enemies:
            if koopa.shell_mode_moving:
                if pygame.sprite.collide_rect(enemy, koopa):
                    enemy.died = True


def check_mario_enemy_collision(screen, mario, enemies, koopas, piranhas):
    for enemy in enemies:
        #if pygame.sprite.collide_rect(mario, enemy):
        if mario.rect.colliderect(enemy):
            # base statement, if mario jumps on top of enemy, kills them
            if mario.rect.bottom > enemy.rect.top - 5:
                enemy.squashed = True
                mario.jump()
                enemies.remove(enemy)
            # mario touches enemy
            elif mario.rect.right >= enemy.rect.left and not mario.invincible:
                if mario.break_brick:
                    mario.become_small()
                    break
                # mario death, reset level
                # reset to beginning of level
                else:
                    pass
                    # mario.death_animation()
                    # enemies.clear()
                    # create_goomba(screen=screen,enemies=enemies)
                    # mario.reset_level()

    for piranha in piranhas:
        if pygame.sprite.collide_rect(mario, piranha):
            print("Piranha hit Mario")

    for koopa in koopas:
        if mario.rect.colliderect(koopa):
            print("hi")
            if mario.rect.bottom > koopa.rect.top - 5:
                mario.jump()
                if koopa.shell_mode:
                    koopa.shell_mode = False
                    koopa.shell_mode_moving = True
                elif koopa.shell_mode_moving:
                    koopa.shell_mode = True
                    koopa.shell_mode_moving = False
                elif not koopa.shell_mode and not koopa.shell_mode_moving:
                    koopa.shell_mode = True
                    koopa.shell_mode_moving = False
            elif mario.rect.right >= koopa.rect.left and not mario.invincible and koopa.shell_mode_moving:
                if mario.break_brick:
                    mario.become_small()
                    break
                else:
                    print("died")
                    mario.death_animation()
                    enemies.clear()
                    create_koopa(screen=screen, koopas=koopas)
                    mario.reset_level()
            if mario.rect.bottom > koopa.rect.top + 5 and mario.center > koopa.middle_x and koopa.shell_mode:
                mario.jump
                koopa.shell_mode = False
                koopa.direction = -1
                koopa.shell_mode_moving = True
            elif mario.rect.bottom > koopa.rect.top - 5 and mario.center < koopa.middle_x and koopa.shell_mode:
                mario.jump()
                koopa.shell_mode = False
                koopa.direction = 1
                koopa.shell_mode_moving = True
            # if mario.rect.bottom > koopa.rect.top - 5 and koopa.shell_mode_moving:
                # mario.jump()
                # koopa.shell_mode_moving = False
                # koopa.direction = 0
                # koopa.shell_mode = True


def check_mario_item_collision(screen, mario, items):
    for item in items:
        if pygame.sprite.collide_rect(mario, item):
            # make little mario into super mario
            mario.become_big()
            items.remove(item)


def create_goomba(screen, enemies):
    # create instance of Goomba class
    goomba = Goomba(screen=screen)
    enemies.append(goomba)


def create_koopa(screen, koopas):
    koopa = RegularKoopa(screen=screen)
    koopas.append(koopa)


def create_piranha(screen, piranhas):
    piranha = UnderGroundPiranha(screen=screen)
    piranhas.append(piranha)

def check_collisiontype_goomba(level, enemies):
    for blocks in level.environment:
        for enemy in enemies:
            if (pygame.sprite.collide_rect(enemy, blocks)):
                # floor
                if str(type(blocks)) == "<class 'Brick.Floor'>" and enemy.rect.bottom >= blocks.rect.top:
                    enemy.floor = True
                    enemy.rect.y = blocks.rect.y - 32
                # sides
                if str(type(blocks)) == "<class 'Brick.Pipe'>" \
                        and (enemy.rect.left <= blocks.rect.right or enemy.rect.right >= blocks.rect.left) \
                        and enemy.rect.bottom > blocks.rect.top \
                        and enemy.rect.top > blocks.rect.top - 16:
                    if enemy.rect.right >= blocks.rect.left \
                            and not enemy.obstacleL \
                            and enemy.rect.left < blocks.rect.left:
                        enemy.rect.right = blocks.rect.left - 1
                        enemy.obstacleR = True
                    else:
                        enemy.obstacleR = False
                    if enemy.rect.left <= enemy.rect.right \
                            and not enemy.obstacleR \
                            and enemy.rect.right > blocks.rect.right:
                        enemy.rect.left = blocks.rect.right + 1
                        enemy.obstacleL = True
                    else:
                        enemy.obstacleL = False
                else:
                    enemy.obstacleR = False
                    enemy.obstacleL = False
                if enemy.obstacleR or enemy.obstacleL:
                    print("im colliding")
                # top of pipe
                if str(type(blocks)) == "<class 'Brick.Pipe'>" \
                        and (enemy.rect.left < blocks.rect.right - 5 and enemy.rect.right > blocks.rect.left + 5) \
                        and enemy.rect.bottom > blocks.rect.top - 32 \
                        and not enemy.obstacleL and not enemy.obstacleR:
                    enemy.floor = True
                    enemy.rect.y = blocks.rect.y - 32

            # bounds
            if enemy.rect.left < 0:
                enemy.obstacleL = True
                enemy.rect.left = 0

def check_collisiontype_koopa(level, koopas):
    for blocks in level.environment:
        for koopa in koopas:
            if (pygame.sprite.collide_rect(koopa, blocks)):
                # floor
                if str(type(blocks)) == "<class 'Brick.Floor'>" and koopa.rect.bottom >= blocks.rect.top:
                    koopa.floor = True
                    koopa.rect.y = blocks.rect.y - 32
                # sides
                if str(type(blocks)) == "<class 'Brick.Pipe'>" \
                        and (koopa.rect.left <= blocks.rect.right or koopa.rect.right >= blocks.rect.left) \
                        and koopa.rect.bottom > blocks.rect.top \
                        and koopa.rect.top > blocks.rect.top - 16:
                    if koopa.rect.right >= blocks.rect.left \
                            and not koopa.obstacleL \
                            and koopa.rect.left < blocks.rect.left:
                        koopa.rect.right = blocks.rect.left - 1
                        koopa.obstacleR = True
                    else:
                        koopa.obstacleR = False
                    if koopa.rect.left <= blocks.rect.right \
                            and not koopa.obstacleR \
                            and koopa.rect.right > blocks.rect.right:
                        koopa.rect.left = blocks.rect.right + 1
                        koopa.obstacleL = True
                    else:
                        koopa.obstacleL = False
                else:
                    koopa.obstacleR = False
                    koopa.obstacleL = False
                if koopa.obstacleR or koopa.obstacleL:
                    print("im colliding")
                # top of pipe
                if str(type(blocks)) == "<class 'Brick.Pipe'>" \
                        and (koopa.rect.left < blocks.rect.right - 5 and koopa.rect.right > blocks.rect.left + 5) \
                        and koopa.rect.bottom > blocks.rect.top - 32 \
                        and not koopa.obstacleL and not koopa.obstacleR:
                    koopa.floor = True
                    koopa.rect.y = blocks.rect.y - 32

            # bounds
            if koopa.rect.left < 0:
                koopa.obstacleL = True
                koopa.rect.left = 0

def edge_koopa_collision(koopas):
    for koopa in koopas:
        if koopa.rect.x <= 0:
            koopas.remove(koopa)


def edge_goomba_collision(enemies):
    for enemy in enemies:
        if enemy.rect.x <= 0:
            enemies.remove(enemy)


def check_collisiontype(level, mario):
    for blocks in level.environment:
        if (pygame.sprite.collide_rect(mario, blocks)):
            #floor
            if str(type(blocks)) == "<class 'Brick.Floor'>" and mario.rect.bottom >= blocks.rect.top:
                mario.floor=True
                mario.rect.y= blocks.rect.y - 32
            #sides
            if str(type(blocks)) == "<class 'Brick.Pipe'>" \
                    and (mario.rect.left <= blocks.rect.right or mario.rect.right >= blocks.rect.left) \
                    and mario.rect.bottom > blocks.rect.top\
                    and mario.rect.top > blocks.rect.top-16:
                if mario.rect.right >= blocks.rect.left \
                        and not mario.obstacleL\
                        and mario.rect.left < blocks.rect.left:
                    mario.rect.right = blocks.rect.left -1
                    mario.obstacleR = True
                else:
                    mario.obstacleR = False
                if mario.rect.left <= blocks.rect.right \
                    and not mario.obstacleR\
                    and mario.rect.right > blocks.rect.right:
                    mario.rect.left = blocks.rect.right + 1
                    mario.obstacleL = True
                else:
                    mario.obstacleL = False
            else:
                mario.obstacleR = False
                mario.obstacleL = False
            if mario.obstacleR or mario.obstacleL:
                print("im colliding")
            #top of pipe
            if str(type(blocks)) == "<class 'Brick.Pipe'>" \
                    and (mario.rect.left < blocks.rect.right-5 and mario.rect.right > blocks.rect.left+5) \
                    and mario.rect.bottom > blocks.rect.top-32\
                    and not mario.obstacleL and not mario.obstacleR:
                mario.floor = True
                mario.rect.y= blocks.rect.y - 32

        #bounds
        if mario.rect.left < 0:
            mario.obstacleL = True
            mario.rect.left = 0

def updateLevel(level, mario):
    level.camera(mario)
    level.update()

def update_mario(mario):
    mario.update()

def update_enemies(enemies, level):
    for enemy in enemies:
        enemy.update(level)

def update_koopas(koopas, level):
    for koopa in koopas:
        koopa.update(level)

def update_piranhas(piranhas):
    for piranha in piranhas:
        piranha.update()

def update_items(items):
    for item in items:
        item.update()

def update_screen(screen, mario, level, koopas, enemies, piranhas):
    screen.fill(constants.bg_color)
    level.blitme()
    for koopa in koopas:
        koopa.blitme()
    for enemy in enemies:
        enemy.blitme()
    for piranha in piranhas:
        piranha.blitme()
    mario.blitme()
    pygame.display.flip()
