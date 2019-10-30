import pygame as pyg
import GameFunctions as gf
from Mario import *
from Koopa import RegularKoopa
from enemies import Goomba
from PiranhaPlant import UnderGroundPiranha
import os
import sys
import time
from Levels import *
import constants

pyg.init()
screen = pyg.display.set_mode((960,470),pyg.RESIZABLE)
screen.fill(constants.bg_color)

mario = LittleMario(screen)
level = Level(screen)
level.create_rects()
# level.create_enemies()
goomba = Goomba(screen=screen)
goomba2 = Goomba(screen=screen)
goomba3 = Goomba(screen=screen)
goomba4 = Goomba(screen=screen)
goomba5 = Goomba(screen=screen)
goomba6 = Goomba(screen=screen)
goomba2.x = 1100
goomba3.x = 1500
goomba4.x = 1550
goomba5.x = 1750
goomba6.x = 1800
enemies = [goomba, goomba2, goomba3, goomba4, goomba5, goomba6]
koopa = RegularKoopa(screen=screen)
koopa2 = RegularKoopa(screen=screen)
koopa.middle_x = 700
koopa2.middle_x = 1000
koopas = [koopa, koopa2]
piranha = UnderGroundPiranha(screen=screen)
piranhas = []

while True:
    gf.check_events(screen = screen, mario = mario)
    gf.update_mario(mario=mario)
    gf.updateLevel(level=level, mario =mario)
    gf.update_koopas(koopas=koopas, level = level)
    gf.update_enemies(enemies=enemies, level = level)
    gf.update_piranhas(piranhas=piranhas)
    gf.check_collisiontype(mario=mario, level=level)
    gf.check_collisiontype_goomba(level=level, enemies=enemies)
    gf.check_collisiontype_koopa(level=level, koopas=koopas)
    gf.edge_koopa_collision(koopas=koopas)
    gf.edge_goomba_collision(enemies=enemies)
    gf.check_koopa_enemy_collision(enemies=enemies, koopas=koopas)
    gf.check_mario_enemy_collision(screen=screen, mario=mario, enemies=enemies, koopas=koopas, piranhas=piranhas)
    gf.update_screen(screen = screen, mario = mario, level = level, koopas=koopas, enemies=enemies, piranhas=piranhas)

