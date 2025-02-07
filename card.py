# Создание класса карты
class Card:
    # функция инициализации
    def __init__(self, character, button):
        self.button, self.character = button, character
        
    # функция для получения характеристик карты или координат отрисовки 
    def __getitem__(self, item):
        if item == 0:
            return self.character
        else:
            return self.button

    # функция для отрисовки карты
    def draw(self, surface):
        self.button.draw(surface)

    # функция для отладки и тестирования
    def __str__(self):
        return self.character
