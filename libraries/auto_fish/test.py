import cv2
import sys
import time

from ultralytics import YOLO

sys.path.append("./libraries/windows_api")
from windows_api.api import Win32api


model = YOLO("C:/Users/kaosh/OneDrive/桌面/Genshin-Impact-Auto/assets/yolo model/best.pt")


def detect(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    result = model.predict(source=image, show=True, save=True)
    
    print(result)
    for r in result:
        print(r.boxes.data)
    

if __name__ == "__main__":
    window = Win32api.find_window(window_name="原神")
    Win32api.set_foreground_window(window)
    time.sleep(1)
    screenshot = Win32api.screenshot(window)
    detect(screenshot)