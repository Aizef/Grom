import ctypes
import json
import os
import sys
from random import choice

import pygame
from pygame import FULLSCREEN
import time

from сard import Card
from anim_sprite import AnimatedSprite, load_image
from buttons import Button
from character import Character
from statistic import Statistic_window
from enemy import Enemy


class Mission:
    def __init__(self, window_width, window_height, screen, pr, dif, n, bi_path):
        pygame.init()
        self.dif = dif
        self.bi = bi_path
        if self.dif.lower() == "щадящий":
            pygame.mixer.music.load("resources/sound/first_mis.mp3")
            pygame.mixer.music.play(-1)
        elif self.dif.lower() == "ветеран":
            pygame.mixer.music.load("resources/sound/sec_mis.mp3")
            pygame.mixer.music.play(-1)
        elif self.dif.lower() == "ангел смерти":
            pygame.mixer.music.load("resources/sound/third_mis.mp3")
            pygame.mixer.music.play(-1)
        pygame.display.set_caption(f'Миссия под номером: {n}')
        self.all_sprites = pygame.sprite.Group()
        self.bots_health = AnimatedSprite(load_image("heart.png", True), 5, 1, window_width // 7.2,
                                          window_height // 3.85,
                                          self.all_sprites, 10)
        self.players_health = AnimatedSprite(load_image("heart.png", True), 5, 1, window_width // 7.2,
                                             window_height // 1.54,
                                             self.all_sprites, 10)

        self.explosion = None

        self.window_width = window_width
        self.window_height = window_height
        self.previous_object = pr
        self.grom_clock = pygame.time.Clock()
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.shrift_coefficient = 35 * self.window_width * self.window_height // user32.GetSystemMetrics(
            0) // user32.GetSystemMetrics(1)
        self.font = pygame.font.Font("resources/settings/font_settings/shrift.otf",  self.shrift_coefficient)
        self.settings = json.load(open("resources/settings/settings.json"))
        fps_status = self.settings['fps_status']
        if fps_status == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))
        self.comp = None
        #  рисуем окно настроек
        if self.settings['fullscreen_status'] == 'True':
            self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_image = pygame.image.load(f"resources/pictures/{self.bi}").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Миссии")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.change_counter = 5
        self.font = pygame.font.Font("resources/settings/font_settings/shrift.otf", self.shrift_coefficient // 2)
        self.stat_health = self.font.render("", True, self.button_color)
        self.stat_name = self.font.render("", True, self.button_color)
        self.stat_damage = self.font.render("", True, self.button_color)
        self.stat_frac = self.font.render("", True, self.button_color)
        self.player_health_text = self.font.render("Ваше здоровье: 0", True, self.button_color)
        self.bot_health_text = self.font.render("Здоровье противника: 0", True, self.button_color)
        self.bot_damage_text = self.font.render("Ваш урон: 0", True, self.button_color)
        self.player_damage_text = self.font.render("Урон противника: 0", True, self.button_color)
        self.player_status = self.font.render("Обменяйте или выложите карту", True, self.button_color)
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

        self.putted_spy = []
        self.dead_card = []

        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch and temp != 'question':
                self.ch.append(temp)
                self.deck.append(Card(Character(temp),
                                      Button(int(self.window_width / 4.22 + len(self.deck) * self.window_width / 15.52),
                                             int(self.window_height / 1.21), int(self.window_width / 15.52),
                                             int(self.window_height / 6.4), '', f'resources/character/{temp}/image.png',
                                             f'resources/character/{temp}/after.png',
                                             f'resources/character/{temp}/sound.mp3')))
            if len(self.deck) == 10:
                break
        self.turn = True
        self.last_used_card = None
        self.stat_image = None
        self.action_button = Button(int(self.window_width / 36), int(self.window_height / 1.14),
                                    int(self.window_width / 5), int(self.window_height / 20),
                                    'Приступить к битве', 'resources/pictures/before.png',
                                    'resources/pictures/after.png', 'resources/sound/btn_on.mp3')

        enemy = Enemy(self.window_width, self.window_height)
        enemy.fill_opponents_deck(self.dif)
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
        if self.dif == 'Ангел Смерти':
            temp = 'question'
        self.next_bot_card = Card(Character(temp), Button(int(self.window_width / 1.25), int(self.window_height / 19),
                                                          int(self.window_width / 15.52),
                                                          int(self.window_height / 6.4), '',
                                                          f'resources/character/{temp}/image.png',
                                                          f'resources/character/{temp}/after.png',
                                                          f'resources/character/{temp}/sound.mp3'))

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
                        if i < len(self.deck):
                            if self.deck[i][1].is_hovered and self.change_counter != 0:  # фаза замены
                                self.change(i)
                            elif self.deck[i][1].is_hovered and self.turn == True:
                                self.put_card(i)
                    if self.action_button.is_hovered and self.turn and self.change_counter != 0:
                        self.member_change(self.change_counter)
                        self.change_counter = 0
                        self.player_status = self.font.render("Выложите карту", True, self.button_color)
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
                if self.next_bot_card[1].is_hovered:
                    self.stat_name = self.font.render(f"Имя: {self.next_bot_card[0].name}", True, self.button_color)
                    self.stat_health = self.font.render(f"Здоровье: {self.next_bot_card[0].health}", True,
                                                        self.button_color)
                    self.stat_image = Button(int(self.window_width / 15), int(self.window_height / 2.3),
                                             int(self.window_width / 15.52), int(self.window_height / 6.4), '',
                                             f'resources/character/{self.next_bot_card[0].path}/image.png')
                    self.stat_damage = self.font.render(f"Урон: {self.next_bot_card[0].damage}", True,
                                                        self.button_color)
                    self.stat_frac = self.font.render(f"Фракция: {self.next_bot_card[0].frac}", True, self.button_color)

            self.grom_clock.tick(90)
            if self.get_fps_result() == "True":
                self.grom_text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True,
                                                           (255, 205, 234))
            else:
                self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

            self.back_button.check_hover(pos)
            self.next_bot_card[1].check_hover(pos)

            self.action_button.check_hover(pos)

            for i in self.deck:
                i[1].check_hover(pos)

            self.redrawing()
            if len(self.putted_card) == len(self.deck) and self.comp != False:
                self.over()

    def back(self):
        self.previous_object.open(True)

    def bot_final_turn(self):
        if len(self.bots_deck) != len(self.bots_putted_card):
            while (self.player_health - self.bot_damage > self.bot_health - self.player_damage) or self.stat[
                'bots_putted_card'] == 15:
                self.bot_turn()
                if self.bots_putted_card:
                    for i in self.bots_putted_card:
                        i[1].draw(self.window)
                pygame.display.flip()
                self.turn = False
            if self.player_health - self.bot_damage <= self.bot_health - self.player_damage:
                time.sleep(0.4)
                self.over()
        else:
            self.over()

    def bot_turn(self):
        try:
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

            if self.bots_deck[self.bots_card_num][0].name == 'Казнь':
                self.card_to_kill()

            self.bots_deck[self.bots_card_num] = (Card
                                                  (Character(temp, True),
                                                   Button(
                                                       int(self.window_width / 3.52 + self.bots_card_num * self.window_width / 15.52),
                                                       int(self.window_height / 1.21), int(self.window_width / 15.52),
                                                       int(self.window_height / 6.4), '',
                                                       f'resources/character/{temp}/used.png',
                                                       f'resources/character/{temp}/used.png')))

            self.bots_putted_card.append(Card(self.bots_deck[self.bots_card_num][0], Button(card_x, card_y,
                                                                                            int(self.window_width / 15.52),
                                                                                            int(self.window_height / 8.4),
                                                                                            '',
                                                                                            f'resources/character/{temp}/image.png',
                                                                                            f'resources/character/{temp}/after.png',

                                                                                            f'resources/character/{temp}/sound.mp3')))
            try:
                if self.dif != 'Ангел Смерти':
                    temp = self.bots_deck[self.bots_card_num + 1][0].path
                    self.next_bot_card = Card(Character(temp),
                                              Button(int(self.window_width / 1.25), int(self.window_height / 19),
                                                     int(self.window_width / 15.52),
                                                     int(self.window_height / 6.4), '',
                                                     f'resources/character/{temp}/image.png',
                                                     f'resources/character/{temp}/after.png',
                                                     f'resources/character/{temp}/sound.mp3'))
            except IndexError:
                pass
            self.bots_card_num += 1
            for i in self.putted_card:
                i[1].draw(self.window)
            time.sleep(0.3)
            self.redrawing()
            pygame.display.flip()
            time.sleep(0.1)
            bots_frac = self.check_frac([i[0] for i in self.bots_putted_card])
            font = pygame.font.SysFont("Times new roman", int(self.shrift_coefficient))

            if bots_frac["e"] >= 3 and "Я инженер — этим всё сказано!" not in self.used_bot_comb:
                self.player_damage = 0
                self.used_bot_comb.append("Я инженер — этим всё сказано!")
                text = font.render('Противник собрал комбинацию: "Я инженер — этим всё сказано!"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                text = font.render('Ваш урон уменьшен до 0', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                self.draw_board()
                time.sleep(0.5)
            elif bots_frac["s"] >= 3 and "Ученье-свет!" not in self.used_bot_comb:
                self.bot_health += 150
                self.used_bot_comb.append("Ученье-свет!")
                text = font.render('Противник собрал комбинацию: "Ученье-свет!"', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                text = font.render('Здоровье противника увеличено на 150', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                self.draw_board()
                time.sleep(0.5)
            elif bots_frac["m"] >= 3 and "Искалеченная плоть, искалеченная душа" not in self.used_bot_comb:
                self.used_bot_comb.append("Искалеченная плоть, искалеченная душа")
                self.bot_damage += 100
                text = font.render('Урон противника увеличен на 100', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Противник собрал комбинацию: "Искалеченная плоть искалеченная душа"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                self.draw_board()
                time.sleep(0.5)
            elif bots_frac["s"] >= 2 and bots_frac[
                "m"] >= 2 and "Одна голова хорошо, а две — мутант!" not in self.used_bot_comb:
                self.used_bot_comb.append("Одна голова хорошо, а две — мутант!")
                self.bot_health += 200
                text = font.render('Здоровье противника увеличено на 200', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Противник собрал комбинацию: "Одна голова хорошо а две — мутант!"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                self.draw_board()
                time.sleep(0.5)
            elif bots_frac["e"] >= 2 and (
                    bots_frac["s"] >= 2 or bots_frac[
                "m"] >= 2) and "Человек хуже мутанта, когда он мутант." not in self.used_bot_comb:
                self.used_bot_comb.append("Человек хуже мутанта, когда он мутант.")
                self.bot_damage += 300
                text = font.render('Урон противника увеличен на 350', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Противник собрал комбинацию: "Человек хуже мутанта когда он мутант."', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                self.draw_board()
                time.sleep(0.5)
            elif bots_frac["s"] >= 5 and "Плох тот ученый который не инженер" not in self.used_bot_comb:
                self.used_bot_comb.append("Плох тот ученый который не инженер")
                self.bot_health += 350
                text = font.render('Здоровье противника увеличено на 450', True, self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                text = font.render('Противник собрал комбинацию: "Плох тот ученый который не инженер"', True,
                                   self.button_color)
                self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                self.draw_board()
                time.sleep(0.5)
        except IndexError:
            pass
        self.turn = True
        self.action_button.text = 'пас'
        if self.bots_card_num == len(self.bots_deck) - 1:
            font = pygame.font.Font("resources/settings/font_settings/shrift.otf", self.shrift_coefficient)
            result = font.render('Противник проиграл из-за недостатка карт', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3.1), int(self.window_height / 2.8)))
            pygame.display.flip()
            time.sleep(1)
            self.bots_hearts = 0
            self.comp = True
            self.open()

    def change(self, num):
        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch and temp != 'question':
                self.ch[num] = temp
                self.deck[num] = (Card(Character(temp),
                                       Button(int(self.window_width / 4.22 + num * self.window_width / 15.52),
                                              int(self.window_height / 1.21), int(self.window_width / 15.52),
                                              int(self.window_height / 6.4), '',
                                              f'resources/character/{temp}/image.png',
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

        self.window.blit(self.bot_damage_text, (int(self.window_width / 100), int(self.window_height / 7)))
        self.window.blit(self.player_damage_text, (int(self.window_width / 100), int(self.window_height / 6)))
        self.change_player_status()
        self.window.blit(self.player_status, (int(self.window_width / 36), int(self.window_height / 1.24)))
        self.window.blit(self.bot_health_text, (int(self.window_width / 100), int(self.window_height / 5.25)))
        self.window.blit(self.player_health_text, (int(self.window_width / 100), int(self.window_height / 4.5)))
        self.back_button.draw(self.window)

        for i in self.deck:
            i[1].draw(self.window)
        for i in self.putted_spy:
            i[1].draw(self.window)
        self.action_button.draw(self.window)
        self.next_bot_card[1].draw(self.window)

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

        if self.bots_hearts == 1 and self.bots_health.cur_frame < 20:
            self.bots_health.update()

        if self.player_hearts == 1 and self.players_health.cur_frame < 20:
            self.players_health.update()

        if self.bots_hearts == 0 and self.bots_health.cur_frame < 50:
            self.bots_health.update()

        if self.player_hearts == 0 and self.players_health.cur_frame < 50:
            self.players_health.update()

        if self.explosion != None and self.explosion.cur_frame < self.explosion.slower * self.explosion.columns:
            self.explosion.update()

        if self.explosion != None and self.explosion.cur_frame == self.explosion.slower * self.explosion.columns - 1:
            self.explosion.kill()
            self.explosion = None

        self.all_sprites.draw(self.window)
        pygame.display.flip()

        if self.players_health.cur_frame == self.players_health.slower * self.players_health.columns - 1 or self.bots_health.cur_frame == self.bots_health.slower * self.bots_health.columns - 1:
            self.finish()

    def put_card(self, i):
        if self.deck[i][0].used is False:
            if not self.check_spy(self.deck[i]):
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
                self.deck[i] = (Card
                                (Character(temp, True),
                                 Button(int(self.window_width / 4.22 + i * self.window_width / 15.52),
                                        int(self.window_height / 1.19), int(self.window_width / 15.52),
                                        int(self.window_height / 6.4), '',
                                        f'resources/character/{temp}/used.png',
                                        f'resources/character/{temp}/used.png')))

                self.putted_card.append(Card(self.deck[i][0], Button(card_x, card_y,
                                                                     int(self.window_width / 15.52),
                                                                     int(self.window_height / 8.4),
                                                                     '',
                                                                     f'resources/character/{temp}/image.png',
                                                                     f'resources/character/{temp}/after.png',
                                                                     f'resources/character/{temp}/sound.mp3')))

                if self.deck[i][0].name == 'Казнь':
                    self.card_to_kill()

                a = self.check_frac([i[0] for i in self.putted_card])
                font = pygame.font.SysFont("Times new roman", int(self.shrift_coefficient))
                if a["e"] >= 3 and "Я инженер — этим всё сказано!" not in self.used_comb:
                    self.bot_damage = 0
                    self.used_comb.append("Я инженер — этим всё сказано!")
                    text = font.render('Вы собрали комбинацию: "Я инженер — этим всё сказано!"', True,
                                       self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                    text = font.render('Урон противника уменьшен до 0', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                    self.draw_board()
                    time.sleep(0.5)
                if a["s"] >= 3 and "Ученье-свет!" not in self.used_comb:
                    self.player_health += 200
                    self.used_comb.append("Ученье-свет!")
                    text = font.render('Вы собрали комбинацию: "Ученье-свет!"', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                    text = font.render('Ваше здоровье увеличено на 200', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                    self.draw_board()
                    time.sleep(0.5)
                if a["m"] >= 3 and "Искалеченная плоть, искалеченная душа" not in self.used_comb:
                    self.used_comb.append("Искалеченная плоть, искалеченная душа")
                    self.player_damage += 150
                    text = font.render('Ваш урон увеличен на 150', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                    text = font.render('Вы собрали комбинацию: "Искалеченная плоть, искалеченная душа"', True,
                                       self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                    self.draw_board()
                    time.sleep(0.5)
                if a["s"] >= 2 and a["m"] >= 2 and "Одна голова хорошо, а две — мутант!" not in self.used_comb:
                    self.used_comb.append("Одна голова хорошо, а две — мутант!")
                    self.player_health += 200
                    text = font.render('Ваше здоровье увеличено на 200', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                    text = font.render('Вы собрали комбинацию: "Одна голова хорошо, а две — мутант!"', True,
                                       self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                    self.draw_board()
                    time.sleep(0.5)
                if a["e"] >= 2 and (
                        a["s"] >= 2 or a["m"] >= 2) and "Человек хуже мутанта, когда он мутант." not in self.used_comb:
                    self.used_comb.append("Человек хуже мутанта, когда он мутант.")
                    self.player_damage += 350
                    text = font.render('Ваш урон увеличен на 350', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                    text = font.render('Вы собрали комбинацию: "Человек хуже мутанта, когда он мутант."', True,
                                       self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                    self.draw_board()
                    time.sleep(0.5)
                if a["s"] >= 5 and "Плох тот ученый который не инженер" not in self.used_comb:
                    self.used_comb.append("Плох тот ученый который не инженер")
                    self.player_health += 490
                    text = font.render('Ваше здоровье увеличено на 490', True, self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.3)))
                    text = font.render('Вы собрали комбинацию: "Плох тот ученый который не инженер"', True,
                                       self.button_color)
                    self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
                    self.draw_board()
                    time.sleep(0.5)

            else:
                self.put_spy(self.deck[i])

            self.turn = False
            self.redrawing()
            self.stat['players_putted_car'] += 1
            self.bot_turn()

    def put_spy(self, spy):
        if spy[0].frac[0] == "s":  # первый ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.bot_rows[0]
            card_y = int(self.window_height / 3.73)
            self.bot_rows[0] += 1

        elif spy[0].frac[0] == "m":  # второй ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.bot_rows[1]
            card_y = int(self.window_height / 7)
            self.bot_rows[1] += 1

        else:  # третий ряд
            card_x = int(self.window_width / 2.73) + int(self.window_width / 15.52) * self.bot_rows[2]
            card_y = int(0)
            self.bot_rows[2] += 1
        temp = spy[0].path

        i = self.deck.index(spy)
        self.deck[i] = (Card(Character(temp, True),
                             Button(int(self.window_width / 4.22 + i * self.window_width / 15.52),
                                    int(self.window_height / 1.19), int(self.window_width / 15.52),
                                    int(self.window_height / 6.4), '',
                                    f'resources/character/{temp}/used.png',
                                    f'resources/character/{temp}/used.png')))

        self.putted_spy.append(Card(spy[0], Button(card_x, card_y, int(self.window_width / 15.52),
                                                   int(self.window_height / 8.4),
                                                   '',
                                                   f'resources/character/{temp}/image.png',
                                                   f'resources/character/{temp}/after.png',

                                                   f'resources/character/{temp}/sound.mp3')))
        self.putted_card.append(Card(spy[0], Button(card_x, card_y,
                                                    int(self.window_width / 15.52),
                                                    int(self.window_height / 8.4),
                                                    '',
                                                    f'resources/character/{temp}/image.png',
                                                    f'resources/character/{temp}/after.png',
                                                    f'resources/character/{temp}/sound.mp3')))

        self.bot_health += int(spy[0].health)
        self.bot_damage += int(spy[0].damage)

        self.bots_card_num += 1
        for i in self.putted_card:
            i[1].draw(self.window)
        time.sleep(0.3)
        font = pygame.font.SysFont("Times new roman", int(self.shrift_coefficient))
        text = font.render('В следующем раунде вы получите бонус в 3 карты', True,
                           self.button_color)
        self.window.blit(text, (int(self.window_width / 3), int(self.window_height / 2.5)))
        self.draw_board()
        time.sleep(1)
        self.redrawing()
        self.turn = True
        self.action_button.text = 'пас'

    def card_to_kill(self):
        maxik = -1
        for i in self.putted_card:
            if maxik < int(i[0].health) + int(i[0].damage) and i not in self.dead_card:
                maxik = max(maxik, int(i[0].health) + int(i[0].damage))
                max_card = (i, 'p')
        for i in self.bots_putted_card:
            if maxik < int(i[0].health) + int(i[0].damage) and i not in self.dead_card:
                maxik = max(maxik, int(i[0].health) + int(i[0].damage))
                max_card = (i, 'b')
        try:
            max_card[0][1].image = pygame.transform.scale(pygame.image.load(max_card[0][0].used_image), (
                int(self.window_width / 15.52),
                int(self.window_height / 8.4)))
        except UnboundLocalError:
            pass
        if max_card[1] == 'b':
            self.bot_health -= int(max_card[0][0].health)
            self.bot_damage -= int(max_card[0][0].damage)
        else:
            self.player_health -= int(max_card[0][0].health)
            self.player_damage -= int(max_card[0][0].damage)

        self.explosion = AnimatedSprite(load_image('explosion.png', True), 5, 1, max_card[0][1].x,
                                        max_card[0][1].y,
                                        self.all_sprites, 6)
        self.dead_card.append(max_card[0])

    def over(self):
        font = pygame.font.Font("resources/settings/font_settings/shrift.otf", self.shrift_coefficient)

        self.stat['bots_summary_damage'] += self.bot_damage
        self.stat['players_summary_damage'] += self.player_damage
        self.stat['bots_summary_health'] += self.bot_health
        self.stat['players_summary_health'] += self.player_health

        if self.player_health - self.bot_damage <= self.bot_health - self.player_damage:
            result = font.render('Вы потеряли жизнь', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3.1), int(self.window_height / 2.8)))
            self.player_hearts -= 1
            pygame.display.flip()
            time.sleep(0.7)
        else:
            result = font.render('Противник потерял жизнь', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3.1), int(self.window_height / 2.8)))
            self.bots_hearts -= 1
            pygame.display.flip()
            time.sleep(0.7)

        if self.player_hearts == 0:
            self.comp = False
            result = font.render('Вы проиграли', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3.1), int(self.window_height / 2.8)))
            time.sleep(0.7)

        elif self.bots_hearts == 0:
            self.comp = True
            result = font.render('Вы Выиграли', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3.1), int(self.window_height / 2.8)))
            time.sleep(0.7)

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
        if self.putted_spy:
            k = 3 * len(self.putted_spy)
            while True:
                temp = choice(os.listdir('resources/character'))
                if temp not in self.ch and temp != 'question':
                    self.ch.append(temp)
                    self.new_deck.append((Character(temp),
                                          Button(int(0),
                                                 int(self.window_height / 1.21), int(self.window_width / 15.52),
                                                 int(self.window_height / 6.4), '',
                                                 f'resources/character/{temp}/image.png',
                                                 f'resources/character/{temp}/after.png',
                                                 f'resources/character/{temp}/sound.mp3')))
                    k -= 1
                if len(self.new_deck) == 10 or k == 0:
                    break
        counter = 0
        for i in self.new_deck:
            i[1].x = int(self.window_width / 4.22 + counter * self.window_width / 15.52)
            self.deck.append(i)
            i[1].draw(self.window)
            counter += 1
        self.null_everything()
        self.action_button.text = "Приступить к битве"
        self.player_status = self.player_status = self.font.render("Обменяйте или выложите карту", True,
                                                                   self.button_color)
        self.redrawing()
        if len(self.new_deck) == 0 and self.bots_hearts != 0:
            result = font.render('Вы проиграли из-за недостатка карт', True, self.button_color)
            self.window.blit(result, (int(self.window_width / 3.1), int(self.window_height / 2.8)))
            pygame.display.flip()
            time.sleep(1)
            self.player_hearts = 0
            self.comp = False
            self.open()

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
        self.putted_spy = []

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

    def draw_board(self):
        pygame.draw.rect(self.window, (255, 205, 234),
                         [int(self.window_width / 3) - 10, int(self.window_height / 2.5) - self.shrift_coefficient,
                          self.window_width // 2.2, 150],
                         width=10)
        pygame.display.flip()

    def check_spy(self, arg):
        result = []
        if arg[0].name.lower() in "бастионснайперштурмовик":
            result = arg
        return result
