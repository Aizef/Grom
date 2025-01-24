import json

from buttons import Button
import sys

import pygame
from pygame import FULLSCREEN


class Statistic_window:
    def __init__(self, window_width, window_height, screen, pr, stat, comp):
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.previous_object = pr
        self.button_color = (255, 205, 234)

        self.button_text_color = (0, 0, 0)
        self.shrift_koeff = 35 * self.window_width * self.window_height // 2560 // 1600
        self.settings = json.load(open("resources/settings/settings.json"))
        if self.settings['fullscreen_status'] == 'True':
            self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        if comp:
            self.font = pygame.font.Font('resources/other/shrift.otf', self.shrift_koeff)
            self.background_image = pygame.image.load("resources/pictures/mis_compl.png").convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.window_width, self.window_height))
        else:
            self.background_image = pygame.image.load("resources/pictures/mis_f.png").convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.window_width, self.window_height))
            self.font = pygame.font.Font('resources/other/shrift.otf', self.shrift_koeff)
        pygame.display.set_caption("Финальное окно")
        self.previous_screen = screen
        self.previous_screen.blit(self.window, (0, 0))
        self.player_damage = self.font.render(f"Суммарный урон игрока: {stat['players_summary_damage']}", True, self.button_color)
        self.player_card = self.font.render(f"Сыгранные игроком карты: {stat['players_putted_car']}", True, self.button_color)
        self.player_health = self.font.render(f"Суммарное здоровье игрока: {stat['players_summary_health']}", True, self.button_color)
        self.bots_damage = self.font.render(f"Суммарный урон бота: {stat['bots_summary_damage']}", True, self.button_color)
        self.bots_health = self.font.render(f"Суммарное здоровье бота: {stat['bots_summary_health']}", True, self.button_color)
        self.bots_cards = self.font.render(f"Сыгранные ботом карты: {stat['bots_putted_card']}", True, self.button_color)
        self.text = self.font.render("Подсчет результатов:", True, self.button_color)
        self.ret_btn = Button(int(self.window_width - self.window_width // 10 - 120), 0,
                              int(self.window_width // 10 + 110), 100, 'Вернуться к миссиям',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/start.mp3')
        self.ret_btn.draw(self.window)
        pygame.display.flip()

    def open(self):
        running = True
        while running:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.ret_btn.is_hovered:
                        self.back()
            self.window.blit(self.background_image, (0, 0))
            self.window.blit(self.player_damage, (int(50), int(self.window_height / 8)))
            self.window.blit(self.player_health, (int(50), int(self.window_height / 6)))
            self.window.blit(self.player_card, (int(50), int(self.window_height / 5)))
            self.window.blit(self.bots_damage, (int(self.window_width / 2), int(self.window_height / 8)))
            self.window.blit(self.bots_health, (int(self.window_width / 2), int(self.window_height / 6)))
            self.window.blit(self.bots_cards, (int(self.window_width / 2), int(self.window_height / 5)))
            self.window.blit(self.text, (self.window_width // 3.5, 50))
            self.ret_btn.draw(self.window)
            self.ret_btn.check_hover(pos)
            pygame.display.flip()

    def back(self):
        self.previous_object.open(True)