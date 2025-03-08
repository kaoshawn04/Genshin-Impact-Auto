import os
import sys
import time

try:
    from library.windows.api import Windows_api
    from library.windows.base import *

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.windows.api import Windows_api
    from library.windows.base import *


MINIUM_INTERVAL = 0.001


def adjust_mouse_speed(speed):
    def inner(func):
        def wrapper(*args, **kwargs):
            original_speed = Windows_api.get_mouse_speed()
            Windows_api.set_mouse_speed(speed)
            func(*args, **kwargs)
            Windows_api.set_mouse_speed(original_speed)

        return wrapper
    return inner


class Mouse():
    @staticmethod
    def _mouse_event(event, x = 0, y = 0, wheel = 0):
        Windows_api.send_input(
            input_type=INPUT_MOUSE,
            event=event,
            dx=x,
            dy=y,
            mouse_data=wheel
        )


    @staticmethod
    @adjust_mouse_speed(10)
    def move(x: int, y: int, mode: str = "rel", duration: float = 0, step: int = None):
        mouse_x, mouse_y = Windows_api.get_mouse_position()
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
    def clickdown(mode: str = "left"):
        if mode == "left":
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTDOWN)

        elif mode == "right":
            Mouse._mouse_event(event=MOUSEEVENTF_RIGHTDOWN)


    @staticmethod
    def clickup(mode: str = "left"):
        if mode == "left":
            Mouse._mouse_event(event=MOUSEEVENTF_LEFTUP)

        elif mode == "right":
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

        Windows_api.send_input(
            input_type=INPUT_KEYBOARD,
            event=event,
            virtual_key=virtual_key
        )


    @staticmethod
    def press(keys: str | list, interval: float = MINIUM_INTERVAL):
        keys = keys if isinstance(keys, list) else list(keys)
        
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_KEYDOWN, key=key)
            time.sleep(interval)
            Keyboard._keyboard_event(event=KEYEVENTF_KEYUP, key=key)


    @staticmethod
    def keydown(keys: str | list):
        keys = keys if isinstance(keys, list) else list(keys)
        
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_EXTENDEDKEY, key=key)


    @staticmethod
    def keyup(keys: str | list):
        keys = keys if isinstance(keys, list) else list(keys)
        
        for key in keys:
            Keyboard._keyboard_event(event=KEYEVENTF_KEYUP, key=key)