import sys
import time

sys.path.append("./libraries/windows_api")
from windows_api.api import Win32api
from windows_api.common import *


class Mouse():
    @staticmethod
    def _mouse_event(event, dx = 0, dy = 0, wheel = 0):
        Win32api.send_input(
            type=INPUT_MOUSE,
            event=event,
            dx=dx,
            dy=dy,
            mouseData=wheel
        )
    
    
    @staticmethod
    def move_to(x: int, y: int, mode: str = "abs"):
        if mode == "rel":
            Mouse._mouse_event(event=MOUSEEVENTF_MOVE, dx=x, dy=y)
                
        elif mode == "abs":
            w, h = Win32api.get_screen_size()
            Mouse._mouse_event(
                event=MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE,
                dx=int(x * 65535 / w),
                dy=int(y * 65535 / h)
            )

    
    @staticmethod
    def drag_to(x: int, y: int, mode: str = "abs", duraton: float = None, steps: int = None):
        if duraton is None:
            duraton = 1
            
        if steps is None:
            steps = 10
            
        if mode == "rel":
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTDOWN)
            
            for dx, dy in zip(range(0, x, x // steps), range(0, y, y // steps)):
                print(dx, dy)
                Mouse._mouse_event(event=MOUSEEVENTF_MOVE, dx=x, dy=y)
                time.sleep(duraton / steps)
        
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTUP)
            
        elif mode == "abs":
            now_x, now_y = Win32api.get_cursor_position()
            x, y = x - now_x, y - now_y

            Mouse._mouse_event(event=MOUSEEVENTF_LEFTDOWN)

            for dx, dy in zip(range(x, step=int(x / steps)), range(y, int(y / steps))):
                Mouse._mouse_event(event=MOUSEEVENTF_MOVE, dx=x, dy=y)
                time.sleep(duraton / steps)
                
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTUP)
            
        
    @staticmethod
    def click(mode: str = "left", pause: float = None):
        if pause is None:
            pause = 0.01
            
        if mode == "left":
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTDOWN)
            time.sleep(pause)
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTUP)
    
        elif mode == "right":
            Mouse._mouse_event(event=MOUSEEVENTF_RIGHTDOWN)
            time.sleep(pause)
            Mouse._mouse_event(event=MOUSEEVENTF_RIGHTUP)
    
    @staticmethod
    def scroll(count: int, duraton: float = None, step: int = None):
        if duraton is None:
            duraton = 1
            
        if step is None:
            step = 10
            
        for delta in range(count, step=count // 10):
            Mouse._mouse_event(event=MOUSEEVENTF_WHEEL, wheel=delta)
            time.sleep(duraton / step)
    

class Keyboard():
    @staticmethod
    def _keyboard_event(event: int, key: str):
        if key in virtual_key_map.keys():
            virtual_key = virtual_key_map[key]
            
        else:
            virtual_key = ord(key.upper())
            
        Win32api.send_input(type=INPUT_KEYBOARD, event=event, virtual_key=virtual_key)


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
    import pyuac
    
    #if not pyuac.isUserAdmin():
    #    pyuac.runAsAdmin()
        
    time.sleep(5)
    Mouse.drag_to(100, 100, "rel")