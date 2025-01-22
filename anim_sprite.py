# Импорт библиотек
import os
import random

import pygame

# Настройка окна


# Функция загрузки изображения
def load_image(name, transparent=False):
    fullname = os.path.join('resources/pictures', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if transparent:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


# Класс анимированного персонажа
class AnimatedSprite(pygame.sprite.Sprite):
    # Функция инициализации
    def __init__(self, sheet, columns, rows, x, y, all_sprites):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.a = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    # Функция обрезки изображения с выделением кадров спрайта
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    # Функция обновления спрайта
    def update(self):
        self.cur_frame = (self.cur_frame + 1)
        self.image = self.frames[self.cur_frame % len(self.frames)]