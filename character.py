# импорт библиотек
import codecs

# создание класса персонажа
class Character:
    # функция инициализации и запоминания всего необходимого
    def __init__(self, path, used=False):
        self.before_image = f'resources/character/{path}/image.png'
        self.after_image = f'resources/character/{path}/after.png'
        
        self.name = \
            codecs.open(f'resources/character/{path}/characteristic.txt', "r", "utf-8").readlines()[0].strip().split(
                ':')[1]
        self.health = \
            codecs.open(f'resources/character/{path}/characteristic.txt', "r", "utf-8").readlines()[1].strip().split(
                ':')[1]
        
        self.sound = f'resources/character/{path}/sound.mp3'
        self.used_image = f'resources/character/{path}/used.png'
        self.used = used
        self.path = path

        self.damage = \
            codecs.open(f'resources/character/{path}/characteristic.txt', "r", "utf-8").readlines()[-2].split(":")[
                -2].strip()
        self.frac = \
            codecs.open(f'resources/character/{path}/characteristic.txt', "r", "utf-8").readlines()[-1].split(":")[
                -2].strip()
        
    # функция для тестирования и отладки
    def __str__(self):
        return f"Name:{self.name}"

    # функция для тестирования и отладки
    def __repr__(self):
        return f"Name:{self.name}"
