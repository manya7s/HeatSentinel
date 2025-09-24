from ultralytics import YOLO

def main():
    model = YOLO("yolo12n.pt") 
    model.train(
        data="data.yaml",
        epochs=30,
        imgsz=720,
        batch=16,
        workers=4,
        device=0,      #CUDA use
        patience=10    #stop train whn no change
    )

if __name__ == "__main__":
    main()
