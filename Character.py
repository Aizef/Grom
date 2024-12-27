import codecs
import json


class Character:
    def __init__(self, path, used=False):
        self.before_image = f'resources/character/{path}/image.png'
        self.after_image = f'resources/character/{path}/after.png'
        self.name = codecs.open(f'resources/character/{path}/characteristic.txt', "r", "utf-8").readlines()[0].strip().split(':')[1]
        self.health = codecs.open(f'resources/character/{path}/characteristic.txt', "r", "utf-8").readlines()[1].strip().split(':')[1]
        self.sound = f'resources/character/{path}/sound.mp3'
        self.used = used
        self.path = path