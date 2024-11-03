import time

from ultralytics import YOLO

from library.general.action import Mouse, Keyboard
from windows_api.api import Win32api


class Auto_fish():
    def __init__(self, hwnd, confidence_threshold = 0.8):
        self.hwnd = hwnd
        self.confidence_threshold = confidence_threshold
        self.model = YOLO("C:/Users/kaosh/OneDrive/桌面/Genshin-Impact-Auto/assets/yolo model/best.pt")
        self.fishes_name = [
            "a"
        ]
    
    
    def detect_fish(self, image_path):
        fish = []
        
        predict_result = self.model.predict(
            source=image_path,
            conf=self.confidence_threshold,
            verbose=False,
            save=True
        )
        
        for r in predict_result[0].boxes.data.tolist():
            x1, y1, x2, y2, confidence, name = r
            print("xy", x1, x2, y1, y2)
            fish.append({
                #"name": self.fishes_name[name],
                "center_x": (x1 + x2) / 2,
                "center_y": (y1 + y2) / 2
            })
            
        return fish
            
            
    def throw_rod(self, x, y):
        title_bar_height = 56
        window_x, window_y, _, _ = Win32api.get_window_size(self.hwnd).values()
        print(window_x, window_y)
        
        x += window_x
        y += window_y
        print(x, y)
        
        Mouse.drag(int(x), int(y), "abs")
    

if __name__ == "__main__":
    import pyuac
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    window = Win32api.find_window(window_name="原神")
    Win32api.set_foreground_window(window)

    fishing = Auto_fish(window)
    time.sleep(2)
    print("checks")
    fish = fishing.detect_fish(Win32api.screenshot(window))
    target = fish[0]
    print("tc", target["center_x"], target["center_y"])
    fishing.throw_rod(target["center_x"], target["center_y"])
    print("check 2")