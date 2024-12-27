import sys
import pygame
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import wmi
from Buttons import Settings_Button, Button
from first_mission import First_mission


class Missions:
    def __init__(self, window_width, window_height, screen, last_object):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.window_width = window_width
        self.window_height = window_height

        #  рисуем окно настроек
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.background_image = pygame.image.load("resources/pictures/background_image.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Миссии")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.grom_clock = pygame.time.Clock()

        self.font = pygame.font.Font("resources/other/shrift.otf", 40)
        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            fps_status = fps_file.readline().strip()
        if fps_status == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

        self.first = Button(int(self.window_width / 3.5), int(self.window_height / 3.86), int(self.window_width / 2),
                                        int(self.window_height / 7.43), 'Перейти к первой миссии',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/start.mp3')
        self.second = Button(int(self.window_width / 3.5), int(self.window_height / 2.14), int(self.window_width / 2),
                                         int(self.window_height / 7.43), 'Перейти к второй миссии',
                                         'resources/pictures/before.png',
                                         'resources/pictures/before.png',
                                         'resources/sound/btn_on.mp3')
        self.third = Button(int(self.window_width / 3.5), int(self.window_height / 1.48), int(self.window_width / 2),
                                        int(self.window_height / 7.43), 'Перейти к третьей миссии',
                                        'resources/pictures/before.png',
                                        'resources/pictures/before.png',
                                        'resources/sound/understood.mp3')
        self.back_btn = Settings_Button(int(self.window_width / 1.29), 0, int(self.window_width / 4.4),
                                        int(self.window_height / 15.2), 'Вернуться',
                                        'resources/pictures/before.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/btn_on.mp3')

        self.previous_screen = screen
        self.back_object = last_object
        #  рендер окна

        self.previous_screen.blit(self.window, (0, 0))
        pygame.display.flip()

    def open(self, full=False):
        if full:
            self.background_image = pygame.image.load("resources/pictures/background_image.png").convert_alpha()
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_btn.is_hovered:
                        self.back()
                    elif self.first.is_hovered:
                        self.first.handle_event(event)
                        first_mission = First_mission(self.window_width, self.window_height, self.previous_screen, self)
                        first_mission.open()

                self.first.handle_event(event)
                self.second.handle_event(event)
                self.third.handle_event(event)
            self.grom_clock.tick(90)
            if self.get_fps_result() == "True":
                self.grom_text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True, (255, 205, 234))
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
        self.window.blit(self.grom_text_show_fps, (0, 0))

    def back(self):  # возврат
        pygame.display.set_caption("Grom: Essense of Chaos")
        self.back_object.main_menu()

    def get_fps_result(self):
        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            return fps_file.readline().strip()