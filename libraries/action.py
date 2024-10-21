import sys
import time
import pyuac

sys.path.append("./libraries/windows_api")
from windows_api.api import Win32api
from windows_api.common import *
        

class Mouse():
    @staticmethod
    def _mouse_event():
        pass
    
    
    @staticmethod
    def move_to(x: int = None, y: int = None, dx: int = None, dy:int = None):
        if x is None or y is None:
            if dx in None or dy is None:
                raise ValueError("Missing arguments.")
            
            else:
                Mouse._mouse_event(event=MOUSEEVENTF_MOVE, dx=dx, dy=dy)
            
        else:
            Mouse._mouse_event(event=MOUSEEVENTF_ABSOLUTE, dx=dx, dy=dy)
    
    
    @staticmethod
    def drag_to():
        pass
    
    
    @staticmethod
    def click():
        pass
    
    
    @staticmethod
    def scroll():
        pass 
    

class Keyboard():
    @staticmethod
    def _keyboard_event(event: int, key: str):
        if key in virtual_key_map.keys():
            virtual_key = virtual_key_map[key]
            
        else:
            virtual_key = ord(key.upper())
            
        Win32api.send_input(event=event, virtual_key=virtual_key)


    @staticmethod
    def press(keys: str | list, pause: float = None):
        if pause is None:  
            pause = 0.01

        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_KEYDOWN, key=key)
            time.sleep(pause)
            Keyboard._keyboard_event(event=KEYEVENTF_KEYUP, key=key)


    @staticmethod
    def keydown(keys: str | list):
        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_EXTENDEDKEY, key=key)


    @staticmethod
    def keyup(keys: str | list):
        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_KEYUP, key=key) 
    
    
if __name__ == "__main__":
    