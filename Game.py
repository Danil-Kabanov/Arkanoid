from random import randint, choice
from pickle import dump, load
from pygame.locals import *
from Create_block import Block
from Create_ball import Ball
from Create_platform import Platform
from Functions import close_arkanoid, get_mouse_x, get_mouse_y, load_theme, f_write_score
import os
import pygame


# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
grey = (127, 127, 127)
red = (225, 0, 0)
green = (0, 255, 0)
colors = ["red", "orange", "yellow", "green", "lightblue", "blue", "purple"]  # Цвета блоков

# Размеры блоков
block_width = 23
block_height = 15

# Размеры поля
ncolumn = 32
nrow = 4

pygame.init()  # Инициализация Pygame

# Параметры экрана
screen = pygame.display.set_mode([800, 600])
background = pygame.Surface(screen.get_size())
pygame.display.set_caption("Arkanoid")
icon = pygame.Surface((10, 10))
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
clock = pygame.time.Clock()
fps = 90  # 90 кадров в секунду
score = 0
volume = 100
difference = 0
selected = 0

# Шрифты
font = pygame.font.SysFont("Courier", 45, bold=True)
medium_font = pygame.font.SysFont("Courier", 36, bold=True)
small_font = pygame.font.SysFont("Courier", 35, bold=True)

# Звуки
whoosh = pygame.mixer.Sound(os.path.join("audio", "sounds", "introwhoosh.wav"))
bounce = pygame.mixer.Sound(os.path.join("audio", "sounds", "bounce.wav"))
music_themes = [1, 2, 3, 4, 5]

start = False
paused = False
settings_opened = False
ext_settings_opened = False
reset_opened = False


# Открытие бинарного файла и чтение данных
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

fog = pygame.Surface((800, 600))  # Затемняющая поверхность

# Текстовые индикаторы и кнопки
x_text = small_font.render("X", True, white)
sc_text = small_font.render(f"{score}", True, white)
hscore_text = small_font.render(f"Best score: {highscore}", True, white)
item1 = small_font.render("resume (Esc)", True, white)
item2 = small_font.render("new game (N)", True, white)
item3 = small_font.render("settings (S)", True, white)
item4 = small_font.render("exit (AltF4)", True, white)
item5 = small_font.render("-", True, white)
item6 = small_font.render("+", True, white)
item7 = small_font.render(f"{volume}", True, white)
xpos = x_text.get_rect(centerx=775, top=5)
sc_pos = sc_text.get_rect(left=5, top=5)
hscore_pos = hscore_text.get_rect(left=10, top=560)
item1pos = item1.get_rect(centerx=400, top=310)
item2pos = item2.get_rect(centerx=400, top=350)
item3pos = item3.get_rect(centerx=400, top=390)
item4pos = item4.get_rect(centerx=400, top=430)
item5pos = item5.get_rect(centerx=431, top=350)
item6pos = item6.get_rect(centerx=515, top=350)
item7pos = item7.get_rect(centerx=473, top=350)

player = Platform()  # Создание платформы
ball = Ball()  # Создание шарика
start_ball_pos = 180  # Начальная ордината шарика

# Добавление спрайтов в группы
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
balls.add(ball)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)


def clear_items():  # Снятие выделения с элементов интерфейса
    global item1, item2, item3, item4, item5, item6, item7
    if settings_opened:
        item1 = small_font.render("< back (Esc)", True, white)
        item2 = small_font.render("volume", True, white)
        item3 = small_font.render("", True, white)
        item4 = small_font.render("", True, white)
        item5 = small_font.render("-", True, white)
        item6 = small_font.render("+", True, white)
        item7 = small_font.render(f"{volume}", True, white)
    else:
        item1 = small_font.render("resume (Esc)", True, white)
        item2 = small_font.render("new game (N)", True, white)
        item3 = small_font.render("settings (S)", True, white)
        item4 = small_font.render("exit (AltF4)", True, white)


