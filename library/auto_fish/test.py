import os
import sys
import time
import traceback

import numpy as np

from ultralytics import YOLO

try:
    from library.general.action import Mouse, Keyboard
    from library.windows_api.api import Windows_api

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)
    
    from library.general.action import Mouse, Keyboard
    from library.windows_api.api import Windows_api


class Auto_fish():
    def __init__(self, hwnd, confidence_threshold = 0.8):
        self.hwnd = hwnd
        self.confidence_threshold = confidence_threshold
        self.fish_class_name = [
            "Aizen Medaka",
            "Akai Maou",
            "Bitter Pufferfish",
            "Crystalfish",
            "Dawn-catch-er",
            "Medaka",
            "Pufferfish",
            "Tea-Colored Shirakodai",
            "Venomspine Fish"
        ]
        
        self.model = YOLO("C:/Users/kaosh/OneDrive/桌面/Genshin-Impact-Auto/assets/yolo model/best.pt")
        self.model.track(persist=True)
    
    
    def detect_fish(self, target_class_name = None, target_id = None):
        predict_result = [None]
        timer = 0
        while predict_result[0] is None and timer < 5:
            timer += 1
            predict_result = self.model.track(
                Windows_api.screenshot(self.hwnd),
                verbose=False,
                persist=True,
                save=False,
                conf=0.7
            )
        
        # if predict_result[0] is None:
        #     self.detect_fish(target_class_name, target_id)
        
        if target_class_name is None and target_id is None:
            return [
                {
                    "id": int(box.id),
                    "class_name": self.fish_class_name[int(box.cls)],
                    "size": tuple(box.xywh.tolist()[0])
                }
                for box in predict_result[0].boxes
            ]   
        
        elif target_class_name is not None:
            box = [
                box 
                for box in predict_result[0].boxes 
                if self.fish_class_name[int(box.cls)] in target_class_name
            ]
            
        elif target_id is not None:
           box = [box for box in predict_result[0].boxes if int(box.id) == target_id]
           
        if len(box) == 0:
            self.detect_fish(target_class_name, target_id)
        
        else:
            return {
                "id": int(box[0].id),
                "class_name": self.fish_class_name[int(box[0].cls)],
                "size": tuple(box[0].xywh.tolist()[0])
            }    
            
    
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
        self.throw_rod(want_fish_name)
        
        
if __name__ == "__main__":
    import pyuac
    
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        
    else:
        af = Auto_fish(Windows_api.find_window(window_name="原神"))
        time.sleep(3)
        af.main()