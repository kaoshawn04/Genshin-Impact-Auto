import cv2
import time

from ultralytics import YOLO

from action import Mouse, Keyboard
from windows_api.api import Win32api


class Auto_fish():
    def __init__(self, confidence_threshold = 0.8):
        self.confidence_threshold = confidence_threshold
        self.model = YOLO("C:/Users/kaosh/OneDrive/桌面/Genshin-Impact-Auto/assets/yolo model/best.pt")
        self.fishes_name = [
            "a"
        ]
    
    
    def detect_fish(self, image_path):
        fishes = []
        
        predict_result = self.model.predict(
            source=image_path,
            conf=self.confidence_threshold,
            verbose=False,
            save=False
        )
        
        for r in predict_result[0].boxes.data.tolist():
            x1, y1, x2, y2, confidence, name = r
            fishes.append({
                "name": self.fishes_name[name],
                "center_x": (x1 + x2) / 2,
                "center_y": (y1 + y2) / 2
            })
            
        return fishes
            
            
    def throw_rod(self, x, y):
        title_bar_height = 56
        border_width, border_height = Win32api.get_window_border_size().values()
        
        
        Mouse.drag()

if __name__ == "__main__":
    Auto_fish().detect_fish("assets/screenshot/1730449582.png")