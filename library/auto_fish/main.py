import os
import sys
import time
import pyuac
import traceback

from ultralytics import YOLO

try:
    from library.common.action import Mouse, Keyboard
    from library.windows.api import Windows_api

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)
    
    from library.common.action import Mouse, Keyboard
    from library.windows.api import Windows_api


class Auto_fish():
    def __init__(self, hwnd, confidence_threshold = 0.8):
        self.hwnd = hwnd
        self.hwnd_size = Windows_api.get_window_size(self.hwnd)
        
        self.confidence_threshold = confidence_threshold
        
        self.model = YOLO("C:/Users/kaosh/OneDrive/桌面/GENSHIN-IMPACT-AUTO/assets/yolo model/best.pt")
        self.model.track(persist=False)
    
    
    def detect_fish(self, source_path = None, target_name = None, target_id = None):
        if source_path is None:
            source_path = Windows_api.screenshot(self.hwnd)
        
        counter = 0
        
        predict_result = self.model.track(
            source=source_path,
            conf=self.confidence_threshold,
            verbose=False,
            persist=True,
            save=True
        )
        
        result = []
        
        for box in predict_result[0].boxes:
            result.append({
                "id": int(box.id) if box.id else None,
                "name": predict_result[0].names[int(box.cls)],
                "size": tuple(map(int, box.xywh.tolist()[0]))
            })

        return result
                 
    
    def throw_rod(self, want_fish_name):
        try:
            x_unit_movement = 20
            y_unit_movement = 20
            target = self.detect_fish(target_class_name=want_fish_name)
            window_size = Windows_api.get_window_size(self.hwnd)
            
            Mouse.clickdown()
            
            while abs(target["size"][0] - (window_size[2] // 2)) >= 50:
                #x_unit_movement *= (target["size"][0] - (window_size[2] // 2)) / 100
                #y_unit_movement *= (target["size"][1] - (window_size[3] // 2)) / 100
                x_unit_movement *= 1 if target["size"][0] - (window_size[2] // 2) > 0 else -1
                y_unit_movement *= 1 if target["size"][1] - (window_size[3] // 2) > 0 else -1
                print(int(abs(target["size"][0] - (window_size[2] // 2))), int(abs(target["size"][1] - (window_size[3] // 2))))
                
                Mouse.move(int(x_unit_movement), int(y_unit_movement))
                
                target = self.detect_fish(target_id=target["id"])
                
            Mouse.clickup()
            
            time.sleep(50)

        except Exception:
            print(traceback.format_exc())
            time.sleep(50)
            
        
    def main(self):
        want_fish_name = ["Pufferfish", "Bitter Pufferfish"]
        
        result = self.detect_fish()