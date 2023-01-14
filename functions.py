import os
import sys
from classes import *


# функция, загружающая картинку
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# создание надписи перед началом игры
def starts(screen):
    # загрузка киртинок
    image = pygame.transform.scale(load_image('fon_start.jpg'), (750, 850))
    image_text = load_image('text_start.png', -1)
    # отрисовка картинок на экране
    screen.blit(image, (0, 0))
    screen.blit(image_text, (0, -25))


# функция, проверяющая столкновения мячика
def collisions(ball, board, board_sprite, dead, screen, clock, fps):
    # проверка столкновения мяча с верхней границей
    if ball.rect.top <= 50:
        ball.vy = 2
        ball.vx = -2 if ball.vx < 0 else 2
    # проверка столкновения мяча с левой границей
    if ball.rect.left <= 0:
        ball.vx = 2
        ball.vy = -2 if ball.vy < 0 else 2
    # проверка столкновения мяча с правой границей
    elif ball.rect.right >= 750:
        ball.vx = -2
        ball.vy = -2 if ball.vy < 0 else 2
    # проверяем столкновения мячика с дощечкой
    elif pygame.sprite.spritecollideany(ball, board_sprite):
        # находим dx(дельту пересечения по х) и dy(дельта пересечения по у)
        if ball.vx > 0:
            dx = ball.rect.right - board.rect.left
        else:
            dx = board.rect.right - ball.rect.left
        if ball.vy > 0:
            dy = ball.rect.bottom - board.rect.top
        else:
            dy = board.rect.bottom - ball.rect.top
        # проверка на столкновение с углами дощечки
        if abs(dx - dy) == 1:
            ball.vx = -2 if ball.vx > 0 else 2
            ball.vy = -2 if ball.vy > 0 else 2
        # столкновение с боковыми сторонами дощечки
        elif dy > dx:
            ball.vx = -2 if ball.vx > 0 else 2
        # столкновение с верхней частью дощечки
        else:
            """проверяем 5 случаев столкновения: 1 - когда мяч отскакивает от центра дощечки; 2 - когда мяч отскакивает 
            от левой части дощечки, а ball.vx положительный; 3 - когда мяч отскакивает от правой части дощечки,
            а ball.vx положительный; 4 - когда мяч отскакивает от левой части дощечки, а ball.vx отрицательный; 5 - 
            когда мяч отскакивает от правой части дощечки, а ball.vx отрицательный.
            В каждом случае меняем траекторию мяча относительно луча падения"""
            if ball.rect.x in range(board.rect.x + 15, board.rect.x + 46):
                ball.vy = -ball.vy
            elif ball.rect.x in range(board.rect.x - 5, board.rect.x + 26) and ball.vx > 0:
                ball.vy = -3
            elif ball.rect.x in range(board.rect.x + 46, board.rect.x + 77) and ball.vx > 0:
                ball.vy = -1
            elif ball.rect.x in range(board.rect.x - 5, board.rect.x + 26) and ball.vx < 0:
                ball.vy = -1
            elif ball.rect.x in range(board.rect.x + 46, board.rect.x + 77) and ball.vx < 0:
                ball.vy = -3
    # проверка на проигрыш
    if ball.rect.y >= 850:
        dead += 1
        if dead < 3:
            ball.is_paused = True
            ball.rect.x = 370
            ball.rect.y = 750
            ball.vy = choice([-1, -2, -3])
        elif dead == 3:
            score, dead = gameover(screen, ball, fps, clock)
    return dead


# счетчик смертей
def score_dead_count(dead, screen, heart):
    if int(dead) == 0:
        screen.blit(heart, (660, 2))
        screen.blit(heart, (600, 2))
        screen.blit(heart, (540, 2))
    if int(dead) == 1:
        screen.blit(heart, (600, 2))
        screen.blit(heart, (660, 2))
    if int(dead) == 2:
        screen.blit(heart, (660, 2))


# функция, работающая после проигрыша
def gameover(screens, ball, fps, clock):
    # открываем картинку
    fons = pygame.transform.scale(load_image('gameover.png'), (750, 850))
    # выводим её на экран
    screens.blit(fons, (0, 0))
    # ждём, пока пользовател не нажмет на R для рестарта
    c = True
    while c:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif events.type == pygame.KEYDOWN and events.key == pygame.K_r:
                locals()
                c = False
                ball.rect.x = 370
                ball.rect.y = 750
                ball.vy = -2
                score = '000'
                ball.is_paused = True
                return score, 0
        # вывод надписи-инструкции
        pygame.display.flip()
        clock.tick(fps)
        text = 'Нажмите R для рестарта'
        font = pygame.font.Font(None, 50)
        top = 725
        str_ren = font.render(text, 1, pygame.Color('white'))
        str_rect = str_ren.get_rect()
        str_rect.top = top
        str_rect.left = 150
        screens.blit(str_ren, str_rect)
    return


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def karta(level_map, stens_sprite, karta_sprites, block_sprite):
    level_map = load_level(level_map)
    count_y = 0
    count_x = 0
    for y in range(len(level_map)):
        count_y += 1
        for x in range(len(level_map[y])):
            count_x += 1
            if level_map[y][x] == '#':
                stens_sprite.add(Stena(x, y, count_x, count_y))
            elif level_map[y][x] == '*':
                block_sprite.add(Block(x, y, 1, count_x, count_y))
            elif level_map[y][x] == '$':
                block_sprite.add(Block(x, y, 3, count_x, count_y))
        count_x = 0
    karta_sprites.add(stens_sprite, block_sprite)


def switch_paused(ball, board, screen):
    ball.is_paused = True
    board.is_paused = True
    image = pygame.Surface((750, 850), pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    pygame.draw.rect(image, (0, 0, 0, 120), (0, 0, 750, 850))
    screen.blit(image, (0, 0))
    text = 'Нажмите SPACE для продолжения'
    font = pygame.font.Font(None, 50)
    top = 400
    str_ren = font.render(text, 1, pygame.Color('yellow'))
    str_rect = str_ren.get_rect()
    str_rect.top = top
    str_rect.left = 75
    screen.blit(str_ren, str_rect)
    c = True
    while c:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ball.is_paused = False
                board.is_paused = False
                c = False
        pygame.display.flip()
        screen.blit(str_ren, str_rect)