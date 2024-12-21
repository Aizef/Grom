import ctypes
import sys
from ctypes import cast

import pygame
from _ctypes import POINTER
from comtypes import CLSCTX_ALL
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities
from Buttons import Button, Settings_Button
from settings import Settings

class Grom:
    def __init__(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('resources/shrift.otf', 30)
        pygame.mixer.music.load("resources/main_theme.mp3")
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load("resources/background_image.png")
        self.icon_image = pygame.image.load("resources/icon.png")
        pygame.display.set_icon(self.icon_image)
        self.grom_clock = pygame.time.Clock()

        with open("resources/volume_level.txt", mode="r", encoding="utf-8") as file:
            current_volume = file.readline().strip()

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.grom_volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.grom_volume.SetMasterVolumeLevelScalar(float(current_volume) / 100, None)

        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        pygame.display.set_caption("Grom:Essense Of Chaos")

        self.go_to_mission_btn = Button(int(self.width / 3.5), int(self.height / 3.86), int(self.width / 2), int(self.height / 7.43), 'Перейти к миссиям',
                                        'resources/after1.png',
                                        'resources/after.png',
                                        'resources/start.mp3')
        self.go_to_settings_btn = Button(int(self.width / 3.5), int(self.height / 2.14), int(self.width / 2), int(self.height / 7.43), 'Настройки',
                                         'resources/after1.png',
                                         'resources/after.png',
                                         'resources/btn_on.mp3')
        self.go_to_desktop_btn = Button(int(self.width / 3.5), int(self.height / 1.48), int(self.width / 2), int(self.height / 7.43), 'Выйти из игры',
                                        'resources/after1.png',
                                        'resources/after.png',
                                        'resources/understood.mp3')
        with open("resources/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            fps_status = fps_file.readline().strip()
        if fps_status == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

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
                        pass # в разработке
                self.go_to_mission_btn.handle_event(event)
                self.go_to_settings_btn.handle_event(event)
                self.go_to_desktop_btn.handle_event(event)

            if self.get_fps_result() == "True":
                self.screen.blit(self.grom_text_show_fps, (0, 0))
                s_b = Settings_Button(0, 0, int(self.width / 22), int(self.height / 11.6), '', 'resources/fps.png')
                s_b.draw(self.screen)

                text_show_fps = self.font.render(f"{str(self.grom_clock.get_fps()).split('.')[0]}", True,
                                                 (255, 205, 234))

                self.screen.blit(text_show_fps, (0, 0))
            else:
                s_b = Settings_Button(0, 0, int(self.width / 22), int(self.height / 11.6), '', 'resources/fps.png')
                s_b.draw(self.screen)


            self.go_to_mission_btn.check_hover(pygame.mouse.get_pos())
            self.go_to_mission_btn.draw(self.screen)

            self.go_to_settings_btn.check_hover(pygame.mouse.get_pos())
            self.go_to_settings_btn.draw(self.screen)

            self.go_to_desktop_btn.check_hover(pygame.mouse.get_pos())

            self.go_to_desktop_btn.draw(self.screen)

            pygame.display.flip()

            self.screen.blit(self.background_image, (0, 0))

            self.grom_clock.tick(90)

    def get_fps_result(self):
        with open("resources/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            return fps_file.readline().strip()
