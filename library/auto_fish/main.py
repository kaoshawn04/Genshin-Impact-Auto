from ultralytics import YOLO
import cv2
import numpy as np

def get_detection_coordinates(model_path, image_path):
    # Load the YOLOv8 model
    model = YOLO(model_path)
    
    # Load and process the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    
    # Run inference
    results = model(image)[0]
    
    # List to store detection information
    detections = []
    
    # Process each detection
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, confidence, class_id = result
        
        # Convert coordinates to integers
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        
        # Calculate center point and dimensions
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        box_width = x2 - x1
        box_height = y2 - y1
        
        # Get class name
        class_name = results.names[int(class_id)]
        
        detection = {
            'class': class_name,
            'confidence': round(confidence, 2),
            'bbox': {
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'center': (center_x, center_y),
                'width': box_width,
                'height': box_height
            }
        }
        detections.append(detection)
    
    return detections

# Example usage
if __name__ == "__main__":
    model_path = "yolov8n.pt"  # or path to your custom model
    image_path = "image.jpg"   # path to your image
    
    detections = get_detection_coordinates(model_path, image_path)
    
    # Print detection information
    for i, detection in enumerate(detections, 1):
        print(f"\nDetection {i}:")
        print(f"Class: {detection['class']}")
        print(f"Confidence: {detection['confidence']}")
        print("Bounding Box:")
        print(f"  Top-left corner: ({detection['bbox']['x1']}, {detection['bbox']['y1']})")
        print(f"  Bottom-right corner: ({detection['bbox']['x2']}, {detection['bbox']['y2']})")
        print(f"  Center point: {detection['bbox']['center']}")
        print(f"  Width: {detection['bbox']['width']}")
        print(f"  Height: {detection['bbox']['height']}")