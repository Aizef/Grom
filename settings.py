import sys
import pygame
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import wmi
from Buttons import Settings_Button, Button


class Settings:
    def __init__(self, window_width, window_height, screen, last_object):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.window_width = window_width
        self.window_height = window_height

        #  код отвечает за изменение яркости
        self.set_brightness(self.get_brightness())
        self.screen_size = (window_width, window_height)
        #  код отвечает за изменение звука
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.set_volume(float(self.get_volume()) / 100)
        #  рисуем окно настроек
        # self.window = pygame.display.set_mode((self.window_width, self.window_height))
        # self.screen_size = (1100, 580)
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background_image = pygame.image.load("resources/background_image.png")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_size)
        self.window.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Настройки")
        self.button_color = (255, 205, 234)
        self.button_text_color = (0, 0, 0)
        self.font = pygame.font.Font("resources/shrift.otf", 45)

        #  создание надписей
        text_complexity = self.font.render("Изменение уровня сложности", True, self.button_color)
        text_volume = self.font.render("Изменение уровня громкости", True, self.button_color)
        text_fps = self.font.render("Отображать FPS?", True, self.button_color)
        text_brightness = self.font.render("Изменение уровня яркости", True, self.button_color)
        self.text_show_fps = self.font.render(f"", True, self.button_color)

        #  создание кнопок

        self.back_btn = Settings_Button(int(self.screen_size[0] / 1.29), 0, int(self.screen_size[0] / 4.4),
                                        int(self.screen_size[1] / 15.2), 'Вернуться',
                                        'resources/before.png',
                                        'resources/after.png',
                                        'resources/btn_on.mp3')

        self.easy_btn = Settings_Button(int(self.screen_size[0] / 15.7), int(self.screen_size[1] / 1.85),
                                        int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43), 'Щадящий',
                                        'resources/before.png',
                                        'resources/before.png',
                                        'resources/btn_on.mp3')
        self.veteran_btn = Settings_Button(int(self.screen_size[0] / 2.75), int(self.screen_size[1] / 1.85),
                                           int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43), 'Ветеран',
                                           'resources/before.png',
                                           'resources/before.png',
                                           'resources/btn_on.mp3')
        self.hard_btn = Settings_Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 1.85),
                                        int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43),
                                        'Ангел Смерти',
                                        'resources/before.png',
                                        'resources/before.png',
                                        'resources/btn_on.mp3')

        self.volume_status = Settings_Button(int(self.screen_size[0] / 2.58), int(self.screen_size[1] / 11.6),
                                             int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 10),
                                             f'{self.get_volume()}',
                                             'resources/after1.png',
                                             'resources/before.png',
                                             'resources/btn_on.mp3')
        self.volume_plus = Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 11.6),
                                  int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '+',
                                  'resources/before.png',
                                  'resources/after.png',
                                  'resources/btn_on.mp3')
        self.volume_minus = Button(int(self.screen_size[0] / 4), int(self.screen_size[1] / 11.6),
                                   int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '-',
                                   'resources/before.png',
                                   'resources/after.png',
                                   'resources/btn_on.mp3')

        self.brightness_status = Settings_Button(int(self.screen_size[0] / 2.58), int(self.screen_size[1] / 3.15),
                                                 int(self.screen_size[0] / 3.6), int(self.screen_size[1] / 10),
                                                 f'{self.get_brightness()}',
                                                 'resources/after1.png',
                                                 'resources/before.png',
                                                 'resources/btn_on.mp3')
        self.brightness_plus = Button(int(self.screen_size[0] / 1.5), int(self.screen_size[1] / 3.15),
                                      int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '+',
                                      'resources/before.png',
                                      'resources/after.png',
                                      'resources/btn_on.mp3')
        self.brightness_minus = Button(int(self.screen_size[0] / 4), int(self.screen_size[1] / 3.15),
                                       int(self.screen_size[0] / 7.33), int(self.screen_size[1] / 10), '-',
                                       'resources/before.png',
                                       'resources/after.png',
                                       'resources/btn_on.mp3')

        self.fps_yes = Button(int(self.screen_size[0] / 2.55), int(self.screen_size[1] / 1.3),
                              int(self.screen_size[0] / 11), int(self.screen_size[1] / 10), 'Да',
                              'resources/before.png',
                              'resources/after1.png',
                              'resources/btn_on.mp3', is_on=False)
        self.fps_no = Button(int(self.screen_size[0] / 1.9), int(self.screen_size[1] / 1.3),
                             int(self.screen_size[0] / 11), int(self.screen_size[1] / 10), 'Нет',
                             'resources/before.png',
                             'resources/after1.png',
                             'resources/btn_on.mp3', is_on=True)

        with open("resources/fps_status.txt", mode="r", encoding="utf-8") as fps_file:
            fps_status = fps_file.readline().strip()
        if fps_status == "True":
            self.fps_yes.is_hovered = True
            self.fps_yes.is_on = True
        else:
            self.fps_no.is_hovered = True
            self.fps_yes.is_on = False

        # выставление уровня сложности
        dif = self.get_difficulty()

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

        # рендер кнопок
        self.window.blit(text_complexity, (int(self.screen_size[0] / 3.1), int(self.screen_size[1] / 2.1)))
        self.window.blit(text_volume, (int(self.screen_size[0] / 3.1), int(self.screen_size[1] / 24.9)))
        self.window.blit(text_brightness, (int(self.screen_size[0] / 3.1), int(self.screen_size[1] / 4.1)))
        self.window.blit(text_fps, (int(self.screen_size[0] / 2.7), int(self.screen_size[1] / 1.4)))

        if self.fps_yes.is_on:
            self.text_show_fps = self.font.render(f"{self.clock.get_fps()}", True, self.button_color)

        self.window.blit(self.text_show_fps, (0, 0))

        self.volume_status.draw(self.window)
        self.volume_plus.draw(self.window, temp=10)
        self.volume_minus.draw(self.window, temp=10)

        self.brightness_status.draw(self.window)
        self.brightness_plus.draw(self.window, temp=10)
        self.brightness_minus.draw(self.window, temp=10)

        self.fps_yes.draw(self.window)
        self.fps_no.draw(self.window)

        self.back_btn.draw(self.window)

        self.previous_screen = screen
        self.back_object = last_object

        #  рендер окна
        self.previous_screen.blit(self.window, (0, 0))
        pygame.display.flip()

    def open(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    a = self.get_difficulty()
                    self.set_difficulty(a)
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.brightness_minus.is_hovered:
                        self.decrease_brightness(self.get_brightness())
                        self.brightness_status.text = str(self.get_brightness())

                        self.brightness_status.draw(self.window)
                        self.brightness_plus.draw(self.window, temp=10)
                        self.brightness_minus.draw(self.window, temp=10)

                        pygame.display.flip()
                    elif self.brightness_plus.is_hovered:
                        self.increase_brightness(self.get_brightness())
                        self.brightness_status.text = str(self.get_brightness())

                        self.brightness_status.draw(self.window)
                        self.brightness_plus.draw(self.window, temp=10)
                        self.brightness_minus.draw(self.window, temp=10)

                        pygame.display.flip()

                    elif self.volume_plus.is_hovered:
                        self.increase_volume(self.get_volume())

                        self.volume_status.text = str(int(str(str(float(self.get_volume())).split(".")[0])))

                        self.volume_status.draw(self.window)
                        self.volume_plus.draw(self.window, temp=10)
                        self.volume_minus.draw(self.window, temp=10)

                        pygame.display.flip()
                    elif self.volume_minus.is_hovered:
                        self.decrease_volume(self.get_volume())

                        self.volume_status.text = str(int(str(str(float(self.get_volume())).split(".")[0])))

                        self.volume_status.draw(self.window)
                        self.volume_plus.draw(self.window, temp=10)
                        self.volume_minus.draw(self.window, temp=10)

                        pygame.display.flip()

                    elif self.fps_yes.is_hovered:

                        with open("resources/fps_status.txt", mode="w", encoding="utf-8") as fps_file:
                            print("True", file=fps_file)

                        self.fps_yes.is_on = True

                        temp = pygame.image.load("resources/after1.png")
                        self.fps_yes.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))

                        temp = pygame.image.load("resources/before.png")
                        self.fps_no.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))

                        self.fps_yes.draw(self.window)
                        self.fps_no.draw(self.window)

                        pygame.display.flip()

                    elif self.fps_no.is_hovered:

                        with open("resources/fps_status.txt", mode="w", encoding="utf-8") as fps_file:
                            print("False", file=fps_file)

                        self.fps_yes.is_on = False

                        temp = pygame.image.load("resources/before.png")
                        self.fps_yes.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))

                        temp = pygame.image.load("resources/after1.png")
                        self.fps_no.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 11), int(self.screen_size[1] / 10)))

                        self.fps_yes.draw(self.window)
                        self.fps_no.draw(self.window)

                        pygame.display.flip()

                    elif self.easy_btn.is_hovered:
                        self.set_difficulty("Щадящий")

                        temp = pygame.image.load("resources/after1.png")
                        self.easy_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/before.png")
                        self.veteran_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/before.png")
                        self.hard_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        self.easy_btn.draw(self.window)
                        self.veteran_btn.draw(self.window)
                        self.hard_btn.draw(self.window)

                        pygame.display.flip()

                    elif self.veteran_btn.is_hovered:
                        self.set_difficulty("Ветеран")

                        temp = pygame.image.load("resources/before.png")
                        self.easy_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/after1.png")
                        self.veteran_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/before.png")
                        self.hard_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        self.easy_btn.draw(self.window)
                        self.veteran_btn.draw(self.window)
                        self.hard_btn.draw(self.window)

                        pygame.display.flip()
                    elif self.hard_btn.is_hovered:
                        self.set_difficulty("Ангел Смерти")

                        temp = pygame.image.load("resources/before.png")
                        self.easy_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/before.png")
                        self.veteran_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        temp = pygame.image.load("resources/after1.png")
                        self.hard_btn.hover_image = pygame.transform.scale(temp, (int(self.screen_size[0] / 3.66), int(self.screen_size[1] / 7.43)))

                        self.easy_btn.draw(self.window)
                        self.veteran_btn.draw(self.window)
                        self.hard_btn.draw(self.window)

                        pygame.display.flip()

                    elif self.back_btn.is_hovered:
                        self.back()

                self.easy_btn.handle_event(event)
                self.veteran_btn.handle_event(event)
                self.hard_btn.handle_event(event)

                self.volume_plus.handle_event(event)
                self.volume_minus.handle_event(event)

                self.brightness_plus.handle_event(event)
                self.brightness_minus.handle_event(event)

                self.fps_yes.handle_event(event)
                self.fps_no.handle_event(event)

            if self.fps_yes.is_on:
                s_b = Settings_Button(0, 0, int(self.screen_size[0] / 22), int(self.screen_size[1] / 11.6), '', 'resources/fps.png')
                s_b.draw(self.window)

                text_show_fps = self.font.render(f"{str(self.clock.get_fps()).split('.')[0]}", True,
                                                 self.button_color)

                self.window.blit(text_show_fps, (0, 0))
            else:
                s_b = Settings_Button(0, 0, int(self.screen_size[0] / 22), int(self.screen_size[1] / 11.6), '', 'resources/fps.png')
                s_b.draw(self.window)

                pygame.display.flip()
            self.easy_btn.check_hover(pygame.mouse.get_pos())
            self.veteran_btn.check_hover(pygame.mouse.get_pos())
            self.hard_btn.check_hover(pygame.mouse.get_pos())

            self.volume_plus.check_hover(pygame.mouse.get_pos())
            self.volume_minus.check_hover(pygame.mouse.get_pos())

            self.brightness_plus.check_hover(pygame.mouse.get_pos())
            self.brightness_minus.check_hover(pygame.mouse.get_pos())

            self.fps_yes.check_hover(pygame.mouse.get_pos())
            self.fps_no.check_hover(pygame.mouse.get_pos())

            self.back_btn.check_hover(pygame.mouse.get_pos())

            self.volume_plus.draw(self.window, temp=10)
            self.volume_minus.draw(self.window, temp=10)

            self.brightness_plus.draw(self.window, temp=10)
            self.brightness_minus.draw(self.window, temp=10)

            self.back_btn.draw(self.window)
            pygame.display.flip()

            self.clock.tick(90)

    def back(self):  # возврат
        pygame.display.set_caption("Grom: Essense of Chaos")
        self.back_object.main_menu()


    def set_difficulty(self, arg):
        with open('resources/difficulty.txt', mode="w", encoding="utf-8"):
            pass
        with open('resources/difficulty.txt', mode="a+", encoding="utf-8") as dif:
            dif.write(arg)

    def get_difficulty(self):
        with open('resources/difficulty.txt', mode="r", encoding="utf-8") as dif:
            return dif.readline()

    def set_volume(self, volum):
        self.volume.SetMasterVolumeLevelScalar(float(volum), None)
        with open("resources/volume_level.txt", mode="w", encoding="utf-8") as volume_file:
            pass
        with open("resources/volume_level.txt", mode="w", encoding="utf-8") as volume_file:
            print(str(int(volum * 100)), file=volume_file)

    def get_volume(self):
        with open("resources/volume_level.txt", mode="r", encoding="utf-8") as volume_file:
            return volume_file.readline().strip()

    def increase_volume(self, current_volume):
        self.set_volume(float(current_volume) / 100 + 0.1) if float(current_volume) <= 90 else print("")

    def decrease_volume(self, current_volume):
        self.set_volume(float(current_volume) / 100 - 0.1) if 0 < float(current_volume) <= 100 else print("")

    def increase_brightness(self, current_brightness):
        self.set_brightness(current_brightness + 10) if current_brightness <= 90 else print("")

    def decrease_brightness(self, current_brightness):
        self.set_brightness(current_brightness - 10) if 0 < current_brightness <= 100 else print("")

    def set_brightness(self, brightness):
        self.c = wmi.WMI(namespace='wmi')
        self.methods = self.c.WmiMonitorBrightnessMethods()[0]
        self.methods.WmiSetBrightness(brightness, 0)

        with open("resources/brightness_level.txt", mode="w", encoding="utf-8") as file:
            pass
        with open("resources/brightness_level.txt", mode="w", encoding="utf-8") as file:
            print(str(brightness), file=file)

    def get_brightness(self):
        with open("resources/brightness_level.txt", mode="r", encoding="utf-8") as file:
            return int(file.readline().strip())
