import os
import random


from buttons import Button
from Character import Character


class Enemy:
    def __init__(self, window_width, window_height):
        self.enemy_deck = []
        self.enemy_ch = []
        self.window_width = window_width
        self.window_height = window_height
        self.putted_amount = 0

    def fill_opponents_deck(self):
        if self.get_dif() == "Щадящий":
            counter = 0
            while counter != 8:
                temp = random.choice(os.listdir('resources/character'))
                if temp not in self.enemy_ch and Character(temp).frac[0] == "m" or Character(temp).frac[0] == "s":
                    self.enemy_ch.append(temp)
                    self.enemy_deck.append((Character(temp),
                                            Button(int(self.window_width / 2 + len(
                                                self.enemy_deck) * self.window_width / 15.52),
                                                   int(self.window_height / 100), int(self.window_width / 15.52),
                                                   int(self.window_height / 6.4), '',
                                                   f'resources/character/{temp}/image.png',
                                                   f'resources/character/{temp}/after.png',
                                                   f'resources/character/{temp}/sound.mp3')))
                    counter += 1
        elif self.get_dif() == "Ветеран":
            counter = 0
            while counter != 8:
                temp = random.choice(os.listdir('resources/character'))
                if temp not in self.enemy_ch and Character(temp).frac[0] != "m":
                    self.enemy_ch.append(temp)
                    self.enemy_deck.append((Character(temp),
                                            Button(int(self.window_width / 3.52 + len(self.enemy_deck) * self.window_width / 15.52),
                                                   int(self.window_height / 100), int(self.window_width / 15.52),
                                                   int(self.window_height / 6.4), '',
                                                   f'resources/character/{temp}/image.png',
                                                   f'resources/character/{temp}/after.png',
                                                   f'resources/character/{temp}/sound.mp3')))
                    counter += 1
        else:
            counter = 0
            while counter != 4:
                temp = random.choice(os.listdir('resources/character'))
                if temp not in self.enemy_ch and Character(temp).frac[0] != "m" and Character(temp).frac[0] != "s":
                    self.enemy_ch.append(temp)
                    self.enemy_deck.append((Character(temp),
                                            Button(int(self.window_width / 2 + len(
                                                self.enemy_deck) * self.window_width / 15.52),
                                                   int(self.window_height / 1.28), int(self.window_width / 15.52),
                                                   int(self.window_height / 6.4), '',
                                                   f'resources/character/{temp}/image.png',
                                                   f'resources/character/{temp}/after.png',
                                                   f'resources/character/{temp}/sound.mp3')))
                    counter += 1
            counter = 0
            while counter != 4:
                temp = random.choice(os.listdir('resources/character'))
                if temp not in self.enemy_ch and Character(temp).frac[0] == "s":
                    self.enemy_ch.append(temp)
                    self.enemy_deck.append((Character(temp),
                                            Button(int(self.window_width / 2 + len(
                                                self.enemy_deck) * self.window_width / 15.52),
                                                   int(self.window_height / 1.28), int(self.window_width / 15.52),
                                                   int(self.window_height / 6.4), '',
                                                   f'resources/character/{temp}/image.png',
                                                   f'resources/character/{temp}/after.png',
                                                   f'resources/character/{temp}/sound.mp3')))
                    counter += 1
        random.shuffle(self.enemy_deck)

    def put_opponents_card(self):
        card_to_put = self.enemy_deck[self.putted_amount]
        self.putted_amount += 1
        return card_to_put

    def get_dif(self):
        with open('resources/settings/difficulty.txt', mode="r", encoding="utf-8") as dif:
            return dif.readline().strip()
