import cv2

from ultralytics import YOLO


model = YOLO("C:/Users/kaosh/OneDrive/桌面/Genshin-Impact-Auto/assets/yolo model/best.pt")
#model.train(
#        data="C:/Users/kaosh/Downloads/fish.v7i.yolov11/data.yaml",
#        mode="detect",
#        epochs=25,
#        imgsz=640,
#        device="cpu"
#    )


def detect(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    result = model.predict(source=image, show=True, save=True)
    
    #print(result)
    #for r in result:
    #    print(r.boxes.data)
    
    
detect("C:/Users/kaosh/OneDrive/桌面/新增資料夾/20241006234840.png")