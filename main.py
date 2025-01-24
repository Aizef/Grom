import ctypes

from Grom import Grom

if __name__ == "__main__":
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    example = Grom(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    example.main_menu()