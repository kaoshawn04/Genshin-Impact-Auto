import ctypes
import ctypes.wintypes

import pyuac
import pyautogui
import pyuac.admin
import win32gui, win32con, win32api


def get_window_size(window_name):
    window = win32gui.FindWindow(None, window_name)
    win32gui.SetForegroundWindow(window)
    f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    
    rect = ctypes.wintypes.RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    f(ctypes.wintypes.HWND(window),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect)
        )
    
    return {
            "x": rect.left,
            "y": rect.top, 
            "w": rect.right - (rect.left + 4),
            "h": rect.bottom - (rect.top + 60)
        }
        

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    genshin_window = get_window_size("原神")

    bar_y = genshin_window["y"] + 150 / 1600 * genshin_window["h"]

    while True:
        for x in range(genshin_window["x"], genshin_window["x"] + genshin_window["w"]):
            pixel = pyautogui.pixel(x, int(bar_y))
            if pixel == (255, 255, 192):
                print(pixel)
 

# (638, 404, 1284, 780)