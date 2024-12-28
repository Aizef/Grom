import codecs
import sys

import pygame
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import wmi
from Buttons import Settings_Button, Button
import ctypes
import screen_brightness_control as sbc


class Settings:
    def __init__(self, window_width, window_height, screen, last_object):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_veri = False
        self.temp_volume = int(self.get_volume())
        self.temp_brightness = int(str(sbc.get_brightness())[1:-1])
        self.set_brightness(self.temp_brightness)
        self.temp_dif = self.get_difficulty()
        self.temp_fps = open('resources/settings/fps_status.txt').read().strip()

        print(self.temp_brightness, file=open('resources/settings/brightness_level.txt', 'w'))

        self.window_width = window_width
        self.window_height = window_height

        #  код отвечает за изменение яркости
        self.set_brightness(self.get_brightness())

        #  код отвечает за изменение звука
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.set_volume(float(self.get_volume()))

        #  код отвечает за изменение разрешения экрана
        self.screen_list = []
        for i in [res for res in pygame.display.list_modes() if res[0] >= 800 and res[1] >= 600][::-1]:
            self.screen_list.append(f'{i[0]} x {i[1]}')
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.max_widht = user32.GetSystemMetrics(0)
        self.max_height = user32.GetSystemMetrics(1)
        self.temp_screen = len(self.screen_list) - 1
        self.screen_list.pop()
        self.screen_list.append('Полноэкранный режим')

        self.set_screen(self.temp_screen)
        self.setting = [self.temp_screen, self.temp_volume, self.temp_brightness, self.get_difficulty(),
                        open('resources/settings/fps_status.txt').read().strip()]
        self.screen_size = (self.window_width,
                            self.window_height)
        self.window = pygame.display.set_mode(self.screen_size)

        self.background_image = pygame.image.load("resources/pictures/background_image.png")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_size)
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Настройки")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.font = pygame.font.Font("resources/other/shrift.otf", 16)

        #  создание надписей
        self.text_complexity = self.font.render("Изменение уровня сложности", True, self.button_color)
        self.text_volume = self.font.render("Изменение уровня громкости", True, self.button_color)
        self.text_fps = self.font.render("Отображать FPS?", True, self.button_color)
        self.text_brightness = self.font.render("Изменение уровня яркости", True, self.button_color)
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
        print(6)
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
                        self.insert_settings(self.temp_volume, self.temp_brightness, self.temp_screen)
                        running = False

                    elif self.brightness_minus.is_hovered:
                        if self.temp_brightness > 0:
                            self.temp_brightness -= 10
                            self.brightness_status.text = str(self.temp_brightness)
                            self.brightness_status.draw(self.window)
                            pygame.display.flip()

                    elif self.brightness_plus.is_hovered:
                        if self.temp_brightness <= 90:
                            self.temp_brightness += 10
                            self.brightness_status.text = str(self.temp_brightness)
                            self.brightness_status.draw(self.window)
                            pygame.display.flip()

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

                    elif self.fps_yes.is_hovered:
                        self.temp_fps = 'True'

                    elif self.fps_no.is_hovered:
                        self.temp_fps = 'False'

                    elif self.easy_btn.is_hovered:
                        self.temp_dif = "Щадящий"
                        temp = pygame.image.load("resources/pictures/after1.png")
                        self.easy_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/pictures/before.png")
                        self.veteran_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/pictures/before.png")
                        self.hard_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        self.easy_btn.draw(self.window)
                        self.veteran_btn.draw(self.window)
                        self.hard_btn.draw(self.window)

                        pygame.display.flip()

                    elif self.veteran_btn.is_hovered:
                        self.temp_dif = ("Ветеран")

                        temp = pygame.image.load("resources/pictures/before.png")
                        self.easy_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/pictures/after1.png")
                        self.veteran_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/pictures/before.png")
                        self.hard_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        self.easy_btn.draw(self.window)
                        self.veteran_btn.draw(self.window)
                        self.hard_btn.draw(self.window)

                        pygame.display.flip()

                    elif self.hard_btn.is_hovered:
                        self.temp_dif = ("Ангел Смерти")

                        temp = pygame.image.load("resources/pictures/before.png")
                        self.easy_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/pictures/before.png")
                        self.veteran_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/pictures/after1.png")
                        self.hard_btn.hover_image = pygame.transform.scale(temp, (
                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        self.easy_btn.draw(self.window)
                        self.veteran_btn.draw(self.window)
                        self.hard_btn.draw(self.window)

                        pygame.display.flip()

                    elif self.back_btn.is_hovered:
                        self.back()

                self.verify.handle_event(event)
                self.easy_btn.handle_event(event)
                self.veteran_btn.handle_event(event)
                self.hard_btn.handle_event(event)

                self.volume_plus.handle_event(event)
                self.volume_minus.handle_event(event)

                self.brightness_plus.handle_event(event)
                self.brightness_minus.handle_event(event)

                self.screen_plus.handle_event(event)
                self.screen_minus.handle_event(event)

                self.fps_yes.handle_event(event)
                self.fps_no.handle_event(event)

            dif = self.temp_dif
            if dif == "Щадящий":
                self.easy_btn.draw(self.window, temp=1)
                self.veteran_btn.draw(self.window, temp=-1)
                self.hard_btn.draw(self.window, temp=-1)
            if dif == "Ветеран":
                self.easy_btn.draw(self.window, temp=-1)
                self.veteran_btn.draw(self.window, temp=1)
                self.hard_btn.draw(self.window, temp=-1)
            if dif == "Ангел Смерти":
                self.easy_btn.draw(self.window, temp=-1)
                self.veteran_btn.draw(self.window, temp=-1)
                self.hard_btn.draw(self.window, temp=1)

            self.easy_btn.check_hover(pygame.mouse.get_pos())
            self.veteran_btn.check_hover(pygame.mouse.get_pos())
            self.hard_btn.check_hover(pygame.mouse.get_pos())

            self.volume_plus.check_hover(pygame.mouse.get_pos())
            self.volume_minus.check_hover(pygame.mouse.get_pos())

            self.brightness_plus.check_hover(pygame.mouse.get_pos())
            self.brightness_minus.check_hover(pygame.mouse.get_pos())

            self.screen_plus.check_hover(pygame.mouse.get_pos())
            self.screen_minus.check_hover(pygame.mouse.get_pos())

            self.fps_yes.check_hover(pygame.mouse.get_pos())
            self.fps_no.check_hover(pygame.mouse.get_pos())

            self.back_btn.check_hover(pygame.mouse.get_pos())
            if self.setting != [self.temp_screen, int(self.temp_volume), self.temp_brightness, self.temp_dif,
                                str(self.temp_fps)]:
                self.is_veri = True
            else:
                self.is_veri = False
            self.redrawing()
            self.clock.tick(90)
            pygame.display.flip()

    def redrawing(self, full=False):
        self.window.blit(self.background_image, (0, 0))
        if full:
            self.back_btn = Settings_Button(int(self.screen_size[0] / 1.29), 0, int(self.screen_size[0] / 4.4),
                                            int(self.screen_size[1] / 15.2), 'Вернуться',
                                            'resources/pictures/before.png',
                                            'resources/pictures/after.png',
                                            'resources/sound/btn_on.mp3')

            self.easy_btn = Settings_Button(int(self.screen_size[0] / 15.7), int(self.screen_size[1] / 1.65),
                                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43), 'Щадящий',
                                            'resources/pictures/before.png',
                                            'resources/pictures/before.png',
                                            'resources/sound/btn_on.mp3')
            self.veteran_btn = Settings_Button(int(self.screen_size[0] / 2.8), int(self.screen_size[1] / 1.65),
                                               int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43),
                                               'Ветеран',
                                               'resources/pictures/before.png',
                                               'resources/pictures/before.png',
                                               'resources/sound/btn_on.mp3')
            self.hard_btn = Settings_Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 1.65),
                                            int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43),
                                            'Ангел Смерти',
                                            'resources/pictures/before.png',
                                            'resources/pictures/before.png',
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

            self.brightness_status = Settings_Button(int(self.screen_size[0] / 2.58), int(self.screen_size[1] / 3.86),
                                                     int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 10),
                                                     f'{self.temp_brightness}',
                                                     'resources/pictures/after1.png',
                                                     'resources/pictures/before.png',
                                                     'resources/sound/btn_on.mp3')
            self.brightness_plus = Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 3.86),
                                          int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '+',
                                          'resources/pictures/before.png',
                                          'resources/pictures/after.png',
                                          'resources/sound/btn_on.mp3')
            self.brightness_minus = Button(int(self.screen_size[0] / 4), int(self.screen_size[1] / 3.86),
                                           int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '-',
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
            self.fps_yes = Button(int(self.screen_size[0] / 2.5), int(self.screen_size[1] / 1.234),
                                  int(self.screen_size[0] / 11), int(self.screen_size[1] / 12), 'Да',
                                  'resources/pictures/before.png',
                                  'resources/pictures/after1.png',
                                  'resources/sound/btn_on.mp3', is_on=False)
            self.fps_no = Button(int(self.screen_size[0] / 2), int(self.screen_size[1] / 1.234),
                                 int(self.screen_size[0] / 11), int(self.screen_size[1] / 12), 'Нет',
                                 'resources/pictures/before.png',
                                 'resources/pictures/after1.png',
                                 'resources/sound/btn_on.mp3', is_on=True)
            self.verify = Button(int(self.screen_size[0] / 2.75), int(self.screen_size[1] / 1.11),
                                     int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 12), 'Подтвердить',
                                     'resources/pictures/before.png',
                                     'resources/pictures/after1.png',
                                     'resources/sound/btn_on.mp3', is_on=True)
        if self.setting[-1] == 'True':
            s_b = Settings_Button(0, 0, int(self.screen_size[0] / 22), int(self.screen_size[1] / 11.6), '',
                                  'resources/pictures/fps.png')
            s_b.draw(self.window)

            text_show_fps = self.font.render(f"{str(self.clock.get_fps()).split('.')[0]}", True,
                                             self.button_color)

            self.window.blit(text_show_fps, (0, 0))

        dif = self.temp_dif
        if dif == "Щадящий":
            self.easy_btn.draw(self.window, temp=1)
            self.veteran_btn.draw(self.window, temp=-1)
            self.hard_btn.draw(self.window, temp=-1)
        if dif == "Ветеран":
            self.easy_btn.draw(self.window, temp=-1)
            self.veteran_btn.draw(self.window, temp=1)
            self.hard_btn.draw(self.window, temp=-1)
        if dif == "Ангел Смерти":
            self.easy_btn.draw(self.window, temp=-1)
            self.veteran_btn.draw(self.window, temp=-1)
            self.hard_btn.draw(self.window, temp=1)
        if self.is_veri:
            self.verify.check_hover(pygame.mouse.get_pos())
            self.verify.draw(self.window, temp=0)
        self.volume_plus.draw(self.window, temp=10)
        self.volume_minus.draw(self.window, temp=10)
        self.volume_status.draw(self.window)

        self.screen_status.draw(self.window)
        self.screen_plus.draw(self.window, temp=10)
        self.screen_minus.draw(self.window, temp=10)

        self.brightness_plus.draw(self.window, temp=10)
        self.brightness_minus.draw(self.window, temp=10)
        self.brightness_status.draw(self.window)

        self.fps_yes.draw(self.window)
        self.fps_no.draw(self.window)

        self.window.blit(self.text_complexity, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 1.8)))
        self.window.blit(self.text_volume, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 23.2)))
        self.window.blit(self.text_brightness, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 4.46)))
        self.window.blit(self.text_fps, (int(self.screen_size[0] / 2.5), int(self.screen_size[1] / 1.28)))
        self.window.blit(self.text_screen, (int(self.screen_size[0] / 2.85), int(self.screen_size[1] / 2.6)))
        self.previous_screen.blit(self.window, (0, 0))
        self.back_btn.draw(self.window)


    def insert_settings(self, volume, brightness, size):
        self.set_volume(volume)
        self.set_brightness(brightness)
        self.set_difficulty(self.temp_dif)
        print(f'{self.temp_fps}', file=open('resources/settings/fps_status.txt', 'w'))
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
        if size != self.setting[0]:
            self.set_screen(size)
            self.window = pygame.display.set_mode(self.screen_size)
            self.background_image = pygame.image.load("resources/pictures/background_image.png")
            self.background_image = pygame.transform.scale(self.background_image, self.screen_size)
            self.window.blit(self.background_image, (0, 0))
        self.setting = []
        self.setting.append(self.get_screen())
        self.setting.append(self.get_volume())
        self.setting.append(self.get_brightness())
        self.setting.append(self.get_difficulty())
        self.setting.append(str(self.temp_fps))
        self.temp_volume = self.get_volume()
        self.temp_brightness = self.get_brightness()
        self.temp_screen = self.get_screen()
        self.temp_dif = self.get_difficulty()
        self.temp_fps = open('resources/settings/fps_status.txt').read().strip()
        self.is_veri = False
        self.redrawing(True)
        pygame.display.flip()
        self.open()

    def back(self):  # возврат
        pygame.display.set_caption("Grom: Essense of Chaos")
        self.back_object.reopen(self.screen_size[0], self.screen_size[1])

    def set_difficulty(self, arg):
        with open('resources/settings/difficulty.txt', mode="w", encoding="utf-8"):
            pass
        with open('resources/settings/difficulty.txt', mode="a+", encoding="utf-8") as dif:
            dif.write(arg)

    def get_difficulty(self):
        with open('resources/settings/difficulty.txt', mode="r", encoding="utf-8") as dif:
            return dif.readline().strip()

    def set_volume(self, volum):
        self.volume.SetMasterVolumeLevelScalar(float(volum) / 100, None)
        with open("resources/settings/volume_level.txt", mode="w", encoding="utf-8") as volume_file:
            pass
        with open("resources/settings/volume_level.txt", mode="w", encoding="utf-8") as volume_file:
            print(str(int(volum)), file=volume_file)

    def get_volume(self):
        with open("resources/settings/volume_level.txt", mode="r", encoding="utf-8") as volume_file:
            return int(volume_file.readline().strip())

    def set_brightness(self, brightness):
        self.c = wmi.WMI(namespace='wmi')
        self.methods = self.c.WmiMonitorBrightnessMethods()[0]
        self.methods.WmiSetBrightness(str(brightness), 0)

        with open("resources/settings/brightness_level.txt", mode="w", encoding="utf-8") as file:
            pass
        with open("resources/settings/brightness_level.txt", mode="w", encoding="utf-8") as file:
            print(str(brightness), file=file)

    def get_brightness(self):
        with open("resources/settings/brightness_level.txt", mode="r", encoding="utf-8") as file:
            return int(file.readline().strip())

    def get_screen(self):
        with codecs.open("resources/settings/screen_status.txt") as file1:
            return int(file1.readline().strip())

    def set_screen(self, new):
        with open("resources/settings/screen_status.txt", mode="w", encoding="utf-8") as file:
            pass
        with open("resources/settings/screen_status.txt", mode="w", encoding="utf-8") as file:
            print(new, file=file)
        if self.screen_list[int(self.temp_screen)].split()[0] == 'Полноэкранный':
            self.screen_size = (self.max_widht,
                                self.max_height)
        else:
            self.screen_size = (int(self.screen_list[int(self.get_screen())].split()[0]),
                                int(self.screen_list[int(self.get_screen())].split()[-1]))
