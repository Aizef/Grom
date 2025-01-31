import getpass
import json
import sys

import pygame
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

from pygame import FULLSCREEN

from buttons import Settings_Button, Button
import ctypes


class Settings:
    def __init__(self, window_width, window_height, screen, last_object):
        pygame.init()
        self.setting = json.load(open('resources/settings/settings.json'))
        self.clock = pygame.time.Clock()
        self.verification = False
        self.temp_volume = int(self.get('volume_level'))
        self.temp_fullscren = self.get('fullscreen_status')
        self.temp_fps = self.get('fps_status')

        self.window_width = window_width
        self.window_height = window_height

        #  код отвечает за изменение звука
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        #  код отвечает за изменение разрешения экрана
        self.screen_list = []
        for i in [res for res in pygame.display.list_modes() if res[0] >= 800 and res[1] >= 600][::-1]:
            self.screen_list.append(f'{i[0]} x {i[1]}')

        self.temp_screen = self.get('screen_status')
        self.screen_size = (self.window_width,
                            self.window_height)

        if self.setting['fullscreen_status'] == 'True':
            self.screen = pygame.display.set_mode((0, 0), FULLSCREEN)
            self.window = pygame.display.set_mode(self.screen_size, FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self.screen_size, FULLSCREEN)
        self.background_image = pygame.image.load("resources/pictures/set_final.png")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_size)
        self.window.blit(self.background_image, (0, 0))

        pygame.display.set_caption("Настройки")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.font = pygame.font.Font("resources/settings/font_settings/shrift.otf", 16)

        #  создание надписей
        self.text_complexity = self.font.render("Сбросить настройки", True, self.button_color)
        self.text_volume = self.font.render("Изменение уровня громкости", True, self.button_color)
        self.text_fps = self.font.render("Отображать FPS?", True, self.button_color)
        self.text_brightness = self.font.render("Полноэкранный режим", True, self.button_color)
        self.text_screen = self.font.render("Изменение разрешения экрана", True, self.button_color)
        self.text_show_fps = self.font.render(f"", True, self.button_color)
        # рендер кнопок
        self.previous_screen = screen
        self.back_object = last_object

        #  рендер окна
        self.previous_screen.blit(self.window, (0, 0))
        self.redrawing(True)
        pygame.display.flip()

    def open(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_plus.is_hovered:
                        self.temp_screen = int(self.temp_screen) + 1
                        if int(self.temp_screen) == len(self.screen_list):
                            self.temp_screen = 0
                        self.screen_status.text = str(self.screen_list[self.temp_screen])
                        pygame.display.flip()

                    elif self.screen_minus.is_hovered:
                        if int(self.temp_screen) > 0:
                            self.temp_screen = int(self.temp_screen) - 1
                        else:
                            self.temp_screen = len(self.screen_list) - 1

                        self.screen_status.text = str(self.screen_list[self.temp_screen])
                        pygame.display.flip()

                    elif self.verify.is_hovered:
                        self.insert_settings()
                        running = False

                    elif self.volume_plus.is_hovered:
                        if float(self.temp_volume) <= 90:
                            self.temp_volume = round(float(self.temp_volume) + 10, 1)
                            self.volume_status.text = str(int(self.temp_volume))
                            self.volume_status.draw(self.window)
                            self.volume_plus.draw(self.window, temp=10)
                            self.volume_minus.draw(self.window, temp=10)
                            pygame.display.flip()

                    elif self.volume_minus.is_hovered:
                        if 0 < float(self.temp_volume):
                            self.temp_volume = round(float(self.temp_volume) - 10, 1)
                            self.volume_status.text = str(int(self.temp_volume))
                            self.volume_status.draw(self.window)
                            self.volume_plus.draw(self.window, temp=10)
                            self.volume_minus.draw(self.window, temp=10)
                            pygame.display.flip()

                    elif self.fullscreen_no.is_hovered:
                        self.temp_fullscren = 'False'

                    elif self.fullscreen_yes.is_hovered:
                        self.temp_fullscren = 'True'

                    elif self.fps_yes.is_hovered:
                        self.temp_fps = 'True'

                    elif self.fps_no.is_hovered:
                        self.temp_fps = 'False'

                    elif self.default.is_hovered:
                        user32 = ctypes.windll.user32
                        user32.SetProcessDPIAware()
                        json.dump({"fps_status": "False", "fullscreen_status": 'True',
                                   "volume_level": 60, "screen_status": 15, "last_user": getpass.getuser()},
                                  open('resources/settings/settings.json', 'w'))
                        s = Settings(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1), self.window,
                                     self.back_object)
                        s.open()

                    elif self.back_btn.is_hovered:
                        self.back()

                self.verify.handle_event(event)
                self.default.handle_event(event)
                self.volume_plus.handle_event(event)
                self.volume_minus.handle_event(event)

                self.fullscreen_yes.handle_event(event)
                self.fullscreen_no.handle_event(event)

                self.screen_plus.handle_event(event)
                self.screen_minus.handle_event(event)

                self.fps_yes.handle_event(event)
                self.fps_no.handle_event(event)

            self.volume_plus.check_hover(pygame.mouse.get_pos())
            self.volume_minus.check_hover(pygame.mouse.get_pos())
            self.default.check_hover(pygame.mouse.get_pos())
            self.fullscreen_yes.check_hover(pygame.mouse.get_pos())
            self.fullscreen_no.check_hover(pygame.mouse.get_pos())

            self.screen_plus.check_hover(pygame.mouse.get_pos())
            self.screen_minus.check_hover(pygame.mouse.get_pos())

            self.fps_yes.check_hover(pygame.mouse.get_pos())
            self.fps_no.check_hover(pygame.mouse.get_pos())

            self.back_btn.check_hover(pygame.mouse.get_pos())
            if self.setting['fps_status'] == self.temp_fps and self.setting[
                'fullscreen_status'] == self.temp_fullscren and self.setting['volume_level'] == self.temp_volume and \
                    self.setting['screen_status'] == self.temp_screen:
                self.verification = False
            else:
                self.verification = True
            self.clock.tick(90)
            self.redrawing()
            pygame.display.flip()

    def redrawing(self, full=False):
        self.window.blit(self.background_image, (0, 0))
        if full:
            self.back_btn = Settings_Button(int(self.screen_size[0] / 1.29), 0, int(self.screen_size[0] / 4.4),
                                            int(self.screen_size[1] / 15.2), 'Вернуться',
                                            'resources/pictures/before.png',
                                            'resources/pictures/after.png',
                                            'resources/sound/btn_on.mp3')

            self.default = Button(int(self.screen_size[0] / 2.8), int(self.screen_size[1] / 1.65),
                                  int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43),
                                  'Подтвердить',
                                  'resources/pictures/before.png',
                                  'resources/pictures/after.png',
                                  'resources/sound/btn_on.mp3')

            self.volume_status = Settings_Button(int(self.screen_size[0] / 2.58), int(self.screen_size[1] / 11.6),
                                                 int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 10),
                                                 f'{self.temp_volume}',
                                                 'resources/pictures/after1.png',
                                                 'resources/pictures/before.png',
                                                 'resources/sound/btn_on.mp3')
            self.volume_plus = Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 11.6),
                                      int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '+',
                                      'resources/pictures/before.png',
                                      'resources/pictures/after.png',
                                      'resources/sound/btn_on.mp3')
            self.volume_minus = Button(int(self.screen_size[0] / 4), int(self.screen_size[1] / 11.6),
                                       int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '-',
                                       'resources/pictures/before.png',
                                       'resources/pictures/after.png',
                                       'resources/sound/btn_on.mp3')
            self.fullscreen_yes = Settings_Button(int(self.screen_size[0] / 2), int(self.screen_size[1] / 3.86),
                                                  int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), 'Да',
                                                  'resources/pictures/before.png',
                                                  'resources/pictures/after.png',
                                                  'resources/sound/btn_on.mp3')
            self.fullscreen_no = Settings_Button(int(self.screen_size[0] / 2.9), int(self.screen_size[1] / 3.86),
                                                 int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), 'Нет',
                                                 'resources/pictures/before.png',
                                                 'resources/pictures/after.png',
                                                 'resources/sound/btn_on.mp3')
            self.screen_status = Settings_Button(int(self.screen_size[0] / 2.58), int(self.screen_size[1] / 2.32),
                                                 int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 10),
                                                 f'{self.screen_list[int(self.temp_screen)]}',
                                                 'resources/pictures/after1.png',
                                                 'resources/pictures/before.png',
                                                 'resources/sound/btn_on.mp3')
            self.screen_plus = Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 2.32),
                                      int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '->',
                                      'resources/pictures/before.png',
                                      'resources/pictures/after.png',
                                      'resources/sound/btn_on.mp3')
            self.screen_minus = Button(int(self.screen_size[0] / 4), int(self.screen_size[1] / 2.32),
                                       int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '<-',
                                       'resources/pictures/before.png',
                                       'resources/pictures/after.png',
                                       'resources/sound/btn_on.mp3')
            self.fps_yes = Settings_Button(int(self.screen_size[0] / 2.5), int(self.screen_size[1] / 1.234),
                                           int(self.screen_size[0] / 11), int(self.screen_size[1] / 12), 'Да',
                                           'resources/pictures/before.png',
                                           'resources/pictures/before.png',
                                           'resources/sound/btn_on.mp3')
            self.fps_no = Settings_Button(int(self.screen_size[0] / 2), int(self.screen_size[1] / 1.234),
                                          int(self.screen_size[0] / 11), int(self.screen_size[1] / 12), 'Нет',
                                          'resources/pictures/before.png',
                                          'resources/pictures/before.png',
                                          'resources/sound/btn_on.mp3')
            self.verify = Button(int(self.screen_size[0] / 2.75), int(self.screen_size[1] / 1.11),
                                 int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 12), 'Подтвердить',
                                 'resources/pictures/before.png',
                                 'resources/pictures/after1.png',
                                 'resources/sound/btn_on.mp3', is_on=True)

        if self.setting['fps_status'] == "True":
            self.grom_text_show_fps = self.font.render(f"{str(self.clock.get_fps()).split('.')[0]}", True,
                                                       (255, 205, 234))
            self.window.blit(self.grom_text_show_fps, (0, 0))

        if self.verification:
            self.verify.check_hover(pygame.mouse.get_pos())
            self.verify.draw(self.window, temp=0)

        self.volume_plus.draw(self.window, temp=10)
        self.volume_minus.draw(self.window, temp=10)
        self.volume_status.draw(self.window)

        self.default.draw(self.window)

        self.screen_status.draw(self.window)
        self.screen_plus.draw(self.window, temp=10)
        self.screen_minus.draw(self.window, temp=10)

        if self.temp_fps == 'True':
            self.fps_yes.draw(self.window, temp=1)
            self.fps_no.draw(self.window, temp=-1)
        else:
            self.fps_yes.draw(self.window, temp=-1)
            self.fps_no.draw(self.window, temp=1)

        if self.temp_fullscren == 'True':
            self.fullscreen_yes.draw(self.window, temp=1)
            self.fullscreen_no.draw(self.window, temp=-1)
        else:
            self.fullscreen_yes.draw(self.window, temp=-1)
            self.fullscreen_no.draw(self.window, temp=1)

        self.window.blit(self.text_complexity, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 1.8)))
        self.window.blit(self.text_volume, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 23.2)))
        self.window.blit(self.text_brightness, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 4.46)))
        self.window.blit(self.text_fps, (int(self.screen_size[0] / 2.5), int(self.screen_size[1] / 1.28)))
        self.window.blit(self.text_screen, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 2.6)))
        self.previous_screen.blit(self.window, (0, 0))
        self.back_btn.draw(self.window)

    def insert_settings(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.screen_size = (int(self.screen_list[self.temp_screen].split()[0]),
                            int(self.screen_list[self.temp_screen].split()[-1]))
        print(20 // user32.GetSystemMetrics(0) // user32.GetSystemMetrics(1) // int(
            self.screen_list[self.temp_screen].split()[0]) // int(self.screen_list[self.temp_screen].split()[-1]),
              file=open('resources/settings/font_settings/font_size.txt', 'w'))

        self.volume.SetMasterVolumeLevelScalar(float(self.temp_volume) / 100, None)
        if self.temp_fps:
            temp = pygame.image.load("resources/pictures/after1.png")
            self.fps_yes.hover_image = pygame.transform.scale(temp, (
                int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))
            temp = pygame.image.load("resources/pictures/before.png")
            self.fps_no.hover_image = pygame.transform.scale(temp, (
                int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))
        else:
            temp = pygame.image.load("resources/pictures/before.png")
            self.fps_yes.hover_image = pygame.transform.scale(temp, (
                int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))
            temp = pygame.image.load("resources/pictures/after1.png")
            self.fps_no.hover_image = pygame.transform.scale(temp, (
                int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))
        if self.temp_fullscren == 'True':
            self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self.screen_size)
        self.background_image = pygame.image.load("resources/pictures/set_final.png")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_size)
        self.window.blit(self.background_image, (0, 0))
        with open('resources/settings/settings.json', 'w') as file:
            s = {'fps_status': self.temp_fps, 'fullscreen_status': self.temp_fullscren,
                 'volume_level': self.temp_volume,
                 'screen_status': self.temp_screen, 'last_user': getpass.getuser()}
            json.dump(s, file)
            self.setting = s
        self.verification = False
        self.redrawing(True)
        pygame.display.flip()
        self.open()

    def back(self):  # возврат
        pygame.display.set_caption("Grom")
        self.back_object.reopen(self.screen_size[0], self.screen_size[1])

    def get(self, name):
        return self.setting[name]
