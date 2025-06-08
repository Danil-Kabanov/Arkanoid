from random import randint
from pygame.locals import *
import pygame
import os


movemode = True


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

    def update(self):  # Движение платформы
        if pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]:
            if self.rect.y > 450:
                self.rect.y -= 2
        if pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]:
            if self.rect.y < 580:
                self.rect.y += 2
        if movemode:  # Движение ракетки с помощью клавиатуры
            if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
                if self.rect.x >= 5:
                    self.rect.x -= 5
            if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                if self.rect.x <= 695:
                    self.rect.x += 5
