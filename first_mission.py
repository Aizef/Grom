import json
import os
import sys
from random import choice

import pygame
from pygame import FULLSCREEN
import time

from buttons import Button
from character import Character
from statistic import Statistic_window
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
        self.settings = json.load(open("resources/settings/settings.json"))
        fps_status = self.settings['fps_status']
        if fps_status == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))
        self.comp = False
        #  рисуем окно настроек
        if self.settings['fullscreen_status']== 'True':
            self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_image = pygame.image.load("resources/pictures/table.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Миссии")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.change_counter = 5
        self.font = pygame.font.Font("resources/other/shrift.otf", 20)
        self.stat_health = self.font.render("", True, self.button_color)
        self.stat_name = self.font.render("", True, self.button_color)
        self.stat_damage = self.font.render("", True, self.button_color)
        self.stat_frac = self.font.render("", True, self.button_color)
        self.bot_damage_text = self.font.render("Ваш урон: 0", True, self.button_color)
        self.player_damage_text = self.font.render("Урон противника: 0", True, self.button_color)
        self.player_status = self.font.render("Обменяйте или выложите карту", True, self.button_color)
        # self.change_text = self.font.render(f"Обменов осталось: {self.change_counter}", True, self.button_color)
        self.null_everything()
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
        self.turn = True
        self.last_used_card = None
        self.stat_image = None
        self.action_button = Button(int(self.window_width / 36), int(self.window_height / 1.14),
                                    int(self.window_width / 5), int(self.window_height / 20),
                                    'Приступить к битве', 'resources/pictures/before.png',
                                    'resources/pictures/after.png', 'resources/sound/btn_on.mp3')

        enemy = Enemy(self.window_width, self.window_height)
        enemy.fill_opponents_deck("Щадящий")
        self.bots_deck = enemy.enemy_deck

        self.player_rows = [0, 0, 0]
        self.bot_rows = [0, 0, 0]
        self.bots_card_num = 0
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
                        self.member_change(self.change_counter)
                        self.change_counter = 0
                        self.player_status = self.font.render("Выложите карту", True, self.button_color)
                        # self.action_button.text = 'Выложите карту'
                    if self.change_counter == 0:
                        self.player_status = self.font.render("Выложите карту", True, self.button_color)
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
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.bot_rows[0]
            card_y = int(self.window_height / 3.73)
            self.bot_rows[0] += 1

        elif self.bots_deck[self.bots_card_num][0].frac[0] == "m":  # второй ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.bot_rows[1]
            card_y = int(self.window_height / 7)
            self.bot_rows[1] += 1

        else:  # третий ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.bot_rows[2]
            card_y = int(0)
            self.bot_rows[2] += 1

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
        for i in self.putted_card:
            i[1].draw(self.window)

        bots_frac = self.check_frac([i[0] for i in self.bots_putted_card])
        font = pygame.font.SysFont("Times New Roman", 40)
        if bots_frac["e"] >= 3 and "Я инженер — этим всё сказано!" not in self.used_bot_comb:
            self.player_damage = 0
            self.used_bot_comb.append("Я инженер — этим всё сказано!")
            text = font.render('Противник собрал комбинацию: "Я инженер — этим всё сказано!"', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
            text = font.render('Ваш урон уменьшен до 0', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
            pygame.display.flip()
            time.sleep(0.5)
        elif bots_frac["s"] >= 3 and "Ученье-свет!" not in self.used_bot_comb:
            self.player_health += 150
            self.used_bot_comb.append("Ученье-свет!")
            text = font.render('Противник собрал комбинацию: "Ученье-свет!"', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
            text = font.render('Здоровье противника увеличено на 150', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
            pygame.display.flip()
            time.sleep(0.5)
        elif bots_frac["m"] >= 3 and "Искалеченная плоть, искалеченная душа" not in self.used_bot_comb:
            self.used_bot_comb.append("Искалеченная плоть, искалеченная душа")
            self.player_damage += 100
            text = font.render('Урон противника увеличен на 100', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
            text = font.render('Противник собрал комбинацию: "Искалеченная плоть, искалеченная душа"', True,
                               self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
            pygame.display.flip()
            time.sleep(0.5)
        elif bots_frac["s"] >= 2 and bots_frac["m"] >= 2 and "Одна голова хорошо, а две — мутант!" not in self.used_bot_comb:
            self.used_bot_comb.append("Одна голова хорошо, а две — мутант!")
            self.bot_health += 200
            text = font.render('Здоровье противника увеличено на 200', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
            text = font.render('Противник собрал комбинацию: "Одна голова хорошо, а две — мутант!"', True,
                               self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
            pygame.display.flip()
            time.sleep(0.5)
        elif bots_frac["e"] >= 2 and (
                bots_frac["s"] >= 2 or bots_frac["m"] >= 2) and "Человек хуже мутанта, когда он мутант." not in self.used_bot_comb:
            self.used_bot_comb.append("Человек хуже мутанта, когда он мутант.")
            self.bot_damage += 350
            text = font.render('Урон противника увеличен на 350', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
            text = font.render('Противник собрал комбинацию: "Человек хуже мутанта, когда он мутант."', True,
                               self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
            pygame.display.flip()
            time.sleep(0.5)
        elif bots_frac["s"] >= 5 and "Плох тот ученый который не инженер" not in self.used_bot_comb:
            self.used_bot_comb.append("Плох тот ученый который не инженер")
            self.bot_health += 450
            text = font.render('Здоровье противника увеличено на 450', True, self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
            text = font.render('Противник собрал комбинацию: "Плох тот ученый который не инженер"', True,
                               self.button_color)
            self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
            pygame.display.flip()
            time.sleep(0.5)

        self.turn = True
        self.action_button.text = 'пас'
        if self.bots_card_num == len(self.bots_deck):
            self.over()
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
        self.window.blit(self.stat_name, (int(self.window_width / 7.5), int(self.window_height / 2.3)))
        self.window.blit(self.stat_health, (int(self.window_width / 7.5), int(self.window_height / 2.2)))
        self.window.blit(self.stat_damage, (int(self.window_width / 7.5), int(self.window_height / 2.1)))
        self.window.blit(self.stat_frac, (int(self.window_width / 7.5), int(self.window_height / 2)))
        self.window.blit(self.stat_frac, (int(self.window_width), int(self.window_height / 1.9)))
        self.player_health_text = self.font.render(f"Ваше здоровье: {self.player_health}", True, self.button_color)
        self.bot_health_text = self.font.render(f"Здоровье противника:{self.bot_health}", True, self.button_color)
        self.bot_damage_text = self.font.render(f"Урон противника: {self.bot_damage}", True, self.button_color)
        self.player_damage_text = self.font.render(f"Ваш урон: {self.player_damage}", True, self.button_color)
        # self.change_text = self.font.render(f"Обменов осталось: {self.change_counter}", True, self.button_color)
        self.window.blit(self.bot_damage_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 100)))
        self.window.blit(self.player_damage_text, (int(self.window_width / 1.25), int(self.window_height / 1.8)))
        self.change_player_status()
        self.window.blit(self.player_status, (int(self.window_width / 36), int(self.window_height / 1.24)))
        self.window.blit(self.bot_health_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 200)))
        self.window.blit(self.player_health_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 300)))
        # self.window.blit(self.change_text, (int(self.window_width / 1.25), int(self.window_height / 1.8 - 400)))
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
                card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.player_rows[0]
                card_y = int(self.window_height / 2.4 + 10)
                self.player_rows[0] += 1
            elif self.deck[i][0].frac[0] == "m":  # второй ряд
                card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.player_rows[1]
                card_y = int(self.window_height / 1.8 - 1)
                self.player_rows[1] += 1

            else:  # третий ряд
                card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.player_rows[2]
                card_y = int(self.window_height / 1.48 + 30)
                self.player_rows[2] += 1

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
            a = self.check_frac([i[0] for i in self.putted_card])
            font = pygame.font.SysFont("Times New Roman", 40)
            if a["e"] >= 3 and "Я инженер — этим всё сказано!" not in self.used_comb:
                self.bot_damage = 0
                self.used_comb.append("Я инженер — этим всё сказано!")
                text = font.render('Вы собрали комбинацию: "Я инженер — этим всё сказано!"', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                text = font.render('Урон противника уменьшен до 0', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                pygame.display.flip()
                time.sleep(1.5)
            elif a["s"] >= 3 and "Ученье-свет!" not in self.used_comb:
                self.player_health += 150
                self.used_comb.append("Ученье-свет!")
                text = font.render('Вы собрали комбинацию: "Ученье-свет!"', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                text = font.render('Ваше здоровье увеличено на 150', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                pygame.display.flip()
                time.sleep(1.5)
            elif a["m"] >= 3 and "Искалеченная плоть, искалеченная душа" not in self.used_comb:
                self.used_comb.append("Искалеченная плоть, искалеченная душа")
                self.player_damage += 100
                text = font.render('Ваш урон увеличен на 100', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Вы собрали комбинацию: "Искалеченная плоть, искалеченная душа"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                pygame.display.flip()
                time.sleep(1.5)
            elif a["s"] >= 2 and a["m"] >= 2 and "Одна голова хорошо, а две — мутант!" not in self.used_comb:
                self.used_comb.append("Одна голова хорошо, а две — мутант!")
                self.player_health += 200
                text = font.render('Ваше здоровье увеличено на 200', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Вы собрали комбинацию: "Одна голова хорошо, а две — мутант!"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                pygame.display.flip()
                time.sleep(1.5)
            elif a["e"] >= 2 and (
                    a["s"] >= 2 or a["m"] >= 2) and "Человек хуже мутанта, когда он мутант." not in self.used_comb:
                self.used_comb.append("Человек хуже мутанта, когда он мутант.")
                self.player_damage += 350
                text = font.render('Ваш урон увеличен на 350', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Вы собрали комбинацию: "Человек хуже мутанта, когда он мутант."', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                pygame.display.flip()
                time.sleep(1.5)
            elif a["s"] >= 5 and "Плох тот ученый который не инженер" not in self.used_comb:
                self.used_comb.append("Плох тот ученый который не инженер")
                self.player_health += 450
                text = font.render('Ваше здоровье увеличено на 450', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Вы собрали комбинацию: "Плох тот ученый который не инженер"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                pygame.display.flip()
                time.sleep(1.5)

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
        enemy.fill_opponents_deck("Щадящий")
        self.bots_deck = enemy.enemy_deck
        try:
            if self.change_counter != 0 or self.change_counter != 5:
                self.change_counter = self.change_mem
        except AttributeError as ae:
            pass
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
        self.null_everything()
        self.action_button.text = "Приступить к битве"
        self.player_status = self.player_status = self.font.render("Обменяйте или выложите карту", True,
                                                                   self.button_color)
        self.redrawing()

    def get_fps_result(self):
        return self.settings['fps_status']

    def finish(self):
        Stat = Statistic_window(self.window_width, self.window_height, self.window, self.previous_object, self.stat,
                                self.comp)
        Stat.open()

    def member_change(self, arg):
        self.change_mem = arg

    def change_player_status(self):
        if not self.turn:
            self.player_status = self.font.render("Ожидайте хода противника", True, self.button_color)
        if sum(self.bot_rows) != 0 and self.turn:
            self.player_status = self.font.render("Выложите карту", True, self.button_color)

    def null_everything(self):
        self.putted_card = []
        self.used_comb = []
        self.used_bot_comb = []
        self.bots_card_num = 0
        self.player_rows = [0, 0, 0]
        self.bot_rows = [0, 0, 0]
        self.player_damage = 0
        self.bot_damage = 0
        self.player_health = 0
        self.bot_health = 0

        self.turn = True

    def check_frac(self, arg):
        result = {"m": 0, "s": 0, "e": 0}
        for i in arg:
            if i.frac[0].lower() == "m":
                result["m"] += 1
            elif i.frac[0].lower() == "s":
                result["s"] += 1
            elif i.frac[0].lower() == "e":
                result["e"] += 1
        return result
