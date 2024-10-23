import sys
import ctypes

from ctypes import wintypes
from typing import Optional

sys.path.append("./libraries/windows_api/common")
from common import *


user32 = ctypes.WinDLL("user32")


class Win32api():
    @staticmethod
    def find_window(class_name: str = None, window_name: str = None) -> int:
        """
        Find window via class and window name,
        return the handle of the window.
        
        Args:
            class_name:
                If this is None, it will find any window
                whose title matches the window_name.

            window_name:
                If this is None, it will find all window.
        """
        
        return user32.FindWindowW(class_name, window_name)
    
    
    @staticmethod
    def set_foreground_window(hwnd: int):
        """
        Set the window into foreground via handle of the window.
        """
        
        user32.SetForegroundWindow(hwnd)
        
        
    @staticmethod
    def get_window_size(hwnd: int) -> tuple:
        rect = ctypes.wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            hwnd,
            DWMWA_EXTENDED_FRAME_BOUNDS,
            ctypes.byref(rect),
            ctypes.sizeof(rect)
        )
        
        return (
                rect.left,
                rect.top, 
                rect.right - (rect.left + 4),
                rect.bottom - (rect.top + 60)
            )
        
        
    @staticmethod
    def get_screen_size() -> tuple:
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
        
        return (w, h)     


    @staticmethod
    def get_cursor_position() -> tuple:
        point = POINT()
        user32.GetCursorPos(ctypes.byref(point))
        
        return (point.x, point.y)
    
       
    @staticmethod
    def send_input(
        type: int,
        event: int,
        dx: int = 0,
        dy: int = 0,
        mouseData: int = 0,
        virtual_key: int = 0
    ):
        """
        Synthesize keystrokes, mouse motions and button clicks.

        Args:
            type: mouse: 0, keyboard: 1
            event: 
                See common.py
            dx (mouse event):
                If event is MOUSEEVENTF_ABSOLUTE (0x8000), 
                this should be int(x * 65535 / screen width).
                Or this will be the numbers of pixel moved.
            dy (mouse input):
                Same as dx.
            wheel (mouse input):
                Positive value for rotate forward,
                negative value for rotate backward.
            virtual_key (keyboard input): The key in ASCII code.
        """

        input = INPUT(type=ctypes.c_ulong(type))

        if type is INPUT_MOUSE:
            input.mi = MOUSEINPUT(
                dx=dx,
                dy=dy,
                mouseData=mouseData,
                dwFlags=event,
                time=0
            )

        elif type is INPUT_KEYBOARD:
            input.ki = KEYBDINPUT(
                wVk=virtual_key,
                wScan=0,
                dwFlags=event,
                time=0
            )

        user32.SendInput(1, ctypes.pointer(input), ctypes.sizeof(INPUT))