import pygame as pyg
import GameFunctions as gf
from Mario import *
from Koopa import RegularKoopa
from enemies import Goomba
import os
import sys
import time
from  Levels import *
import constants

pyg.init()
screen = pyg.display.set_mode((960,470),pyg.RESIZABLE)
screen.fill(constants.bg_color)

mario = LittleMario(screen)
level = Level(screen)
level.create_rects()
level.create_enemies()
goomba = Goomba(screen=screen)
enemies = [goomba]
koopa = RegularKoopa(screen=screen)
koopas = [koopa]

while True:
    gf.check_events(screen = screen, mario = mario)
    gf.update_mario(mario=mario)
    gf.update_koopas(koopas=koopas)
    gf.update_enemies(enemies=enemies)
    gf.updateLevel(level=level, mario =mario)
    gf.check_collisiontype(mario=mario, level=level)
    gf.check_collisiontype_goomba(level=level, enemies=enemies)
    gf.check_collisiontype_koopa(level=level, koopas=koopas)
    gf.check_mario_enemy_collision(screen=screen, mario=mario, enemies=enemies, koopas=koopas)
    gf.update_screen(screen = screen, mario = mario, level = level, koopas=koopas, enemies=enemies)

