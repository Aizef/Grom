# импорт библиотеки 
import pygame

# Создание класса кнопки
class Button:
    # функция инициализации
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=False,
                 is_on=None):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        self.is_on = is_on
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        self.is_hovered = False

    # функция для рендера кнопки
    def draw(self, screen, temp=0): 
        # если курсор на кнопке
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
            
        # меняем изображение кнопки при необходимости
        if temp == 1:
            current_image = self.hover_image

        elif temp == -1:
            current_image = self.image
            
        # отрисовка самой кнопки
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        screen.blit(current_image, self.rect.topleft)

        # возвращаем прежний шрифт, если до этого меняли на Arial
        if temp == 0:
            font = pygame.font.Font("resources/settings/font_settings/shrift.otf", int(open('resources/settings/font_settings/font_size.txt').read().strip()))
            text_surface = font.render(self.text, True, (255, 205, 234))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
            
        # меняем шрифт на Arial, если в тексте кнопки есть символы: '-=+-' и т.д. системный шрифт эти символы просто не поддерживает
        elif temp == 10:
            font = pygame.font.SysFont("Arial", int(open('resources/settings/font_settings/font_size.txt').read().strip()))
            text_surface = font.render(self.text, True, (255, 205, 234))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    # функция для запоминания положения курсора мыши
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    # функция для проигрывания звука при нажатии
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    # функция для проверки на наведение курсора мыши 
    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
        
    # для тестировки и отладки
    def __repr__(self):
        return f"X:{self.x}; W:{self.width}; H:{self.height}"
        
    # для тестировки и отладки
    def __str__(self):
        return f"X:{self.x}; W:{self.width}; H:{self.height}"

# Создание класса кнопки(для меню настроек)
class Settings_Button:
    # функция инициализации
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=False,
                 is_touchable=True):
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.is_touchable = is_touchable
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        self.is_hovered = False

    # функция для рендера кнопки
    def draw(self, screen, temp=0): 
        # если курсор на кнопке
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
            
        # меняем изображение кнопки при необходимости
        if temp == 1:
            temp = pygame.image.load("resources/pictures/after1.png")
            current_image = pygame.transform.scale(temp, (self.width, self.height))
        elif temp == -1:
            temp = pygame.image.load("resources/pictures/before.png")
            current_image = pygame.transform.scale(temp, (self.width, self.height))
            
        # отрисовка самой кнопки
        screen.blit(current_image, self.rect.topleft)
        font = pygame.font.Font('resources/settings/font_settings/shrift.otf', 20)
        text_surface = font.render(self.text, True, (255, 205, 234))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # функция для запоминания положения курсора мыши
    def check_hover(self, mouse_pos, event=None):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    # функция для проигрывания звука при нажатии
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    # функция для проверки на наведение курсора мыши 
    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
