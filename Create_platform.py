import pygame
import os
import random
from pygame.locals import *


movemode = False


# Это платформа
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.image.load(os.path.join("images", "player", "playerframe1.png"))

        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = random.randint(0, 700)
        self.rect.y = self.screenheight - self.height - 5
        self.movemode = 0

    # Движение плотформы
    def update(self):
        if pygame.key.get_pressed()[K_UP]:
            if self.rect.y > 450:
                self.rect.y -= 2
        if pygame.key.get_pressed()[K_DOWN]:
            if self.rect.y < 580:
                self.rect.y += 2
        if movemode:
            if pygame.key.get_pressed()[K_LEFT]:
                if self.rect.x >= 5:
                    self.rect.x -= 5
            if pygame.key.get_pressed()[K_RIGHT]:
                if self.rect.x <= 695:
                    self.rect.x += 5
        else:
            self.rect.x = pygame.mouse.get_pos()[0]
            if self.rect.x > self.screenwidth - self.width:
                self.rect.x = self.screenwidth - self.width
