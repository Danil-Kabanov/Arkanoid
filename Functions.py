import pygame
import os
from sys import exit
from random import randint


# Выход из игры
def close_game(f):
    f.close()
    pygame.quit()
    exit()


# Функция для нахождения абсциссы указателя в данный момент.
def get_OX():
    return pygame.mouse.get_pos()[1]


# Функция для нахождения ординаты указателя в данный момент.
def get_OY():
    return pygame.mouse.get_pos()[1]


# Музыка для игры
def load_theme():
    music_theme = randint(1, 5)
    music = {1: "ErrorRate", 2: "Humdrum", 3: "Ictus", 4: "Plunge", 5: "Zigzag"}
    music_to_load = os.path.join("audio", "themes", f"Viscid_{music[music_theme]}.mp3")
    pygame.mixer.music.load(music_to_load)
    return music_to_load
