import time

from ultralytics import YOLO


model = YOLO("C:/Users/kaosh/OneDrive/桌面/GENSHIN-IMPACT-AUTO/assets/yolo model/best.pt")

result = model.track(
    source="C:/Users/kaosh/OneDrive/桌面/GENSHIN-IMPACT-AUTO/test3.mp4",
    conf=0.85,
    vid_stride=3,
    persist=True,
    save=True
)