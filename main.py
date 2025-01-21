import ctypes
import json
import getpass

import pygame

from Grom import Grom

if __name__ == "__main__":
    s = json.load(open('resources/settings/settings.json'))
    screen_list = []
    pygame.init()
    for i in [res for res in pygame.display.list_modes() if res[0] >= 800 and res[1] >= 600][::-1]:
        screen_list.append(f'{i[0]} x {i[1]}')
    if s['last_user'] == getpass.getuser():
        Gr = Grom(int(screen_list[s['screen_status']].split('x')[0][:-1])
                  , int(screen_list[s['screen_status']].split('x')[1])
                  )
        print(Gr.width, Gr.height)
        Gr.main_menu()
    else:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        for i in range(len(screen_list)):
            if int(screen_list[i].split('x')[0][:-1]) == user32.GetSystemMetrics(0):
                json.dump({"fps_status": "False", "fullscreen_status": 'True',
                           "volume_level": 60, "screen_status": i, "last_user": getpass.getuser()},
                          open('resources/settings/settings.json', 'w'))
                break
        example = Grom(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        example.main_menu()
