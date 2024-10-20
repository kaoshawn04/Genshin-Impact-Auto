import sys
import ctypes

sys.path.append("./libraries/windows_api/common.py")
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
    def send_input(event: int, virtual_key: int):
        """
        Synthesize keystrokes, mouse motions and button clicks.

        Args:
            event: keydown: 0, keyup: 2.
            virtual_key: The key in ASCII code.
        """
        input = INPUT(
            type=ctypes.c_ulong(INPUT_KEYBOARD),
            ki=KEYBDINPUT(
                wVk=virtual_key,
                wScan=0,
                dwFlags=event,
                time=0,
                #dwExtraInfo=ctypes.pointer(ctypes.c_ulong(0))
            )
        )
        user32.SendInput(1, ctypes.pointer(input), ctypes.sizeof(INPUT))