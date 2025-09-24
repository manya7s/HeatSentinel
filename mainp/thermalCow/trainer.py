from ultralytics import YOLO

def main():
    model = YOLO("yolo12n.pt") 
    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=1024,
        batch=16,
        workers=4,
        device=0  # CUDA
    )

if __name__ == "__main__":
    main()


