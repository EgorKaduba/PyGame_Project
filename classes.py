import pygame
from random import choice


# класс доски
class Board(pygame.sprite.Sprite):
    def __init__(self, board_sprite, left, r):
        super().__init__(board_sprite)
        self.right = r
        self.left = left
        # создание доски
        self.image = pygame.Surface((60, 10))
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 60, 10))
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 820
        self.is_paused = False

    # функция, перемещающая доску по экрану
    def update(self, pos=0):
        if not self.is_paused:
            # проверяем, находится ли курсор мыши внутри экрана
            mousefocus = pygame.mouse.get_focused()
            # если курсор не находится внутри экрана, перемещение происходит с помощью кнопок клавиатуры
            if pos == 0:
                if not mousefocus:
                    if self.rect.left >= 0:
                        if self.left:
                            self.rect = self.rect.move(-5, 0)
                    if self.rect.right <= 750:
                        if self.right:
                            self.rect = self.rect.move(5, 0)
            else:
                self.rect.x = pos if pos < 690 else 690


# класс мячика
class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_sprite):
        super().__init__(ball_sprite)
        # создание мячика внутри квадрата
        self.image = pygame.Surface((10, 10))
        pygame.draw.rect(self.image, (219, 112, 147), (0, 0, 10, 10))
        pygame.draw.circle(self.image, (255, 255, 255), (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.x = 370
        self.rect.y = 750
        self.vx = choice([-2, 2])
        self.vy = -2
        self.is_paused = False

    # функция, осуществляющая перемещение шарика
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)