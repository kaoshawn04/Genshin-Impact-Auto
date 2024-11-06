import os
import sys
import time

try:
    from library.windows_api.api import Win32api
    from library.windows_api.common import *
    
except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)
    
    from library.windows_api.api import Win32api
    from library.windows_api.common import *
    

MINIUM_INTERVAL = 0.001


def adjust_mouse_speed(speed):
    def inner(func):
        def wrapper(*args, **kwargs):
            original_speed = Win32api.get_mouse_speed()
            Win32api.set_mouse_speed(speed)
            func(*args, **kwargs)
            Win32api.set_mouse_speed(original_speed)
            
        return wrapper
    return inner


class Mouse():
    @staticmethod
    def _mouse_event(event, x = 0, y = 0, wheel = 0):
        Win32api.send_input(
            type=INPUT_MOUSE,
            event=event,
            dx=x,
            dy=y,
            mouseData=wheel
        )


    @staticmethod
    @adjust_mouse_speed(10)
    def move(x: int, y: int, mode: str = "rel", duration: float = 0, step: int = None):
        mouse_x, mouse_y = Win32api.get_mouse_position()
        delta_time = 0

        if mode == "abs":
            x -= mouse_x
            y -= mouse_y
            
        if duration == 0:
            Mouse._mouse_event(event=MOUSEEVENTF_MOVE, x=x, y=y)
            return
        
        if step is None:                    
            step = abs(max(x, y)) // 3

        delta_time = duration / step
        
        if delta_time < MINIUM_INTERVAL:
            delta_time = 0
        
        delta_x, delta_y = x // step, y // step
        
        x_decimal_count = step / (x % step) if x % step else 0
        y_decimal_count = step / (y % step) if y % step else 0
        
        for i in range(step):
            if x_decimal_count != 0 and i % x_decimal_count < 1:
                x = delta_x + 1
            
            else:
                x = delta_x
                    
            if y_decimal_count != 0 and i % y_decimal_count < 1:
                y = delta_y + 1
            
            else:
                y = delta_y

            Mouse._mouse_event(event=MOUSEEVENTF_MOVE, x=x, y=y)
            time.sleep(delta_time)

    
    @staticmethod
    def drag(x: int, y: int, mode: str = "rel", duration: float = 1, step: int = None):
        Mouse._mouse_event(event=MOUSEEVENTF_LEFTDOWN)
        Mouse.move(x=x, y=y, mode=mode, duration=duration, step=step)        
        Mouse._mouse_event(event=MOUSEEVENTF_LEFTUP)
            
        
    @staticmethod
    def click(mode: str = "left", interval: float = MINIUM_INTERVAL):
        if mode == "left":
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTDOWN)
            time.sleep(interval)
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTUP)
    
        elif mode == "right":
            Mouse._mouse_event(event=MOUSEEVENTF_RIGHTDOWN)
            time.sleep(interval)
            Mouse._mouse_event(event=MOUSEEVENTF_RIGHTUP)
    
    
    @staticmethod
    def scroll(count: int, duration: float = 1, step: int = None):
        if duration == 0:
            Mouse._mouse_event(event=MOUSEEVENTF_WHEEL, wheel=count)
            return
        
        if step is None:
            step = abs(count)
            
        delta = count // step  
        
        for _ in range(step):
            Mouse._mouse_event(event=MOUSEEVENTF_WHEEL, wheel=delta)
            time.sleep(duration / step)
    

class Keyboard():
    @staticmethod
    def _keyboard_event(event: int, key: str):
        if key in virtual_key_map.keys():
            virtual_key = virtual_key_map[key]
            
        else:
            virtual_key = ord(key.upper())
            
        Win32api.send_input(type=INPUT_KEYBOARD, event=event, virtual_key=virtual_key)


    @staticmethod
    def press(keys: str | list, interval: float = MINIUM_INTERVAL):
        keys = [keys] if type(keys) != list else keys
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_KEYDOWN, key=key)
            time.sleep(interval)
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
    
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    else:
        time.sleep(3)
        window = Win32api.find_window(window_name="原神")
        Win32api.set_foreground_window(window)
        time.sleep(3)
        
        Mouse.move(640 * 4, 0, duration=3)
        #time.sleep(1)
        #Mouse.move(1280, 0, duration=3)
        
        
        
# 水平視角靈敏度, dx == 640, dx == 1280, dx == 1920, dx == 2560
# 5: 110, 225, 335, 450
# 4: 90, 185, 280, 375
# 3: 65, 125, 185, 250
# 2: 30, 65, 90, 125
# 1: 15, 30, 45, 60