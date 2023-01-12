import os
import pygame


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
def collisions(ball):
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
