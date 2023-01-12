import pygame
from functions import *
from classes import *

# создаём группы спрайтов
board_sprite = pygame.sprite.Group()

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
start = False
left = False
r = False
dvij = False
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
        # начать игру, если нажали кнопку 'S'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if not start:
                board = Board(board_sprite, left, r)
                start = True
                dvij = True
                all_sprites.add(board_sprite)
        if dvij:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                board.left = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                board.left = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                board.right = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                board.right = True
            elif event.type == pygame.MOUSEMOTION:
                board.update(event.pos[0])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ball.is_paused = False
    if dvij:
        # передвижение доски
        board.update()
    else:
        # вывод на экран инструции до старта
        starts(screen)
    # прорисовка и обновление экрана
    pygame.display.flip()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    clock.tick(fps)
# выход
pygame.quit()
