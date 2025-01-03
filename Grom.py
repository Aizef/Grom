import ctypes
import sys
from ctypes import cast

import pygame
from _ctypes import POINTER
from comtypes import CLSCTX_ALL
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities
from Buttons import Button
from missions import Missions
from settings import Settings

class Grom:
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('resources/other/shrift.otf', 18)
        pygame.mixer.music.load("resources/sound/main_theme.mp3")
        pygame.mixer.music.play(-1)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load("resources/pictures/background_image.png")
        self.icon_image = pygame.image.load("resources/pictures/icon.png")
        pygame.display.set_icon(self.icon_image)
        self.grom_clock = pygame.time.Clock()

        with open("resources/settings/volume_level.txt", mode="r", encoding="utf-8") as file:
            current_volume = file.readline().strip()

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.grom_volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.grom_volume.SetMasterVolumeLevelScalar(float(current_volume) / 100, None)

        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        pygame.display.set_caption("Grom:Essense Of Chaos")

        self.go_to_mission_btn = Button(int(self.width / 4), int(self.height / 3.86), int(self.width / 2), 78, 'Перейти к миссиям',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/start.mp3')
        self.go_to_settings_btn = Button(int(self.width / 4), int(self.height / 2.14), int(self.width / 2), 78, 'Настройки',
                                         'resources/pictures/after1.png',
                                         'resources/pictures/after.png',
                                         'resources/sound/btn_on.mp3')
        self.go_to_desktop_btn = Button(int(self.width / 4), int(self.height / 1.48), int(self.width / 2), 78, 'Выйти из игры',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/understood.mp3')
        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            fps_status = fps_file.readline().strip()
        if fps_status == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

        self.screen.blit(self.grom_text_show_fps, (0, 0))

    def reopen(self, a, s):
        self.width, self.height = a, s
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load("resources/pictures/background_image.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.go_to_mission_btn = Button(int(self.width / 4), int(self.height / 3.86), int(self.width / 2), 78, 'Перейти к миссиям',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/start.mp3')
        self.go_to_settings_btn = Button(int(self.width / 4), int(self.height / 2.14), int(self.width / 2), 78, 'Настройки',
                                         'resources/pictures/after1.png',
                                         'resources/pictures/after.png',
                                         'resources/sound/btn_on.mp3')
        self.go_to_desktop_btn = Button(int(self.width / 4), int(self.height / 1.48), int(self.width / 2), 78, 'Выйти из игры',
                                        'resources/pictures/after1.png',
                                        'resources/pictures/after.png',
                                        'resources/sound/understood.mp3')
        self.main_menu()




    def main_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.go_to_desktop_btn.is_hovered:  # если нажата кнопка выйти из игры
                        pygame.quit()
                        sys.exit()
                    elif self.go_to_settings_btn.is_hovered:  # если нажата кнопка Настройки
                        self.go_to_settings_btn.handle_event(event)
                        settings = Settings(self.width, self.height, self.screen, self)
                        settings.open()
                    elif self.go_to_mission_btn.is_hovered:  # если нажата кнопка Перейти к миссиям
                        self.go_to_mission_btn.handle_event(event)
                        missions = Missions(self.width, self.height, self.screen, self)
                        missions.open()

                self.go_to_mission_btn.handle_event(event)
                self.go_to_settings_btn.handle_event(event)
                self.go_to_desktop_btn.handle_event(event)

            self.go_to_mission_btn.check_hover(pygame.mouse.get_pos())
            self.go_to_mission_btn.draw(self.screen)

            self.go_to_settings_btn.check_hover(pygame.mouse.get_pos())
            self.go_to_settings_btn.draw(self.screen)

            self.go_to_desktop_btn.check_hover(pygame.mouse.get_pos())

            self.grom_clock.tick(90)

            if self.get_fps_result() == "True":
                self.grom_text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True, (255, 205, 234))
            else:
                self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))
            self.go_to_desktop_btn.draw(self.screen)

            self.screen.blit(self.grom_text_show_fps, (0, 0))
            pygame.display.flip()

            self.screen.blit(self.background_image, (0, 0))


    def get_fps_result(self):
        with open("resources/settings/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            return fps_file.readline().strip()