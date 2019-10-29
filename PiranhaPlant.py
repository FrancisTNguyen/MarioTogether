import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet
from Timer import Timer


class PiranhaPlant(Sprite):
    def __init__(self, screen, pop_list):
        super(PiranhaPlant, self).__init__()

        # get screen dimensions
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # list to hold animation images
        self.pop_list = pop_list

        # Timer class to animate sprites
        self.animation = Timer(frames=self.pop_list)

        # get the rect of the image
        self.imagePop = self.animation.imagerect()
        self.rect = self.imagePop.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store objects exact position
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # movement flags
        self.going_up = False
        self.going_down = False
        self.direction = 1

    def blitme(self):
        if self.going_up or self.going_down:
            self.screen.blit(self.imagePop, self.rect)

    def update(self):
        self.y += (1 * self.direction)
        # (2 * self.direction)
        self.rect.y = self.y

        if self.rect.top >= self.screen_rect.centery + 250:
            self.direction *= -1
            self.going_up = False
            self.going_down = True
        if self.rect.bottom <= self.screen_rect.centery - 250:
            self.direction *= -1
            self.going_up = True
            self.going_down = False
        if self.going_down or self.going_up:
            self.imagePop = self.pop_list[self.animation.frame_index()]


class UnderGroundPiranha(PiranhaPlant):
    def __init__(self, screen):
        sprite_sheet = SpriteSheet("Images/enemies.png")
        self.under_piranha = []
        imagePop = pygame.transform.scale(sprite_sheet.get_image(390, 60, 19, 25), (32, 32))
        self.under_piranha.append(imagePop)
        imagePop = pygame.transform.scale(sprite_sheet.get_image(420, 60, 19, 25), (32, 32))
        self.under_piranha.append(imagePop)
        super().__init__(screen=screen, pop_list=self.under_piranha)