def center_items():  # Возвращение сдвинувшихся элементов интерфейса на исходные позиции
    global item1pos, item2pos, item3pos, item4pos, item5pos, item6pos, item7pos
    item1pos = item1.get_rect(centerx=400, top=310)
    if settings_opened:
        item2pos = item2.get_rect(centerx=337, top=350)
    else:
        item2pos = item2.get_rect(centerx=400, top=350)
    item3pos = item3.get_rect(centerx=400, top=390)
    item4pos = item4.get_rect(centerx=400, top=430)
    item5pos = item5.get_rect(centerx=431, top=350)
    item6pos = item6.get_rect(centerx=515, top=350)
    item7pos = item7.get_rect(centerx=473, top=350)


def pause():  # Функция, отвечающая за паузу
    global event,       \
        paused,         \
        selected,       \
        settings_opened, \
        game_over,      \
        result,         \
        nextlevel,      \
        score,          \
        all_sprites,     \
        blocks,         \
        nrow,           \
        level,          \
        x_text,          \
        sc_text,         \
        hscore_text,     \
        item1,          \
        item2,          \
        item3,          \
        item4
    while paused:
        x_text = small_font.render("X", True, white)
        sc_text = small_font.render("||", True, white)
        hscore_text = small_font.render(f"Best score: {highscore}", True, white)
        ball.image = pygame.image.load(os.path.join("images", "ball", f"ballframe{ballframe}.png"))
        player.image = pygame.image.load(os.path.join("images", "player", f"playerframe{playerframe}.png"))
        if speedup:
            screen.blit(x_text, xpos)
        fog.set_alpha(200)
        screen.fill(black)
        fog.fill(black)
        all_sprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sc_text, sc_pos)
        screen.blit(hscore_text, hscore_pos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)

        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    event.key = None
                    close_arkanoid()
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.unpause()
                    paused = False
                    event.key = None
                if event.key == K_n:
                    screen.fill(black)
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.queue(load_theme())
                    paused = False
                    result = None
                    game_over = True
                    nextlevel = False
                    nrow = 4
                    score = 0
                    level = 1
                    dead_blocks.clear()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(ball)
                    all_sprites.add(player)
                    blocks = pygame.sprite.Group()
                    event.key = None
                if event.key == K_s:
                    settings_opened = True
                    clear_items()
                    center_items()
                    event.key = None
                    settings()
                if event.key == K_DOWN:
                    if selected == 0 or selected == 4:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 1:
                        pygame.mouse.set_pos(item2pos.center)
                    elif selected == 2:
                        pygame.mouse.set_pos(item3pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item4pos.center)
                    event.key = None
                if event.key == K_UP:
                    if selected == 0 or selected == 1:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 2:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item2pos.center)
                    elif selected == 4:
                        pygame.mouse.set_pos(item3pos.center)
                    event.key = None
            if item1pos.left <= get_mouse_x() <= item1pos.right and \
                    item1pos.top <= get_mouse_y() <= item1pos.bottom:
                clear_items()
                item1 = medium_font.render("resume (Esc)", True, grey)
                center_items()
                selected = 1
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.unpause()
                    if pygame.mixer.music.get_endevent():
                        pygame.mixer.music.queue(load_theme())
                    paused = False

            elif item2pos.left <= get_mouse_x() <= item2pos.right and \
                    item2pos.top <= get_mouse_y() <= item2pos.bottom:
                clear_items()
                item2 = medium_font.render("new game (N)", True, grey)
                center_items()
                selected = 2
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    screen.fill(black)
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.queue(load_theme())
                    paused = False
                    result = None
                    game_over = True
                    nextlevel = False
                    nrow = 4
                    score = 0
                    level = 1
                    dead_blocks.clear()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(ball)
                    all_sprites.add(player)
                    blocks = pygame.sprite.Group()

            elif item3pos.left <= get_mouse_x() <= item3pos.right and \
                    item3pos.top <= get_mouse_y() <= item3pos.bottom:
                clear_items()
                item3 = medium_font.render("settings (S)", True, grey)
                center_items()
                selected = 3
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    settings_opened = True
                    clear_items()
                    center_items()
                    settings()

            elif item4pos.left <= get_mouse_x() <= item4pos.right and \
                    item4pos.top <= get_mouse_y() <= item4pos.bottom:
                clear_items()
                item4 = medium_font.render("exit (AltF4)", True, grey)
                center_items()
                selected = 4
                if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                    event.button = None
                    event.key = None
                    close_arkanoid()

            else:
                clear_items()
                center_items()
                selected = 0

        pygame.display.flip()
        clock.tick(fps)


