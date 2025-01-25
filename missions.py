import ctypes
import json
import sys
import pygame
from pygame import FULLSCREEN

from buttons import Settings_Button, Button
from mission import Mission


class Missions:
    def __init__(self, window_width, window_height, screen, last_object):
        pygame.init()
        self.grom_clock = pygame.time.Clock()

        self.window_width = window_width
        self.window_height = window_height
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        #  рисуем окно настроек
        if json.load(open('resources/settings/settings.json'))['fullscreen_status'] == 'True':
            self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_image = pygame.image.load("resources/pictures/mis_final.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Миссии")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.grom_clock = pygame.time.Clock()

        self.font = pygame.font.Font("resources/other/shrift.otf", 35 * self.window_width * self.window_height  // user32.GetSystemMetrics(0) // user32.GetSystemMetrics(1))

        if self.get_fps_result() == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

        self.first = Button(int(self.window_width / 3.5), int(self.window_height / 3.86), int(self.window_width / 2),
                            int(self.window_height / 7.43), 'Перейти к первой миссии',
                            'resources/pictures/after1.png',
                            'resources/pictures/after.png',
                            'resources/sound/btn_on.mp3')
        self.second = Button(int(self.window_width / 3.5), int(self.window_height / 2.14), int(self.window_width / 2),
                             int(self.window_height / 7.43), 'Перейти к второй миссии',
                             'resources/pictures/after1.png',
                             'resources/pictures/after.png',
                             'resources/sound/btn_on.mp3')
        self.third = Button(int(self.window_width / 3.5), int(self.window_height / 1.48), int(self.window_width / 2),
                            int(self.window_height / 7.43), 'Перейти к третьей миссии',
                            'resources/pictures/after1.png',
                            'resources/pictures/after.png',
                            'resources/sound/understood.mp3')
        self.back_btn = Settings_Button(int(self.window_width / 1.29), 0, int(self.window_width / 4.4),
                                        int(self.window_height / 15.2), 'Вернуться',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/btn_on.mp3')

        self.previous_screen = screen
        self.back_object = last_object
        #  рендер окна

        self.previous_screen.blit(self.window, (0, 0))
        pygame.display.flip()

    def open(self, full=False):
        if full:
            self.background_image = pygame.image.load("resources/pictures/mis_final.png").convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.window_width, self.window_height))
            self.window.blit(self.background_image, (0, 0))
            pygame.display.set_caption("Миссии")
        running = True
        while running:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_btn.is_hovered:
                        self.back()
                    elif self.first.is_hovered:
                        self.first.handle_event(event)
                        first_mis = Mission(self.window_width, self.window_height, self.previous_screen, self,
                                            dif="Щадящий", n=1, bi_path="table.png")
                        first_mis.open()
                    elif self.second.is_hovered:
                        self.second.handle_event(event)
                        second_mis = Mission(self.window_width, self.window_height, self.previous_screen, self,
                                            dif="Ветеран", n=1, bi_path="table.png")
                        second_mis.open()
                    elif self.third.is_hovered:
                        self.third.handle_event(event)
                        third_mis = Mission(self.window_width, self.window_height, self.previous_screen, self,
                                            dif="Ангел Смерти", n=1, bi_path="table.png")
                        third_mis.open()
                self.first.handle_event(event)
                self.second.handle_event(event)
                self.third.handle_event(event)
            self.grom_clock.tick(90)
            if self.get_fps_result() == "True":
                self.grom_text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True,
                                                           (255, 205, 234))
            else:
                self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

            self.first.check_hover(pos)
            self.second.check_hover(pos)
            self.third.check_hover(pos)

            self.back_btn.check_hover(pos)
            self.redrawing()
            pygame.display.flip()

    def redrawing(self):
        self.window.blit(self.background_image, (0, 0))
        self.first.draw(self.window)
        self.second.draw(self.window)
        self.third.draw(self.window)
        self.back_btn.draw(self.window)
        if self.get_fps_result() == "True":
            self.window.blit(self.grom_text_show_fps, (0, 0))

    def back(self):  # возврат
        pygame.display.set_caption("Grom: Essense of Chaos")
        self.back_object.main_menu()

    def get_fps_result(self):
        return json.load(open('resources/settings/settings.json'))['fps_status']
