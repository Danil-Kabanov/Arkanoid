from math import radians, sin, cos
import pygame
import os


pygame.init()
bounce = pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav"))


class Ball(pygame.sprite.Sprite):
    speed = 0
    x = 0
    y = 0
    directions = [120, 140, 160, 180, 200, 220, 240]
    direction = 0
    width = 20
    height = 20

    def __init__(self):  # Создание мячика
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "ball", "ballframe1.png"))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, d):  # Горизонтальный отскок мячика
        self.direction = (180 - self.direction) % 360
        self.direction -= d
        bounce.play()

    def vertical_bounce(self):  # Вертикальный отскок мячика
        self.direction = (360 - self.direction) % 360
        bounce.play()

    def update(self):  # Движение мячика
        if self.direction < 0:
            self.direction += 360
        if self.direction >= 360:
            self.direction -= 360
        direction_radians = radians(self.direction)
        self.x += self.speed * sin(direction_radians)
        self.y -= self.speed * cos(direction_radians)
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
        if self.x <= 0:
            self.vertical_bounce()
            self.x = 1
        if self.x > self.screenwidth - self.width:
            self.vertical_bounce()
            self.x = self.screenwidth - self.width - 1
        if self.y > 600:
            return True
        else:
            return False
