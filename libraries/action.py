import time
import pyuac

from windows_api.api import Win32api
from windows_api.common import *


keyboard_map = {
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
}
        

class Keyboard():
    def __init__(self, hwnd):
        self.hwnd = hwnd

 
    def _keyboard_event(self, message, **params):
        key = params["key"].lower()
        
        if key in keyboard_map.keys():
            vitual_key = keyboard_map[key]

        else:
            vitual_key = ord(key)

        Win32api.post_message(self.hwnd, message, vitual_key, 0)


    def press(self, keys: str | list, pause: float = None):
        if pause is None:  
            pause = 0.01

        for key in keys:
            self.keyboard_event(message=0x0100, key=key)
            time.sleep(pause)
            self._keyboard_event(message=0x0101, key=key)


    def keydown(self, keys: str | list):
        for key in keys:
            self._keyboard_event(message=0x0100, key=key)


    def keyup(self, hwnd, keys: str | list):
        for key in keys:
            self._keyboard_event(message=0x0101, key=key)  
            
            
if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    time.sleep(5)
    
    window = Win32api.find_window(window_name="原神")
    Keyboard(window).press("b")