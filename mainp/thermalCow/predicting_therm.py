import os, random
from ultralytics import YOLO

# load your YOLOv12 model
model = YOLO(r"runs\detect\train10\weights\best.pt")
model.to("mps")

# sample 4 images
image_dir = r"datasets\Heat Detection\test\images"
imgs = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg','png','jpeg'))]
for fname in random.sample(imgs, 4):
    path = os.path.join(image_dir, fname)
    results = model(
        path,
        imgsz=1024,      
        conf=0.1,        
        iou=0.3,         
        augment=True    
    )
    if results[0].boxes:
        print(f"{len(results[0].boxes)} objects in {fname}")
        results[0].show()
    else:
        print(f"no detections in {fname}")