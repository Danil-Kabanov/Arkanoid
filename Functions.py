from random import randint
from sys import exit
from pickle import dump, load
import pygame
import os

f = open("highscore.dat", "rb")
white = (255, 255, 255)
score = 0
volume = 100

font = pygame.font.SysFont("Courier", 45, bold=True)
medium_font = pygame.font.SysFont("Courier", 36, bold=True)
small_font = pygame.font.SysFont("Courier", 35, bold=True)


def close_arkanoid():  # Выход из игры
    f.close()
    pygame.quit()
    exit()


def get_mouse_x():  # Функция для нахождения абсциссы указателя в данный момент.
    return pygame.mouse.get_pos()[0]


def get_mouse_y():  # Функция для нахождения ординаты указателя в данный момент.
    return pygame.mouse.get_pos()[1]


def load_theme():  # Плеер.
    music_theme = randint(1, 5)
    music = {1: "ErrorRate", 2: "Humdrum", 3: "Ictus", 4: "Plunge", 5: "Zigzag"}
    music_to_load = os.path.join("audio", "themes", f"Viscid_{music[music_theme]}.mp3")
    pygame.mixer.music.load(music_to_load)
    return music_to_load


def f_write_score():  # Запись данных в бинарный файл и их чтение
    global f, players, score, highscore, level, highlevel
    f = open("highscore.dat", "rb")
    try:
        players = load(f)
    except EOFError:
        players = {"Player1": [0, 0]}
    f.close()
    if "Player1" in players.keys():
        if len(players["Player1"]) == 2:
            highscore = players["Player1"][0]
            highlevel = players["Player1"][1]
        else:
            highscore = 0
            highlevel = 0
            f.close()
            f = open("highscore.dat", "wb")
            players = {"Player1": [0, 0]}
            dump(players, f, True)
    else:
        highscore = 0
        highlevel = 0
        f.close()
        f = open("highscore.dat", "wb")
        players = {"Player1": [0, 0]}
        dump(players, f, True)
    f.close()
    if score > int(highscore):
        f = open("highscore.dat", "wb")
        players = {"Player1": [score, level]}
        dump(players, f, True)
        f.close()

