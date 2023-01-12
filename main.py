import pygame
from functions import *

# инициализация pygame
pygame.init()
# создание экрана
size = 750, 850
screen = pygame.display.set_mode(size)
# задаём название и иконку главному окну приложения
pygame.display.set_icon(load_image('icon.png', -1))
pygame.display.set_caption('Арканоид')
# создание группы, в которой будут находиться все спрайты
all_sprites = pygame.sprite.Group()
# создание переменных для последовательной работы игры
clock = pygame.time.Clock()
fps = 150
running = True

# основной цикл игры
while running:
    # перебор всех сигналов
    for event in pygame.event.get():
        # прекратить цикл, если приложение закрыли
        if event.type == pygame.QUIT:
            running = False
    # прорисовка и обновление экрана
    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(fps)
# выход
pygame.quit()

