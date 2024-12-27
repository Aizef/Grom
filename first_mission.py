import os
import sys
from random import choice

import pygame

from Buttons import Button
from Character import Character


class First_mission:
    def __init__(self, window_width, window_height, screen, pr):
        pygame.init()
        pygame.display.set_caption('Миссия первая')
        self.button_color = (255, 205, 234)
        # self.first_sting = self.font.render("Правила:", True, self.button_color) WIN
        # self.second_string = self.font.render("Перед боем вы можете заменить три карты", True, self.button_color)
        # self.third_string = self.font.render("Если не хотите нажмите приступите у битве", True, self.button_color)
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


        pygame.mouse.set_visible(True)
        #  рисуем окно настроек
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_image = pygame.image.load("resources/pictures/table.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Миссии")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.font = pygame.font.Font("resources/other/shrift.otf", 20)
        self.stat_health =  self.font.render("", True, self.button_color)
        self.stat_name =  self.font.render("", True, self.button_color)
        self.previous_screen = screen
        #  рендер окна
        # self.window.blit(self.first_sting, (0, int(self.window_height / 2.2))) WIN
        # self.window.blit(self.second_string, (0, int(self.window_height / 2.1)))
        # self.window.blit(self.third_string, (0, int(self.window_height / 2))) WIN
        self.previous_screen.blit(self.window, (0, 0))
        pygame.display.flip()
        self.back_button = Button(self.window_width - self.window_width // 10, 0, self.window_width // 10, 100,
                                  'Сдаться', 'resources/pictures/before.png', 'resources/pictures/after.png',
                                  'resources/sound/btn_on.mp3')
        self.deck = []
        self.putted_card = None
        self.ch = []
        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch:
                self.ch.append(temp)
                self.deck.append((Character(temp),
                                  Button(int(self.window_width / 3.52 + len(self.deck) * self.window_width / 15.52),
                                         int(self.window_height / 1.28), int(self.window_width / 15.52),
                                         int(self.window_height / 6.4), '', f'resources/character/{temp}/image.png',
                                         f'resources/character/{temp}/after.png',
                                         f'resources/character/{temp}/sound.mp3')))
            if len(self.deck) == 8:
                break
        self.change_counter = 3
        self.turn = True
        # self.turn = choice([True, False])
        self.action_button = Button(int(self.window_width / 36), int(self.window_height / 1.24), int(self.window_width / 5), int(self.window_height / 20),
                                    'Приступить к битве', 'resources/pictures/before.png',
                                    'resources/pictures/after.png', 'resources/sound/btn_on.mp3')

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
                            self.change_counter -= 1
                        elif self.deck[i][1].is_hovered and self.turn == True:
                            self.put_card(i)
                        elif self.action_button.is_hovered and self.turn:
                            self.change_counter = 0
                            self.action_button.text = 'Выложите карту'
                for i in self.deck:
                    if i[1].is_hovered:
                        self.stat_name = self.font.render(f"Имя: {i[0].name}", True, self.button_color)
                        self.stat_health = self.font.render(f"Здоровье: {i[0].health}", True, self.button_color)



                self.back_button.handle_event(event)
            self.grom_clock.tick(90)
            if self.get_fps_result() == "True":
                self.grom_text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True, (255, 205, 234))
            else:
                self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

            self.back_button.check_hover(pos)
            if self.change_counter != 0:
                self.action_button.check_hover(pos)
            for i in self.deck:
                i[1].check_hover(pos)
            self.redrawing()
            pygame.display.flip()

    def back(self):
        self.previous_object.open(True)

    def change(self, num):
        while True:
            temp = choice(os.listdir('resources/character'))
            if temp not in self.ch:
                self.ch[num] = temp
                self.deck[num] = ((Character(temp),
                                   Button(int(self.window_width / 3.52 + num * self.window_width / 15.52),
                                          int(self.window_height / 1.28), int(self.window_width / 15.52),
                                          int(self.window_height / 6.4), '', f'resources/character/{temp}/image.png',
                                          f'resources/character/{temp}/after.png',
                                          f'resources/character/{temp}/sound.mp3')))
                break
        self.redrawing()

    def redrawing(self):
        self.window.blit(self.background_image, (0, 0))
        self.window.blit(self.stat_name, (int(self.window_width / 100), int(self.window_height / 2.2)))
        self.window.blit(self.stat_health, (int(self.window_width / 100), int(self.window_height / 2)))
        self.back_button.draw(self.window)
        for i in self.deck:
            i[1].draw(self.window)
        self.action_button.draw(self.window)
        if self.putted_card != None:
            self.putted_card[1].draw(self.window)
        self.window.blit(self.grom_text_show_fps, (0, 0))

        pygame.display.flip()

    def bot_turn(self):
        self.action_button.text = 'Ожидайте хода противника'
        self.redrawing()


    def put_card(self, i):
        temp = self.deck[i][0].path
        self.deck[i] = ((Character(temp, True), Button(int(self.window_width / 3.52 + i * self.window_width / 15.52),
                                                       int(self.window_height / 1.28), int(self.window_width / 15.52),
                                                       int(self.window_height / 6.4), '',
                                                       f'resources/character/{temp}/used.png',
                                                       f'resources/character/{temp}/used.png')))
        self.putted_card = (self.deck[i][0], Button(int(self.window_width / 1.83), int(self.window_height / 2.1),
                                                    int(self.window_width / 15.52), int(self.window_height / 6.4), '',
                                                    f'resources/character/{temp}/image.png',
                                                    f'resources/character/{temp}/after.png',
                                                    f'resources/character/{temp}/sound.mp3'))
        self.putted_card[1].draw(self.window)
        self.turn = False
        self.action_button.text = 'Завершить ход'
        self.bot_turn()

    def get_fps_result(self):
        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            return fps_file.readline().strip()