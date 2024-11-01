import os
import time
import zlib
import ctypes
import struct

from .common import *


crc32 = zlib.crc32
user32 = ctypes.WinDLL("user32")
gdi32 = ctypes.WinDLL('gdi32')


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
    def get_window_size(hwnd: int) -> dict:
        rect = ctypes.wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            hwnd,
            DWMWA_EXTENDED_FRAME_BOUNDS,
            ctypes.byref(rect),
            ctypes.sizeof(rect)
        )
        
        return {
                "left": rect.left,
                "top": rect.top, 
                "width": rect.right - rect.left, # -(rect.left + 4)
                "height": rect.bottom - rect.top # - (rect.top + 60)
            }
        
        
    @staticmethod
    def get_screen_size() -> tuple:
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
        
        return (w, h)     


    @staticmethod
    def get_mouse_position() -> tuple:
        point = POINT()
        user32.GetCursorPos(ctypes.byref(point))
        
        return (point.x, point.y)
    
    
    @staticmethod
    def get_mouse_speed():
        speed = ctypes.c_int()
        user32.SystemParametersInfoA(SPI_GETMOUSESPEED, 0, ctypes.byref(speed), 0)
        
        return speed.value
    
    
    @staticmethod
    def set_mouse_speed(speed):
        user32.SystemParametersInfoA(
            SPI_SETMOUSESPEED,
            0,
            speed,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )


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
        
        
    @staticmethod
    def screenshot(hwnd: int) -> str:
        # https://github.com/BoboTiG/python-mss
        
        x, y, w, h = Win32api.get_window_size(hwnd).values()
        
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
        bits = gdi32.GetDIBits(memdc, bmp, 0, h, data, bmi, DIB_RGB_COLORS)
        
        raw = bytearray(data)
        rgb = bytearray(w * h * 3)
        rgb[::3] = raw[2::4]
        rgb[1::3] = raw[1::4]
        rgb[2::3] = raw[::4]
        
        data = bytes(rgb)
        
        line = w * 3
        png_filter = struct.pack(">B", 0)
        scanlines = b"".join([png_filter + data[y * line : y * line + line] for y in range(h)])
        
        magic = struct.pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)
        
        ihdr = [b"", b"IHDR", b"", b""]
        ihdr[2] = struct.pack(">2I5B", w, h, 8, 2, 0, 0, 0)
        ihdr[3] = struct.pack(">I", crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
        ihdr[0] = struct.pack(">I", len(ihdr[2]))
        
        idat = [b"", b"IDAT", zlib.compress(scanlines, 6), b""]
        idat[3] = struct.pack(">I", crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
        idat[0] = struct.pack(">I", len(idat[2]))
        
        iend = [b"", b"IEND", b"", b""]
        iend[3] = struct.pack(">I", crc32(iend[1]) & 0xFFFFFFFF)
        iend[0] = struct.pack(">I", len(iend[2]))
        
        filename = f"assets/screenshot/{int(time.time())}.png"
        
        with open(filename, "wb") as fileh:
            fileh.write(magic)
            fileh.write(b"".join(ihdr))
            fileh.write(b"".join(idat))
            fileh.write(b"".join(iend))

            fileh.flush()
            os.fsync(fileh.fileno())
            
        return filename