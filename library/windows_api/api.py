import os
import sys
import PIL
import time
import ctypes

try:
    from library.windows_api.common import *

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.windows_api.common import *


gdi32 = ctypes.WinDLL("gdi32")
user32 = ctypes.WinDLL("user32")
kernel32 = ctypes.WinDLL("Kernel32")


class Windows_api():
    @staticmethod
    def find_window(
        class_name: str = None,
        window_name: str = None
    ) -> int | None:
        """
        Find a window by it's class_name or window_name

        Args:
            class_name (str, optional):
                If None, will match any window with a matching window_name.
            
            window_name (str, optional):
                If None, will match all window.
  
            window_name:
                If this is None, it will find all window.
            
        Returns:
            int: 
                The handle (HWND) of the window,
                return None if no window is found.
                
        Note:
            - The method return the first matching window if multiple exist.
        """
        find_window = user32.FindWindowW
        find_window.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
        find_window.restype = ctypes.c_void_p

        return user32.FindWindowW(class_name, window_name)


    @staticmethod
    def set_foreground_window(hwnd: int):
        """
        Bring a window to the foreground.
        
        Args:
            hwnd (int):
                The handle (HWND) of the window to bring to the foreground,
                typically obtained from `find_window` method.
        """
        set_foreground_window = user32.SetForegroundWindow
        set_foreground_window.argtypes = [ctypes.c_int]
        set_foreground_window.restype = ctypes.c_bool

        result = set_foreground_window(hwnd)

        if result is False:
            raise ctypes.WinError()


    @staticmethod
    def get_window_size(hwnd: int) -> tuple[int]:
        """
        Get the size of a specified window.
        
        Args:
            hwnd (int):
                The handle (HWND) of the window to get size for,
                typically obtained from `find_window` method.
                
        Returns:
            tuple[int]: 
                A tuple containing (left, top, width, height) information.
        """
        rect = ctypes.wintypes.RECT()

        get_window_attribute = ctypes.windll.dwmapi.DwmGetWindowAttribute
        get_window_attribute.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.wintypes.RECT),
            ctypes.c_int
        ]
        get_window_attribute.restype = ctypes.c_int

        result = get_window_attribute(
            hwnd,
            DWMWA_EXTENDED_FRAME_BOUNDS,
            ctypes.byref(rect),
            ctypes.sizeof(rect)
        )

        if result == 0:
            return (
                rect.left,
                rect.top,
                rect.right - rect.left,
                rect.bottom - rect.top
            )

        else:
            raise ctypes.WinError(code=result)


    @staticmethod
    def get_screen_size() -> tuple[int]:
        """
        Get the size of the primary monitor.
                
        Returns:
            tuple[int]:
                A tuple containing (width, height) information.
        """
        devmode = DEVMODEA()
        devmode.dmSize = ctypes.sizeof(DEVMODEA)

        enum_display_settings = user32.EnumDisplaySettingsW
        enum_display_settings.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_int,
            ctypes.POINTER(DEVMODEA)
        ]
        enum_display_settings.restype = ctypes.c_bool

        result = user32.EnumDisplaySettingsW(None, -1, ctypes.byref(devmode))

        if result is False:
            raise ctypes.WinError()

        else:
            return (devmode.dmPelsWidth, devmode.dmPelsHeight)


    @staticmethod
    def get_mouse_position() -> tuple:
        """
        Get the current mouse position on the screen.
        
        Returns:
            tuple: 
                A tuple containing (x, y) coordinates of the mouse.
        """
        point = ctypes.wintypes.POINT()

        get_cursor_pos = user32.GetCursorPos
        get_cursor_pos.argtypes = [ctypes.POINTER(ctypes.wintypes.POINT)]
        get_cursor_pos.restype = ctypes.c_bool

        result = get_cursor_pos(ctypes.byref(point))

        if result is False:
            return ctypes.WinError(code=kernel32.GetLastError())

        else:
            return (point.x, point.y)


    @staticmethod
    def get_mouse_speed() -> int:
        """
        Get the mouse speed in the Windows system setting.
        
        Returns:
            tuple: 
                The mouse speed setting (ranges from 1 to 20).
        """
        speed = ctypes.c_int()

        system_parameters_info = user32.SystemParametersInfoW
        system_parameters_info.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_int
        ]
        system_parameters_info.restype = ctypes.c_bool

        result = system_parameters_info(
            SPI_GETMOUSESPEED,
            0,
            ctypes.byref(speed),
            0
        )

        if result is False:
            return ctypes.WinError(code=kernel32.GetLastError())

        else:
            return speed.value


    @staticmethod
    def set_mouse_speed(speed: int):
        """
        Set the mouse speed in the Windows system setting.
        
        Args:
            speed (int):
                The mouse speed setting (ranges from 1 to 20).
        """
        system_parameters_info = user32.SystemParametersInfoW
        system_parameters_info.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]
        system_parameters_info.restype = ctypes.c_bool

        result = system_parameters_info(
            SPI_SETMOUSESPEED,
            0,
            speed,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )

        if result is False:
            return ctypes.WinError(code=kernel32.GetLastError())


    @staticmethod
    def send_input(input_type: int, event: int, **kwargs):
        """
        Synthesize keystrokes, mouse motions and button clicks.

        Args:
            input_type: 
                Type of input to simulate (mouse: 0, keyboard: 1). 

            event: 
                Specific event to simulate. (See common.py)
        """

        input_message = INPUT(type=ctypes.c_ulong(input_type))

        if input_type is INPUT_MOUSE:
            input_message.mi = MOUSEINPUT(
                dx=kwargs["dx"],
                dy=kwargs["dy"],
                mouseData=kwargs["mouse_data"],
                dwFlags=event,
                time=0
            )

        elif input_type is INPUT_KEYBOARD:
            input_message.ki = KEYBDINPUT(
                wVk=kwargs["virtual_key"],
                wScan=0,
                dwFlags=event,
                time=0
            )

        user32.SendInput(
            1,
            ctypes.pointer(input_message),            
            ctypes.sizeof(INPUT)
        )

    @staticmethod
    def screenshot(
        hwnd: int,
        size: tuple[int] = None,
        filepath: str = None
    ) -> str:
        # https://github.com/BoboTiG/python-mss

        if size is None:
            x, y, w, h = Windows_api.get_window_size(hwnd)

        else:
            x, y, w, h = size

        if filepath is None:
            filepath = f"screenshot/{int(time.time_ns())}.bmp"

        srcdc = user32.GetWindowDC(0)
        memdc = gdi32.CreateCompatibleDC(srcdc)

        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        bmi.bmiHeader.biClrUsed = 0
        bmi.bmiHeader.biClrImportant = 0

        bmi.bmiHeader.biWidth = w
        bmi.bmiHeader.biHeight = -h

        data = ctypes.create_string_buffer(w * h * 4)

        bmp = gdi32.CreateCompatibleBitmap(srcdc, w, h)
        gdi32.SelectObject(memdc, bmp)

        gdi32.BitBlt(memdc, 0, 0, w, h, srcdc, x, y, SRCCOPY | CAPTUREBLT)
        gdi32.GetDIBits(memdc, bmp, 0, h, data, bmi, DIB_RGB_COLORS)

        raw = bytearray(data)
        rgb = bytearray(w * h * 3)
        rgb[::3] = raw[2::4]
        rgb[1::3] = raw[1::4]
        rgb[2::3] = raw[::4]

        data = bytes(rgb)

        image = PIL.Image.new("RGB", (w, h))
        image.frombytes(data)
        image.save(filepath)

        return filepath