import threading
import ctypes
from ctypes import wintypes
import time

class HotkeyListener:
    """
    A hotkey listener implementation using Windows API through ctypes.
    Supports multiple hotkey combinations and custom callbacks.
    """
    
    # Windows API constants
    MOD_ALT = 0x0001
    MOD_CONTROL = 0x0002
    MOD_SHIFT = 0x0004
    MOD_WIN = 0x0008
    
    # Virtual key codes for common keys
    VK_CODES = {
        'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
        'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
        'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
        'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
        'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
        'Z': 0x5A, '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33,
        '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38,
        '9': 0x39, 'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
        'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78,
        'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B
    }
    
    def __init__(self):
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self.running = False
        self.hotkeys = {}
        self.thread = None
        
        # Define required Windows API function prototypes
        self.user32.RegisterHotKey.argtypes = [
            wintypes.HWND, ctypes.c_int, ctypes.c_uint, ctypes.c_uint
        ]
        self.user32.RegisterHotKey.restype = ctypes.c_bool
        
        self.user32.GetMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG), wintypes.HWND,
            ctypes.c_uint, ctypes.c_uint
        ]
        self.user32.GetMessageW.restype = ctypes.c_bool

    def register_hotkey(self, modifiers, key, callback):
        """
        Register a hotkey combination with a callback function.
        
        Args:
            modifiers (list): List of modifier keys ('alt', 'ctrl', 'shift', 'win')
            key (str): The main key (e.g., 'A', 'B', '1', 'F1')
            callback (callable): Function to call when hotkey is pressed
        """
        if not key in self.VK_CODES:
            raise ValueError(f"Unsupported key: {key}")
            
        mod_value = 0
        for mod in modifiers:
            if mod.lower() == 'alt':
                mod_value |= self.MOD_ALT
            elif mod.lower() == 'ctrl':
                mod_value |= self.MOD_CONTROL
            elif mod.lower() == 'shift':
                mod_value |= self.MOD_SHIFT
            elif mod.lower() == 'win':
                mod_value |= self.MOD_WIN
                
        id = len(self.hotkeys) + 1
        success = self.user32.RegisterHotKey(None, id, mod_value, self.VK_CODES[key])
        
        if not success:
            error = ctypes.get_last_error()
            raise RuntimeError(f"Failed to register hotkey. Error code: {error}")
            
        self.hotkeys[id] = callback

    def _listener_thread(self):
        """Internal thread function to listen for hotkey events."""
        try:
            msg = wintypes.MSG()
            while self.running:
                if self.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == 0x0312:  # WM_HOTKEY
                        if msg.wParam in self.hotkeys:
                            self.hotkeys[msg.wParam]()
        except Exception as e:
            print(f"Error in listener thread: {e}")

    def start(self):
        """Start the hotkey listener."""
        if self.thread is not None:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._listener_thread)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the hotkey listener."""
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None
            
        # Unregister all hotkeys
        for id in self.hotkeys:
            self.user32.UnregisterHotKey(None, id)
        self.hotkeys.clear()

# Example usage
if __name__ == "__main__":
    def on_hotkey():
        print("Hotkey pressed!")
        
    def on_quit():
        print("Quitting...")
        listener.stop()
        
    listener = HotkeyListener()
    
    # Register Ctrl+Alt+A
    listener.register_hotkey(['ctrl', 'alt'], 'A', on_hotkey)
    
    # Register Ctrl+Q to quit
    listener.register_hotkey(['ctrl'], 'Q', on_quit)
    
    print("Listening for hotkeys... Press Ctrl+Q to quit")
    listener.start()
    
    # Keep the main thread running
    while listener.running:
        time.sleep(0.1)