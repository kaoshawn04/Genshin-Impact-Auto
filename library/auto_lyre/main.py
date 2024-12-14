import os
import sys
import time

try:
    from library.general.action import Mouse, Keyboard
    from library.windows_api.api import Windows_api
    from library.auto_lyre.midi import Midi

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)
    
    from library.general.action import Mouse, Keyboard
    from library.windows_api.api import Windows_api
    from library.auto_lyre.midi import Midi


def play(sheet):
    sheet.pop(0) # duration
    
    for element in sheet:
        press_keys, wait = element[0], element[1]
        
        #print(press_keys, wait)
        
        if len(press_keys) == 1:
            if press_keys[0] is not None:
                Keyboard.press(press_keys[0])
        
        else:
            Keyboard.press(press_keys)
        
        time.sleep(wait)
        
        
if __name__ == "__main__":
    import pyuac
    
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    else:
        window = Windows_api.find_window(window_name="原神")
        Windows_api.set_foreground_window(window)
        time.sleep(5)
        play(Midi("assets/midi/test.mid").process())