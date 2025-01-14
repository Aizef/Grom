import os
import sys
from random import choice

import pygame
from pygame import FULLSCREEN
import time

from buttons import Button
from character import Character
from Statistic import Statistic_window
from enemy import Enemy

class First_mission:
    def __init__(self, window_width, window_height, screen, pr):
        pygame.init()
        pygame.display.set_caption('Миссия первая')
        self.window_width = window_width
        self.window_height = window_height
        self.previous_object = pr
        self.grom_clock = pygame.time.Clock()
        self.font = pygame.font.Font('resources/other/shrift.otf', 18)

        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            fps_status = fps_file.readline().strip()
        if fps_status == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))
        self.comp = False
        #  рисуем окно настроек
        if open('resources/settings/fullscreen_status.txt').read().strip() == 'True':
            self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_image = pygame.image.load("resources/pictures/table.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Миссии")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.font = pygame.font.Font("resources/other/shrift.otf", 20)
        self.stat_health = self.font.render("", True, self.button_color)
        self.stat_name = self.font.render("", True, self.button_color)
        self.stat_damage = self.font.render("", True, self.button_color)
        self.stat_frac = self.font.render("", True, self.button_color)
        self.bot_damage_text = self.font.render("Ваш урон: 0", True, self.button_color)
        self.player_damage_text = self.font.render("Урон противника: 0", True, self.button_color)
        self.bot_damage = 0
        self.player_damage = 0
        self.bot_health = 0
        self.player_health = 0
        self.previous_screen = screen
        #  рендер окна
        self.previous_screen.blit(self.window, (0, 0))
        pygame.display.flip()
        self.back_button = Button(self.window_width - self.window_width // 10, 0, self.window_width // 10, 100,
                                  'Сдаться', 'resources/pictures/before.png', 'resources/pictures/after.png',
                                  'resources/sound/btn_on.mp3')
        self.deck = []
        self.putted_card = []
        self.ch = []

        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch:
                self.ch.append(temp)
                self.deck.append((Character(temp),
                                  Button(int(self.window_width / 3.52 + len(self.deck) * self.window_width / 15.52),
                                         int(self.window_height / 1.21), int(self.window_width / 15.52),
                                         int(self.window_height / 6.4), '', f'resources/character/{temp}/image.png',
                                         f'resources/character/{temp}/after.png',
                                         f'resources/character/{temp}/sound.mp3')))
            if len(self.deck) == 8:
                break
        self.change_counter = 3
        self.turn = True
        self.last_used_card = None
        self.stat_image = None
        self.action_button = Button(int(self.window_width / 36), int(self.window_height / 1.24),
                                    int(self.window_width / 5), int(self.window_height / 20),
                                    'Приступить к битве', 'resources/pictures/before.png',
                                    'resources/pictures/after.png', 'resources/sound/btn_on.mp3')

        enemy = Enemy(self.window_width, self.window_height)
        enemy.fill_opponents_deck()
        self.bots_deck = enemy.enemy_deck

        self.count_e = 0
        self.count_m = 0
        self.count_s = 0
        self.count_e_bots = 0
        self.count_m_bots = 0
        self.bots_card_num = 0
        self.count_s_bots = 0
        self.bots_putted_card = []
        self.pas = False
        self.player_hearts = 2
        self.bots_hearts = 2
        self.stat = {'bots_putted_card': 0, 'players_putted_car': 0, 'bots_summary_damage': 0,
                     'players_summary_damage': 0, 'bots_summary_health': 0, 'players_summary_health': 0}

    def open(self):
        running = True
        while running:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_hovered:
                        self.back()
                    for i in range(len(self.deck)):
                        if self.deck[i][1].is_hovered and self.change_counter != 0:  # фаза замены
                            self.change(i)
                        elif self.deck[i][1].is_hovered and self.turn == True:
                            self.put_card(i)
                    if self.action_button.is_hovered and self.turn and self.change_counter != 0:
                        self.change_counter = 0
                        self.action_button.text = 'Выложите карту'
                    if self.action_button.text == 'пас' and self.action_button.is_hovered:
                        self.bot_final_turn()

                for i in self.deck:
                    if i[1].is_hovered:
                        self.stat_name = self.font.render(f"Имя: {i[0].name}", True, self.button_color)
                        self.stat_health = self.font.render(f"Здоровье: {i[0].health}", True, self.button_color)
                        self.stat_image = Button(int(self.window_width / 15), int(self.window_height / 2.3),
                                                 int(self.window_width / 15.52), int(self.window_height / 6.4), '',
                                                 f'resources/character/{i[0].path}/image.png')
                        self.stat_damage = self.font.render(f"Урон: {i[0].damage}", True, self.button_color)
                        self.stat_frac = self.font.render(f"Фракция: {i[0].frac}", True, self.button_color)

            self.grom_clock.tick(90)
            if self.get_fps_result() == "True":
                self.grom_text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True,
                                                           (255, 205, 234))
            else:
                self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

            self.back_button.check_hover(pos)

            self.action_button.check_hover(pos)

            for i in self.deck:
                i[1].check_hover(pos)
            self.redrawing()

    def back(self):
        self.previous_object.open(True)

    def bot_final_turn(self):
        while (self.player_health - self.bot_damage > self.bot_health - self.player_damage) or self.stat[
            'bots_putted_card'] == 8:
            self.bot_turn()
            if self.bots_putted_card:
                for i in self.bots_putted_card:
                    i[1].draw(self.window)
            pygame.display.flip()
            self.turn = False
        if self.player_health - self.bot_damage <= self.bot_health - self.player_damage:
            time.sleep(0.5)
            self.over()

    def bot_turn(self):
        temp = self.bots_deck[self.bots_card_num][0].path
        self.stat['bots_putted_card'] += 1

        if self.bots_deck[self.bots_card_num][0].frac[0] == "s":  # первый ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.count_s_bots
            card_y = int(self.window_height / 3.73)
            self.count_s_bots += 1

        elif self.bots_deck[self.bots_card_num][0].frac[0] == "m":  # второй ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.count_m_bots
            card_y = int(self.window_height / 7)
            self.count_m_bots += 1

        else:  # третий ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.count_e_bots
            card_y = int(0)
            self.count_e_bots += 1

        self.bot_health += int(self.bots_deck[self.bots_card_num][0].health)
        self.bot_damage += int(self.bots_deck[self.bots_card_num][0].damage)
        self.bots_deck[self.bots_card_num] = (
            (Character(temp, True),
             Button(int(self.window_width / 3.52 + self.bots_card_num * self.window_width / 15.52),
                    int(self.window_height / 1.21), int(self.window_width / 15.52),
                    int(self.window_height / 6.4), '',
                    f'resources/character/{temp}/used.png',
                    f'resources/character/{temp}/used.png')))

        self.bots_putted_card.append((self.bots_deck[self.bots_card_num][0], Button(card_x, card_y,
                                                                                    int(self.window_width / 15.52),
                                                                                    int(self.window_height / 8.4),
                                                                                    '',
                                                                                    f'resources/character/{temp}/image.png',
                                                                                    f'resources/character/{temp}/after.png',
                                                                                    f'resources/character/{temp}/sound.mp3')))
        self.bots_card_num += 1
        if self.bots_card_num == len(self.bots_deck):
            self.over()
        self.turn = True
        self.action_button.text = 'пас'
        time.sleep(0.3)

    def change(self, num):
        self.last_used_card = Button(
            int(self.window_width / 3.45 + len(self.deck) * self.window_width / 15.52),
            int(self.window_height / 1.28), int(self.window_width / 15.52),
            int(self.window_height / 6.4), '', self.deck[num][0].used_image, self.deck[num][0].used_image)
        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch:
                self.ch[num] = temp
                self.deck[num] = ((Character(temp),
                                   Button(int(self.window_width / 3.52 + num * self.window_width / 15.52),
                                          int(self.window_height / 1.21), int(self.window_width / 15.52),
                                          int(self.window_height / 6.4), '', f'resources/character/{temp}/image.png',
                                          f'resources/character/{temp}/after.png',
                                          f'resources/character/{temp}/sound.mp3')))
                break
        self.change_counter -= 1
        self.redrawing()

    def redrawing(self):
        self.window.blit(self.background_image, (0, 0))
        self.window.blit(self.stat_name, (int(self.window_width / 7.5), int(self.window_height / 2.1)))
        self.window.blit(self.stat_health, (int(self.window_width / 7.5), int(self.window_height / 2)))
        self.window.blit(self.stat_damage, (int(self.window_width / 7.5), int(self.window_height / 1.9)))
        self.window.blit(self.stat_frac, (int(self.window_width / 7.5), int(self.window_height / 1.8)))
        self.window.blit(self.stat_frac, (int(self.window_width), int(self.window_height / 1.8)))
        self.player_health_text = self.font.render(f"Ваше здоровье: {self.player_health}", True, self.button_color)
        self.bot_health_text = self.font.render(f"Здоровье противника:{self.bot_health}", True, self.button_color)
        self.bot_damage_text = self.font.render(f"Ваш урон: {self.player_damage}", True, self.button_color)
        self.player_damage_text = self.font.render(f"Урон противника: {self.bot_damage}", True, self.button_color)
        self.window.blit(self.bot_damage_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 100)))
        self.window.blit(self.player_damage_text, (int(self.window_width / 1.25), int(self.window_height / 1.8)))
        self.window.blit(self.bot_health_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 200)))
        self.window.blit(self.player_health_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 300)))
        self.back_button.draw(self.window)
        for i in self.deck:
            i[1].draw(self.window)
        self.action_button.draw(self.window)

        if self.putted_card:
            for i in self.putted_card:
                i[1].draw(self.window)
        if self.get_fps_result() == "True":
            self.window.blit(self.grom_text_show_fps, (0, 0))
        if self.last_used_card is not None:
            self.last_used_card.draw(self.window)
        if self.stat_image is not None:
            self.stat_image.draw(self.window)
        if self.bots_putted_card:
            for i in self.bots_putted_card:
                i[1].draw(self.window)
        pygame.display.flip()

    def put_card(self, i):
        if self.deck[i][0].used is False:
            temp = self.deck[i][0].path
            if self.deck[i][0].frac[0] == "s":  # первый ряд
                card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.count_s
                card_y = int(self.window_height / 2.4 + 10)
                self.count_s += 1
            elif self.deck[i][0].frac[0] == "m":  # второй ряд
                card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.count_m
                card_y = int(self.window_height / 1.8 - 1)
                self.count_m += 1

            else:  # третий ряд
                card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.count_e
                card_y = int(self.window_height / 1.48 + 30)
                self.count_e += 1

            self.player_damage += int(Character(temp).damage)
            self.player_health += int(Character(temp).health)
            self.deck[i] = (
                (Character(temp, True), Button(int(self.window_width / 3.52 + i * self.window_width / 15.52),
                                               int(self.window_height / 1.19), int(self.window_width / 15.52),
                                               int(self.window_height / 6.4), '',
                                               f'resources/character/{temp}/used.png',
                                               f'resources/character/{temp}/used.png')))

            self.putted_card.append((self.deck[i][0], Button(card_x, card_y,
                                                             int(self.window_width / 15.52),
                                                             int(self.window_height / 8.4),
                                                             '',
                                                             f'resources/character/{temp}/image.png',
                                                             f'resources/character/{temp}/after.png',
                                                             f'resources/character/{temp}/sound.mp3')))
            for i in self.putted_card:
                i[1].draw(self.window)
            self.turn = False
            self.redrawing()
            self.stat['players_putted_car'] += 1
            self.bot_turn()

    def over(self):
        self.stat['bots_summary_damage'] += self.bot_damage
        self.stat['players_summary_damage'] += self.player_damage
        self.stat['bots_summary_health'] += self.bot_health
        self.stat['players_summary_health'] += self.player_health

        font = pygame.font.Font("resources/other/shrift.otf", 40)
        if self.player_health - self.bot_damage <= self.bot_health - self.player_damage:
            result = font.render('Вы потеряли жизнь', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3), int(self.window_height / 2.5)))
            self.player_hearts -= 1
            pygame.display.flip()
            time.sleep(0.5)
        else:
            result = font.render('Противник потерял жизнь', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3), int(self.window_height / 2.5)))
            self.bots_hearts -= 1
            pygame.display.flip()
            time.sleep(0.5)

        if self.player_hearts == 0:
            self.comp = False
            result = font.render('Вы проиграли', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3), int(self.window_height / 2.5)))
            time.sleep(1)
            self.finish()
        elif self.bots_hearts == 0:
            self.comp = True
            result = font.render('Вы Выиграли', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3), int(self.window_height / 2.5)))
            time.sleep(1)
            self.finish()

        enemy = Enemy(self.window_width, self.window_height)
        enemy.fill_opponents_deck()
        self.bots_deck = enemy.enemy_deck
        self.putted_card = []
        self.bots_card_num = 0
        self.count_e = 0
        self.count_m = 0
        self.count_s = 0
        self.count_e_bots = 0
        self.count_m_bots = 0
        self.count_s_bots = 0
        self.bots_putted_card = []
        self.pas = False
        self.new_deck = []
        for i in self.deck:
            if not i[0].used:
                self.new_deck.append(i)
        self.deck = []
        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch:
                self.ch.append(temp)
                self.new_deck.append((Character(temp),
                                      Button(int(0),
                                             int(self.window_height / 1.21), int(self.window_width / 15.52),
                                             int(self.window_height / 6.4), '', f'resources/character/{temp}/image.png',
                                             f'resources/character/{temp}/after.png',
                                             f'resources/character/{temp}/sound.mp3')))
            if len(self.new_deck) == 8:
                break
        counter = 0
        for i in self.new_deck:
            i[1].x = int(self.window_width / 3.52 + counter * self.window_width / 15.52)
            self.deck.append(i)
            i[1].draw(self.window)
            counter += 1
        self.player_damage = 0
        self.bot_damage = 0
        self.player_health = 0
        self.bot_health = 0

        self.turn = True
        self.redrawing()

    def get_fps_result(self):
        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            return fps_file.readline().strip()

    def finish(self):
        Stat = Statistic_window(self.window_width, self.window_height, self.window, self.previous_object, self.stat,
                                self.comp)
        Stat.open()
