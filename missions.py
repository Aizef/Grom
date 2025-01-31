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
        self.shrift_koeff = 35 * self.window_width * self.window_height // 2560 // 1600
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

        self.font = pygame.font.Font("resources/other/shrift.otf", int(self.shrift_koeff * 1.2))

        self.text = self.font.render("Основные комбинации, без которых не одержать победы:", True, (255, 205, 234))

        self.font = pygame.font.Font("resources/other/shrift.otf", int(self.shrift_koeff // 1.11))
        self.comb1_text = self.font.render("Одна голова хорошо, а две мутант! = Дает 100 едениц урона", True,
                                           (255, 205, 234))
        self.comb2_text = self.font.render("Ученье есть свет! = Дает 200 едениц урона", True,
                                           (255, 205, 234))
        self.comb3_text = self.font.render("Я инженер и этим всё сказано! = Урон противника 0", True,
                                           (255, 205, 234))
        self.comb4_text = self.font.render("Искалеченная плоть, искалеченная душа. = Дает 100 едениц здоровья", True,
                                           (255, 205, 234))
        self.comb5_text = self.font.render("Человек хуже мутанта, когда он мутант. = Дает 200 едениц здоровья", True,
                                           (255, 205, 234))

        self.font = pygame.font.SysFont("Times New roman", int(self.shrift_koeff * 1.2))

        self.ben_comb1_text = self.font.render("+ 100 едениц урона", True, (255, 205, 234))
        self.ben_comb2_text = self.font.render("+ 200 едениц урона", True, (255, 205, 234))
        self.ben_comb3_text = self.font.render("Урон противника уменьшен до 0", True, (255, 205, 234))
        self.ben_comb4_text = self.font.render("+100 едениц здоровья", True, (255, 205, 234))
        self.ben_comb5_text = self.font.render("+200 едениц здоровья", True, (255, 205, 234))

        self.comb1_image = pygame.image.load("resources/pictures/c1.png")
        self.comb2_image = pygame.image.load("resources/pictures/c2.png")
        self.comb3_image = pygame.image.load("resources/pictures/c3.png")
        self.comb4_image = pygame.image.load("resources/pictures/c4.png")
        self.comb5_image = pygame.image.load("resources/pictures/c5.png")

        self.comb1_image = pygame.transform.scale(self.comb1_image,
                                                  (493 * self.window_width // 2560, 208 * self.window_height // 1600))
        self.comb2_image = pygame.transform.scale(self.comb2_image,
                                                  (493 * self.window_width // 2560, 208 * self.window_height // 1600))
        self.comb3_image = pygame.transform.scale(self.comb3_image,
                                                  (493 * self.window_width // 2560, 208 * self.window_height // 1600))
        self.comb4_image = pygame.transform.scale(self.comb4_image,
                                                  (493 * self.window_width // 2560, 208 * self.window_height // 1600))
        self.comb5_image = pygame.transform.scale(self.comb5_image,
                                                  (493 * self.window_width // 2560, 208 * self.window_height // 1600))

        self.comb1 = self.comb1_image.get_rect(topleft=(int(self.window_height / 18), int(self.window_height / 7.2)))
        self.comb2 = self.comb2_image.get_rect(topleft=(int(self.window_height / 18), int(self.window_height / 3.5)))
        self.comb3 = self.comb3_image.get_rect(topleft=(int(self.window_height / 18), int(self.window_height / 2.4)))
        self.comb4 = self.comb4_image.get_rect(topleft=(int(self.window_height / 18), int(self.window_height / 1.845)))
        self.comb5 = self.comb5_image.get_rect(topleft=(int(self.window_height / 18), int(self.window_height / 1.47)))

        if self.get_fps_result() == "True":
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (255, 205, 234))
        else:
            self.grom_text_show_fps = self.font.render(f"{self.grom_clock.get_fps()}", True, (0, 0, 0))

        self.first = Button(int(self.window_width / 140.01) + 25, int(self.window_height) - int(self.window_width / 11),
                            int(self.window_width / 3.15),
                            int(self.window_height / 11), 'Перейти к первой миссии',
                            'resources/pictures/after1.png',
                            'resources/pictures/after.png',
                            'resources/sound/btn_on.mp3')
        self.second = Button(int(self.window_width / 3.01) + 25, int(self.window_height) - int(self.window_width / 11),
                             int(self.window_width / 3.15),
                             int(self.window_height / 11), 'Перейти к второй миссии',
                             'resources/pictures/after1.png',
                             'resources/pictures/after.png',
                             'resources/sound/btn_on.mp3')
        self.third = Button(int(2 * self.window_width / 3) + 25, int(self.window_height) - int(self.window_width / 11),
                            int(self.window_width / 3.15),
                            int(self.window_height / 11), 'Перейти к третьей миссии',
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
                if event.type == pygame.MOUSEBUTTONDOWN:
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

        self.window.blit(self.text,
                         (int(self.window_height / 18), self.window_height // 12))
        self.window.blit(self.comb1_text,
                         (int(self.window_height / 18) + 500, int(self.window_height / 7.2 + 191 / 2)))
        self.window.blit(self.comb2_text,
                         (int(self.window_height / 18) + 500, int(self.window_height / 3.5 + 191 / 2)))
        self.window.blit(self.comb3_text,
                         (int(self.window_height / 18) + 500, int(self.window_height / 2.4 + 191 / 2)))
        self.window.blit(self.comb4_text,
                         (int(self.window_height / 18) + 500, int(self.window_height / 1.845 + 191 / 2)))
        self.window.blit(self.comb5_text,
                         (int(self.window_height / 18) + 500, int(self.window_height / 1.47 + 191 / 2)))

        self.window.blit(self.comb1_image, self.comb1.topleft)
        self.window.blit(self.comb2_image, self.comb2.topleft)
        self.window.blit(self.comb3_image, self.comb3.topleft)
        self.window.blit(self.comb4_image, self.comb4.topleft)
        self.window.blit(self.comb5_image, self.comb5.topleft)

        if self.get_fps_result() == "True":
            self.window.blit(self.grom_text_show_fps, (0, 0))

    def back(self):  # возврат
        pygame.display.set_caption("Grom: Essense of Chaos")
        self.back_object.main_menu()

    def get_fps_result(self):
        return json.load(open('resources/settings/settings.json'))['fps_status']
