import pygame
from sys import exit


pygame.init()


width = 800
height = 600


White = (255, 255, 255)
Black = (0, 0, 0)


window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")

running = False
setting = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not running and not setting:
        window.fill(Black)

        font = pygame.font.Font(None, 50)
        text = font.render("Меню старта", True, White)
        window.blit(text, ((width - text.get_width()) // 2, height // 4))

        start_button = pygame.Rect(((width - 200) // 2, height // 2 - 30, 200, 60))
        pygame.draw.rect(window, White, start_button, 2)
        font = pygame.font.Font(None, 30)
        text = font.render("Старт", True, White)
        window.blit(text, ((width - text.get_width()) // 2, height // 2 - 10))

        exit_button = pygame.Rect((width - 200) // 2, height // 2 + 110, 200, 60)
        pygame.draw.rect(window, White, exit_button, 2)
        text = font.render("Выход", True, White)
        window.blit(text, ((width - text.get_width()) // 2, height // 2 + 130))

        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                running = True
        elif exit_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                exit()

    if running:
        window.fill(White)

    pygame.display.update()
