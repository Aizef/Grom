import ctypes
from Grom import Grom

if __name__ == "__main__":
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    print(20, file=open('resources/settings/font_settings/font_size.txt','w'))
    example = Grom(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    example.main_menu()
