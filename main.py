# импорт библиотек
import ctypes
import json
import getpass

from grom import Grom
from list_modes import List_modes

# проверка: открывалась ли игра до этого и изменялось ли разрешение экрана в предыдущей сессии
if __name__ == "__main__":
    s = json.load(open('resources/settings/settings.json'))
    screen_list = List_modes()
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    #  установка шрифта
    print(25 * int(screen_list[s['screen_status']].split('x')[0][:-1])
                  * int(screen_list[s['screen_status']].split('x')[1]) // user32.GetSystemMetrics(0) // user32.GetSystemMetrics(1),
          file=open('resources/settings/font_settings/font_size.txt', 'w'))
    
    if s['last_user'] == getpass.getuser():  #  проврка пользователя
        Gr = Grom(int(screen_list[s['screen_status']].split('x')[0][:-1])
                  , int(screen_list[s['screen_status']].split('x')[1])
                  )  #  создание окна на основе имеющихся данных
        
        Gr.main_menu()
    else:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        for i in range(len(screen_list)): #  установка настроек на базовые значения
            if int(screen_list[i].split('x')[0][:-1]) == user32.GetSystemMetrics(0):
                json.dump({"fps_status": "False", "fullscreen_status": 'True',
                           "volume_level": 60, "screen_status": i, "last_user": getpass.getuser()},
                          open('resources/settings/settings.json', 'w'))
                break
                
        example = Grom(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)) #  создание окна
        
        example.main_menu()
