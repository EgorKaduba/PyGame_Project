import pygame
from pygame import mixer

from functions import *

# создаём группы спрайтов
board_sprite = pygame.sprite.Group()
ball_sprite = pygame.sprite.Group()
stens_sprite = pygame.sprite.Group()
block_sprite = pygame.sprite.Group()
karta_sprites = pygame.sprite.Group()

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
dead = 0
score = '000'
# список уровней
list_of_maps = ['map.map', 'map_2.map']
current_level = list_of_maps[0]
# загрузка картинок
star = pygame.transform.scale(load_image('star.png', -1), (100, 50))
fon = pygame.transform.scale(load_image('fon2.jpg'), (750, 850))
heart = pygame.transform.scale(load_image('heart.jpg', -1), (65, 47))
# загрузка музыки
mixer.music.load(os.path.join('data', "music.mp3"))
mixer.music.play(-1)
# уровень громкости
vol = 1.0
# отключение отображения курсора
pygame.mouse.set_visible(False)
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
                ball = Ball(ball_sprite)
                board = Board(board_sprite, left, r)
                maps(current_level, stens_sprite, karta_sprites, block_sprite)
                start = True
                dvij = True
                all_sprites.add(Background(fon), board_sprite, ball_sprite)
                ball.is_paused = True
        if dvij and (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
            switch_paused(ball, board, screen)
        # регулировка громкости музыки
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                vol = vol + 0.1 if vol < 1.0 else vol
            elif event.y < 0:
                vol = vol - 0.1 if vol > 0.0 else vol
            mixer.music.set_volume(vol)
        # передвижение доски кнопками или мышкой
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
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3)) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_t):
                ball.is_paused = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                locals()
                c = False
                ball.rect.x = 370
                ball.rect.y = 750
                ball.vx = choice([-2, 2])
                ball.vy = -2
                ball.is_paused = True
                score = '000'
                dead = 0
                for i in block_sprite:
                    i.kill()
                for i in stens_sprite:
                    i.kill()
                maps(current_level, stens_sprite, karta_sprites, block_sprite)
    if dvij:
        # проверка столкновений мячика с стенами
        ball.vx, ball.vy = collide_stena(ball, stens_sprite)
        # проверка столкновений мячика с блоками
        ball.vx, ball.vy, score = collide_block(ball, block_sprite, score)
        # проверка столкновений
        score, dead = collisions(screen, ball, board, board_sprite, clock, fps, dead, karta_sprites, stens_sprite,
                                 block_sprite, score, current_level)
        # передвижение доски
        board.update()
        # передвижение мячика
        ball.update()
        # отображение жизней и счёта
        score_dead_count(dead, screen, heart, score, star)
        pygame.draw.line(screen, (128, 128, 128), (0, 47), (750, 47), 3)
        score, dead, current_level = win(screen, list_of_maps, block_sprite, current_level, ball, score, stens_sprite,
                                         karta_sprites, dead)
    else:
        # вывод на экран инструции до старта
        starts(screen)
    # прорисовка и обновление экрана
    pygame.display.flip()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    karta_sprites.draw(screen)
    clock.tick(fps)
# выход
pygame.quit()
