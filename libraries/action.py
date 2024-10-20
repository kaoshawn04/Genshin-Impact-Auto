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
    def move_to():
        pass
    
    
    @staticmethod
    def click():
        pass
    
    
    @staticmethod
    def scroll():
        pass 
    

class Keyboard():
    @staticmethod
    def _keyboard_event(message, key):
        if key in virtual_key_map.keys():
            virtual_key = virtual_key_map[key]
            
        else:
            virtual_key = ord(key.upper())
            
        Win32api.send_input(event=message, virtual_key=virtual_key)


    @staticmethod
    def press(keys: str | list, pause: float = None):
        if pause is None:  
            pause = 0.01

        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(message=KEYEVENTF_KEYDOWN, key=key)
            time.sleep(pause)
            Keyboard._keyboard_event(message=KEYEVENTF_KEYUP, key=key)


    @staticmethod
    def keydown(keys: str | list):
        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(message=KEYEVENTF_EXTENDEDKEY, key=key)


    @staticmethod
    def keyup(keys: str | list):
        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(message=KEYEVENTF_KEYUP, key=key)  
            
            
if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    time.sleep(5)
    Keyboard.press(" ")
    