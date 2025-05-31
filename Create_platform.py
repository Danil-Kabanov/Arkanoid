from random import randint
from pygame.locals import *
from Functions import get_mouse_x
import pygame
import os


movemode = False


class Platform(pygame.sprite.Sprite):

    def __init__(self):  # Создание платформы
        super().__init__()
        self.width = 100
        self.height = 15
        self.image = pygame.image.load(os.path.join("images", "player", "playerframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = randint(0, 700)
        self.rect.y = self.screenheight - self.height - 5
        self.movemode = 0

    def update(self):  # Движение ракетки
        if pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]:
            if self.rect.y > 450:
                self.rect.y -= 2
        if pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]:
            if self.rect.y < 580:
                self.rect.y += 2
        # Управление платформой мышью
        self.rect.x = get_mouse_x()
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
