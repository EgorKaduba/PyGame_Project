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
def collisions(screen, ball, board, board_sprite, clock, fps, dead, karta_sprites, stens_sprite, block_sprite, score,
               current_level):
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
            score, dead = gameover(screen, clock, fps, ball, karta_sprites, stens_sprite, block_sprite, score,
                                   current_level)
    return score, dead


# счетчик смертей
def score_dead_count(dead, screen, heart, score, star):
    # отрисовка границ
    pygame.draw.rect(screen, pygame.Color('orange'), (-3, -3, 150, 50), 3)
    screen.blit(star, (67, -3))
    # вывод счёта
    text = score
    font = pygame.font.Font(None, 70)
    str_ren = font.render(text, 1, pygame.Color('yellow'))
    str_rect = str_ren.get_rect()
    str_rect.x = 5
    str_rect.y = 0
    screen.blit(str_ren, str_rect)
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
def gameover(screens, clock, fps, ball, karta_sprites, stens_sprite, block_sprite, score, current_level):
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
                ball.is_paused = True
                score = '000'
                for i in block_sprite:
                    i.kill()
                for i in stens_sprite:
                    i.kill()
                maps(current_level, stens_sprite, karta_sprites, block_sprite)
                return score, 0
        # вывод надписи-инструкции
        pygame.display.flip()
        clock.tick(fps)
        text = 'Нажмите R для рестарта'
        text_score = f'Ваш результат: {int(score)}'
        font = pygame.font.Font(None, 50)
        top = 725
        str_ren_score = font.render(text_score, 1, pygame.Color('yellow'))
        str_ren = font.render(text, 1, pygame.Color('white'))
        str_rect = str_ren.get_rect()
        str_rect.top = top
        str_rect.left = 150
        screens.blit(str_ren, str_rect)
        str_rects = str_ren_score.get_rect()
        str_rects.top = 100
        str_rects.left = 200
        screens.blit(str_ren_score, str_rects)
    return


def load_level(filename):
    filename = os.path.join('data', filename)
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def maps(level_map, stens_sprite, karta_sprites, block_sprite):
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


# функция, проверяющая столкновения мячика и блоков
def collide_block(ball, block_sprite, score):
    # перебор столкновений
    hit = pygame.sprite.spritecollide(ball, block_sprite, False)
    for i in hit:
        if i.hp == 1:
            score = scores(score, i.count)
            if pygame.sprite.spritecollideany(ball, block_sprite):
                # находим dx(дельту пересечения по х) и dy(дельта пересечения по у)
                if ball.vx > 0:
                    dx = ball.rect.right - i.rect.left
                else:
                    dx = i.rect.right - ball.rect.left
                if ball.vy > 0:
                    dy = ball.rect.bottom - i.rect.top
                else:
                    dy = i.rect.bottom - ball.rect.top
                # изменяем направление полета шарика
                if abs(dx - dy) < 5:
                    ball.vx = -2 if ball.vx > 0 else 2
                    ball.vy = -2 if ball.vy > 0 else 2
                    i.kill()
                    return ball.vx, ball.vy, score
                elif dx > dy:
                    ball.vy = -2 if ball.vy > 0 else 2
                    i.kill()
                    return ball.vx, ball.vy, score
                else:
                    ball.vx = -2 if ball.vx > 0 else 2
                    i.kill()
                    return ball.vx, ball.vy, score
        else:
            i.hp -= 1
            if pygame.sprite.spritecollideany(ball, block_sprite):
                # находим dx(дельту пересечения по х) и dy(дельта пересечения по у)
                if ball.vx > 0:
                    dx = ball.rect.right - i.rect.left
                else:
                    dx = i.rect.right - ball.rect.left
                if ball.vy > 0:
                    dy = ball.rect.bottom - i.rect.top
                else:
                    dy = i.rect.bottom - ball.rect.top
                # изменяем направление полета шарика
                if abs(dx - dy) < 5:
                    ball.vx = -2 if ball.vx > 0 else 2
                    ball.vy = -2 if ball.vy > 0 else 2
                    return ball.vx, ball.vy, score
                elif dx > dy:
                    ball.vy = -2 if ball.vy > 0 else 2
                    return ball.vx, ball.vy, score
                else:
                    ball.vx = -2 if ball.vx > 0 else 2
    return ball.vx, ball.vy, score


# функция, проверяющая столкновения мячика со стенами
def collide_stena(ball, stens_sprite):
    # перебор столкновений мячика и стены
    hit = pygame.sprite.spritecollide(ball, stens_sprite, False)
    for i in hit:
        if pygame.sprite.spritecollideany(ball, stens_sprite):
            # находим dx(дельту пересечения по х) и dy(дельта пересечения по у)
            if ball.vx > 0:
                dx = ball.rect.right - i.rect.left
            else:
                dx = i.rect.right - ball.rect.left
            if ball.vy > 0:
                dy = ball.rect.bottom - i.rect.top
            else:
                dy = i.rect.bottom - ball.rect.top
            # изменяем направление полета шарика
            if abs(dx - dy) < 3:
                ball.vx = -3 if ball.vx > 0 else 3
                ball.vy = -1 if ball.vy > 0 else 1
                return ball.vx, ball.vy
            elif dx > dy:
                ball.vy = -2 if ball.vy > 0 else 2
                return ball.vx, ball.vy
            elif dx < dy:
                ball.vx = -2 if ball.vx > 0 else 2
                return ball.vx, ball.vy
    return ball.vx, ball.vy


# счётчик очков
def scores(score, count):
    score = str(int(score) + count)
    zero = 3 - len(score)
    score = '0' * zero + score
    return score


# функция, работающая при выигрыше
# переход на новый уровень, если он есть
def win(screen, list_of_maps, block_sprite, current_level, ball, score, stens_sprite, karta_sprites, dead):
    locals()
    # проверяем, последний ли это уровень
    if current_level != list_of_maps[-1]:
        # если все блоки разбиты, выводим картинку с поздравлением
        if not len(block_sprite.sprites()):
            # загружаем следующий уровень
            level_map = list_of_maps[list_of_maps.index(current_level) + 1]
            fon = pygame.Surface((750, 850), pygame.SRCALPHA, 32)
            fon = fon.convert_alpha()
            pygame.draw.rect(fon, (0, 0, 0, 120), (0, 0, 750, 850))
            screen.blit(fon, (0, 0))
            # загружаем победную картинку
            image = pygame.transform.scale(load_image('win.jpg', -1), (750, 850))
            c = True
            while c:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # если пользователь нажал на N, загружаем новый уровень и обновляем данные
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                        c = False
                        ball.rect.x = 370
                        ball.rect.y = 750
                        ball.vy = -2
                        ball.is_paused = True
                        score = '000'
                        for i in block_sprite:
                            i.kill()
                        for i in stens_sprite:
                            i.kill()
                        maps(level_map, stens_sprite, karta_sprites, block_sprite)
                        return score, 0, level_map
                pygame.display.flip()
                screen.blit(image, (30, -30))
            return score, dead, level_map
    # если это последний уровень, проверяем, разбиты ли все блоки, выводим победную картинку
    else:
        if not len(block_sprite.sprites()):
            fon = pygame.Surface((750, 850), pygame.SRCALPHA, 32)
            fon = fon.convert_alpha()
            pygame.draw.rect(fon, (0, 0, 0, 120), (0, 0, 750, 850))
            screen.blit(fon, (0, 0))
            image = pygame.transform.scale(load_image('win.jpg', -1), (750, 850))
            c = True
            while c:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
                screen.blit(image, (30, -30))
    level_map = current_level
    return score, dead, level_map
