import os
import sys
import time
import keyboard

try:
    from library.general.action import Keyboard
    from library.windows_api.api import Windows_api
    from library.auto_lyre.midi import Midi

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.general.action import Keyboard
    from library.windows_api.api import Windows_api
    from library.auto_lyre.midi import Midi


speed = 1
is_pause = False


class Hotkey():
    def __init__(self):
        self.hotkeys = [
            {"key": "d", "callback": self.speedup},
            {"key": "a", "callback": self.speeddown},
            {"key": "space", "callback": self.pause}
        ]


    def start(self):
        for hotkey in self.hotkeys:
            keyboard.add_hotkey(
                hotkey=hotkey["key"],
                callback=hotkey["callback"]
            )


    def speedup(self):
        if speed < 5:
            speed += 0.2


    def speeddown(self):
        if speed > 0.2:
            speed -= 0.2


    def pause(self):
        is_pause = not is_pause


def play(sheet):
    information = sheet.pop(0)
    #Hotkey().start()
    
    for element in sheet:
        #print(speed)
        press_keys, wait = element[0], element[1]
        print(press_keys, wait)
        
        if len(press_keys) == 1:
            if press_keys[0] is not None:
                Keyboard.press(press_keys)
        
        else:
            Keyboard.press(press_keys)
        
        time.sleep(wait)# * (1 / speed))


if __name__ == "__main__":
    import pyuac
    
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    else:
        window = Windows_api.find_window(window_name="原神")
        Windows_api.set_foreground_window(window)
        time.sleep(3)
        sheet = Midi().process("midi/Never_Gonna_Give_You_Up.mid")
        play(sheet)