def settings():  # Функция, отвечающая за настройки
    global event,       \
        settings_opened, \
        selected,       \
        volume,         \
        x_text,          \
        sc_text,         \
        hscore_text,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        item5,          \
        item6,          \
        ext_settings_opened
    while settings_opened:
        if speedup:
            screen.blit(x_text, xpos)
        fog.set_alpha(200)
        screen.fill(black)
        fog.fill(black)
        ball.image = pygame.image.load(os.path.join("images", "ball", f"ballframe{ballframe}.png"))
        player.image = pygame.image.load(os.path.join("images", "player", f"playerframe{playerframe}.png"))
        all_sprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sc_text, sc_pos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        screen.blit(item5, item5pos)
        screen.blit(item6, item6pos)
        screen.blit(item7, item7pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    event.key = None
                    close_arkanoid()
                if event.key == K_ESCAPE:
                    settings_opened = False
                    event.key = None
                    clear_items()
                    center_items()
                if event.key == K_RSHIFT or event.key == K_LSHIFT:
                    event.key = None
                    settings_opened = False
                    ext_settings_opened = True
                    clear_items()
                    center_items()
                if event.key == K_MINUS or event.key == K_KP_MINUS:
                    if volume > 0:
                        volume -= 5
                        pygame.mixer.music.set_volume(volume / 100)
                    event.key = None
                if event.key == K_EQUALS or event.key == K_KP_PLUS:
                    if volume < 100:
                        volume += 5
                    event.key = None
                if event.key == K_DOWN:
                    if selected == 0 or selected == 4:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 1:
                        pygame.mouse.set_pos(item5pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 5:
                        pygame.mouse.set_pos(item6pos.center)
                    elif selected == 6:
                        pygame.mouse.set_pos(item3pos.center)
                    event.key = None
                if event.key == K_UP:
                    if selected == 0 or selected == 1:
                        pygame.mouse.set_pos(item4pos.center)
                    elif selected == 3:
                        pygame.mouse.set_pos(item6pos.center)
                    elif selected == 4:
                        pygame.mouse.set_pos(item3pos.center)
                    elif selected == 5:
                        pygame.mouse.set_pos(item1pos.center)
                    elif selected == 6:
                        pygame.mouse.set_pos(item5pos.center)
                    event.key = None
                if event.key == K_SPACE:
                    if selected == 1:
                        settings_opened = False
                        clear_items()
                        center_items()
                    elif selected == 4:
                        settings_opened = False
                        ext_settings_opened = True
                        clear_items()
                        center_items()
                    elif selected == 5:
                        if volume > 0:
                            volume -= 5
                            pygame.mixer.music.set_volume(volume / 100)
                    elif selected == 6:
                        if volume < 100:
                            volume += 5
                            pygame.mixer.music.set_volume(volume / 100)
                    event.key = None

        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = medium_font.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.key = None
                settings_opened = False
                clear_items()
                center_items()
            if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                event.button = None
                event.key = None
                settings_opened = False
                ext_settings_opened = True
                clear_items()
                center_items()
        elif item5pos.left <= get_mouse_x() <= item5pos.right and \
                item5pos.top <= get_mouse_y() <= item5pos.bottom:
            clear_items()
            item5 = small_font.render("-", True, grey)
            center_items()
            selected = 5
            if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                event.button = None
                event.key = None
                if volume > 0:
                    volume -= 5
                    event.button = 0
                    pygame.mixer.music.set_volume(volume / 100)
        elif item6pos.left <= get_mouse_x() <= item6pos.right and \
                item6pos.top <= get_mouse_y() <= item6pos.bottom:
            clear_items()
            item6 = small_font.render("+", True, grey)
            center_items()
            selected = 6
            if event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYDOWN and event.key == K_SPACE:
                event.button = None
                event.key = None
                if volume < 100:
                    volume += 5
                    event.button = 0
                    pygame.mixer.music.set_volume(volume / 100)
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def reset():
    global event,       \
        reset_opened,    \
        selected,       \
        x_text,          \
        sc_text,         \
        hscore_text,     \
        item1,          \
        item2,          \
        item3,          \
        item4,          \
        ext_settings_opened
    while reset_opened:
        if speedup:
            screen.blit(x_text, xpos)
        fog.set_alpha(200)
        fog.fill(black)
        ball.image = pygame.image.load(os.path.join("images", "ball", f"ballframe{ballframe}.png"))
        player.image = pygame.image.load(os.path.join("images", "player", f"playerframe{playerframe}.png"))
        all_sprites.draw(screen)
        screen.blit(fog, (0, 0))
        screen.blit(sc_text, sc_pos)
        screen.blit(item1, item1pos)
        screen.blit(item2, item2pos)
        screen.blit(item3, item3pos)
        screen.blit(item4, item4pos)
        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                event.key = None
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT and event.key == K_F4:
                    close_arkanoid()
                if event.key == K_ESCAPE:
                    reset_opened = False
                    ext_settings_opened = True
                    event.key = None
                    clear_items()
                    center_items()
        if item1pos.left <= get_mouse_x() <= item1pos.right and \
                item1pos.top <= get_mouse_y() <= item1pos.bottom:
            clear_items()
            item1 = medium_font.render("< back (Esc)", True, grey)
            center_items()
            selected = 1
            if event.type == MOUSEBUTTONUP and event.button == 1:
                event.button = None
                reset_opened = False
                ext_settings_opened = True
                clear_items()
                center_items()
        else:
            clear_items()
            center_items()

        pygame.display.flip()
        clock.tick(fps)


def intro():  # Приветственный экран в начале игры
    global start, i, event
    whoosh.play()

    while not start:
        for i in range(0, 255, 2):
            text = small_font.render("Press any key to start the game", True, (i, i, i))
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 450

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
                    if event.key != K_LALT and event.key != K_RALT:
                        start = True
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            clock.tick(fps)
            screen.blit(text, textpos)
            pygame.display.flip()

        for i in range(255, 0, -2):
            text = small_font.render("Press any key to start the game", True, (i, i, i))
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 450

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
                    if event.key != K_LALT and event.key != K_RALT:
                        start = True
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            clock.tick(fps)
            screen.fill(black)
            screen.blit(text, textpos)
            pygame.display.flip()


intro()  # Отображение начального экрана

dead_blocks = []
score = 0
level = 1
ballframe = 1
playerframe = 1
framecount = 1

result = None
shift = False

current_speed = ball.speed

while True:
    game_over = False
    nextlevel = False
    speedup = False
    movemode = 0

    while not start:
        for i in range(0, 255, 2):
            text1 = small_font.render("Press any key to start new game", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450

            text2 = font.render("You win!", True, green)
            text2pos = text2.get_rect(centerx=background.get_width() / 2)
            text2pos.top = 300

            text3 = font.render("Game over", True, red)
            text3pos = text3.get_rect(centerx=background.get_width() / 2)
            text3pos.top = 300

            text4 = small_font.render(f"Your score is {score}", True, white)
            text4pos = text4.get_rect(centerx=background.get_width() / 2)
            text4pos.top = 350

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    dead_blocks.clear()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(ball)
                    all_sprites.add(player)
                    blocks = pygame.sprite.Group()
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
                    if event.key != K_LALT and event.key != K_RALT:
                        start = True
                        dead_blocks.clear()
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(ball)
                        all_sprites.add(player)
                        blocks = pygame.sprite.Group()
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            # Анимации конца игры
            if player.rect.y < 580:
                player.rect.y += 1
            for b in blocks:
                b.rect.y += randint(2, 3)

            clock.tick(fps)
            screen.fill(black)
            player.image = pygame.image.load(os.path.join("images", "player", f"playerframe{playerframe}.png"))

            if not nextlevel:
                text1 = small_font.render("Press any key to start new game", True, (i, i, i))
            else:
                text1 = small_font.render("Press any key to start next level", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450
            screen.blit(text1, text1pos)

            all_sprites.draw(screen)

            if result == "Victory":
                screen.blit(text2, text2pos)
                nextlevel = True

            elif result == "Defeat":
                if level == 1:
                    text4 = small_font.render(f"Your score is {score}", True, white)
                else:
                    text4 = small_font.render(f"You reached level {level}", True, white)
                    text5 = small_font.render(f"and your score is {score}", True, white)
                    
                    text5pos = text5.get_rect(centerx=background.get_width() / 2)
                    text5pos.top = 400
                    screen.blit(text5, text5pos)

                text4pos = text4.get_rect(centerx=background.get_width() / 2)
                text4pos.top = 350
                screen.blit(text3, text3pos)
                screen.blit(text4, text4pos)

            pygame.display.flip()

        for i in range(255, 0, -2):
            text1 = small_font.render("Press any key to start new game", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450

            text2 = font.render("You win!", True, green)
            text2pos = text2.get_rect(centerx=background.get_width() / 2)
            text2pos.top = 300

            text3 = font.render("Game over", True, red)
            text3pos = text3.get_rect(centerx=background.get_width() / 2)
            text3pos.top = 300

            text4 = small_font.render(f"Yor score is {score}", True, white)
            text4pos = text4.get_rect(centerx=background.get_width() / 2)
            text4pos.top = 350

            for event in pygame.event.get():  # Проверка событий
                if event.type == QUIT:
                    close_arkanoid()
                if event.type == MOUSEBUTTONDOWN:
                    start = True
                    dead_blocks.clear()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(ball)
                    all_sprites.add(player)
                    blocks = pygame.sprite.Group()
                    break
                if event.type == KEYDOWN:
                    if event.mod == KMOD_ALT:
                        if event.key == K_F4:
                            close_arkanoid()
                    if event.key != K_LALT and event.key != K_RALT:
                        start = True
                        dead_blocks.clear()
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(ball)
                        all_sprites.add(player)
                        blocks = pygame.sprite.Group()
                        break
            if start:
                load_theme()
                pygame.mixer.music.queue(load_theme())
                pygame.mixer.music.play()
                break

            # Анимации конца игры
            if player.rect.y < 580:
                player.rect.y += 1
            for b in blocks:
                if b.rect.y <= screen.get_height():
                    b.rect.y += randint(2, 3)

            clock.tick(fps)
            screen.fill(black)
            player.image = pygame.image.load(os.path.join("images", "player", f"playerframe{playerframe}.png"))

            if not nextlevel:
                text1 = small_font.render("Press any key to start new game", True, (i, i, i))
            else:
                text1 = small_font.render("Press any key to start next level", True, (i, i, i))
            text1pos = text1.get_rect(centerx=background.get_width() / 2)
            text1pos.top = 450
            screen.blit(text1, text1pos)

            all_sprites.draw(screen)

            if result == "Victory":
                screen.blit(text2, text2pos)
                nextlevel = True

            elif result == "Defeat":
                if level == 1:
                    text4 = small_font.render(f"Your score is {score}", True, white)
                else:
                    text4 = small_font.render(f"You reached level {level}", True, white)
                    text5 = small_font.render(f"and your score is {score}", True, white)
                    text5pos = text5.get_rect(centerx=background.get_width() / 2)
                    text5pos.top = 400
                    screen.blit(text5, text5pos)

                text4pos = text4.get_rect(centerx=background.get_width() / 2)
                text4pos.top = 350
                screen.blit(text3, text3pos)
                screen.blit(text4, text4pos)

            pygame.display.flip()

    if result == "Defeat":
        f_write_score()
        nrow = 4
        score = 0
        level = 1
    elif result == "Victory":
        level += 1

    top = 50
    ballframe = 1
    playerframe = 1
    framecount = 1
    player.rect.y = 580
    levels = [["11111111111111111111111111111111",  # 1 уровень
               "11111111111111111111111111111111",
               "11111111111111111111111111111111",
               "11111111111111111111111111111111"],

              ["00101010101010101010101010101010",  # 2 уровень
               "01010101010101010101010101010100",
               "00101010101010101010101010101010",
               "01010101010101010101010101010100",
               "00101010101010101010101010101010"],

              ["11111111111111111111111111111111",  # 3 уровень
               "10000000000000000000000000000001",
               "10111111111111111111111111111101",
               "10111111111111111111111111111101",
               "10000000000000000000000000000001",
               "11111111111111111111111111111111"],

              ["11111111111111110011001100110011",  # 4 уровень
               "11111111111111110011001100110011",
               "11001100110011000011001100110011",
               "11001100110011000011001100110011",
               "11001100110011000011001100110011",
               "11001100110011001111111111111111",
               "11001100110011001111111111111111"],

              ["11001100110011001100110011001100",  # 5 уровень
               "11001100110011001100110011001100",
               "00110011001100110011001100110011",
               "00110011001100110011001100110011",
               "11001100110011001100110011001100",
               "11001100110011001100110011001100",
               "00110011001100110011001100110011",
               "00110011001100110011001100110011"],

              ["00001000001000001000001000001000",  # 6 уровень
               "10000010000010000010000010000010",
               "00100000100000100000100000100000",
               "00001000001000001000001000001000",
               "10000010000010000010000010000010",
               "00100000100000100000100000100000",
               "00001000001000001000001000001000",
               "00100000100000100000100000100000",
               "10000010000010000010000010000010"],

              ["01001001011010010110100101100010",  # 7 уровень
               "00101011101001010010010101001010",
               "11110010111001010101010110101010",
               "01010101000110110110100111111111",
               "01001011111111000100101010000111",
               "01010100110010110100100100100111",
               "10100100101101000101010101010110",
               "01011101001001011001100011101010",
               "00000011111011010100010111100111",
               "01010101010000000111111111011011"],

              ["01111111111111111111111111111110",  # 8 уровень
               "10000000000000000000000000000001",
               "10011111111111111111111111111001",
               "10100000000000000000000000000101",
               "10101111111111111111111111110101",
               "10100000000000000000000000000101",
               "10011111111111111111111111111001",
               "10000000000000000000000000000001",
               "01111111111111111111111111111110"]]

    if level <= 8:
        for row in range(len(levels[level-1])):  # Отрисовка блоков
            for column in range(ncolumn):
                if int(levels[level-1][row][column]):
                    block = Block(choice(colors), column * (block_width + 2) + 1, top)
                    blocks.add(block)
                    all_sprites.add(block)
            top += block_height + 2
    else:
        for row in range(nrow):  # Отрисовка блоков
            for column in range(ncolumn):
                block = Block(choice(colors), column * (block_width + 2) + 1, top)
                blocks.add(block)
                all_sprites.add(block)
            top += block_height + 2

    ball.x = randint(20, 740)
    ball.y = start_ball_pos
    ball.direction = choice(ball.directions)
    ball.speed = 1.2 + level / 10

    while not game_over:  # Главный игровой цикл
        clock.tick(fps)
        screen.fill(black)
        x_text = small_font.render("X", True, white)
        sc_text = small_font.render(f"{score}", True, white)

        if pygame.mixer.music.get_endevent():
            pygame.mixer.music.queue(load_theme())

        for event in pygame.event.get():  # Проверка событий
            if event.type == QUIT:
                close_arkanoid()
            if event.type == KEYDOWN:
                if event.mod == KMOD_ALT:
                    if event.key == K_F4:
                        close_arkanoid()
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    pygame.mixer.music.pause()
                    paused = True
                if event.key == K_x:
                    speedup = not speedup
                    if speedup:
                        current_speed = ball.speed
                        ball.speed *= 2
                    else:
                        ball.speed = current_speed
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_a or event.key == K_d:
                    movemode = 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if player.rect.y > 450:
                        player.rect.y -= 5
                elif event.button == 5:
                    if player.rect.y < 580:
                        player.rect.y += 5
            if event.type == MOUSEMOTION:
                if movemode:
                    pygame.mouse.set_pos(player.rect.x, player.rect.y)
                movemode = 0

        if paused:
            pause()

        if not ball.update():
            player.update()

        if ball.update() and len(blocks) > 0:  # Игрок не поймал мячик
            result = "Defeat"
            whoosh.play()
            pygame.mixer.music.stop()
            game_over = True

        if pygame.sprite.spritecollide(player, balls, False):  # Отскок мячика от ракетки
            x1, y1 = ball.rect.bottomleft
            x2, y2 = ball.rect.topright
            x3, y3 = player.rect.bottomleft
            x4, y4 = player.rect.topright

            width = min(x2, x4) - max(x1, x3)  # ширина пересечения
            height = min(y1, y3) - max(y2, y4)  # высота пересечения
            if width < height or ball.rect.top > player.rect.top:
                ball.vertical_bounce()
            else:
                ball.y -= 5
                difference = player.rect.centerx - ball.rect.centerx
                if difference > 30:
                    difference = 30
                ball.bounce(difference)
                if 85 < ball.direction < 180:
                    ball.direction = 85
                elif 180 < ball.direction < 275:
                    ball.direction = 275
                ball.speed += 0.03
                if ball.direction < 0:
                    ball.direction += 360
                if ball.direction >= 360:
                    ball.direction -= 360

        dead_blocks = pygame.sprite.spritecollide(ball, blocks, True)  # Список только что сбитых блоков

        if len(dead_blocks) > 0:
            if len(dead_blocks) == 1:
                hitted = dead_blocks[0]
                x1, y1 = ball.rect.bottomleft
                x2, y2 = ball.rect.topright
                x3, y3 = hitted.rect.bottomleft
                x4, y4 = hitted.rect.topright
                width = min(x2, x4) - max(x1, x3)  # ширина пересечения
                height = min(y1, y3) - max(y2, y4)  # высота пересечения
                if width < height:
                    ball.vertical_bounce()
                else:
                    ball.bounce(0)
                score += 1
            else:
                hitted1 = dead_blocks[0]
                hitted2 = dead_blocks[1]
                hitted_left = min(hitted1.rect.left, hitted2.rect.left)
                hitted_top = min(hitted1.rect.top, hitted2.rect.top)
                if hitted1.rect.left == hitted2.rect.left:
                    hitted_width = 23
                    hitted_height = 32
                else:
                    hitted_width = 48
                    hitted_height = 15
                hitted = pygame.Rect(hitted_left, hitted_top, hitted_width, hitted_height)
                x1, y1 = ball.rect.bottomleft
                x2, y2 = ball.rect.topright
                x3, y3 = hitted.bottomleft
                x4, y4 = hitted.topright
                width = min(x2, x4) - max(x1, x3)  # ширина пересечения
                height = min(y1, y3) - max(y2, y4)  # высота пересечения
                if width < height:
                    ball.vertical_bounce()
                else:
                    ball.bounce(0)
                score += len(dead_blocks)
                if ball.direction < 0:
                    ball.direction += 360
                if ball.direction >= 360:
                    ball.direction -= 360

            if len(blocks) == 0:  # Игрок сбил все блоки
                result = "Victory"
                whoosh.play()
                pygame.mixer.music.stop()
                game_over = True
                if nrow < 10:
                    nrow += 1
                    start_ball_pos += block_height

        # Анимация мячика и ракетки
        if framecount == fps:
            ballframe += 1
            playerframe += 1
            framecount = 1
        if framecount % (fps // 6) == 0:
            ballframe += 1
            playerframe += 1
        if ballframe == 9:
            ballframe = 1
        if playerframe == 14:
            playerframe = 1
        ball.image = pygame.image.load(os.path.join("images", "ball", f"ballframe{ballframe}.png"))
        player.image = pygame.image.load(os.path.join("images", "player", f"playerframe{playerframe}.png"))
        framecount += 1

        if speedup:
            screen.blit(x_text, xpos)
        screen.blit(sc_text, sc_pos)
        all_sprites.draw(screen)
        pygame.display.flip()
        start = False
