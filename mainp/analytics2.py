from ultralytics import YOLO
import numpy as np

def evaluate_model():
    model = YOLO(r"C:\Users\manya\Desktop\yolo12\mainp\runs\detect\train2\weights\best.pt")

    results = model.val(
        data="data.yaml",
        split="test",
        imgsz=720,
        save_json=True,
        device=0
    )

    # Raw confusion matrix counts (not normalized!)
    cm = results.confusion_matrix.matrix.astype(int)  # <-- force counts not fractions
    tp = np.diag(cm)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp
    tn = cm.sum() - (tp + fp + fn)

    # Overall metrics
    precision = tp.sum() / (tp.sum() + fp.sum() + 1e-9)
    recall = tp.sum() / (tp.sum() + fn.sum() + 1e-9)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-9)
    accuracy = (tp.sum() + tn.sum()) / cm.sum()

    fpr = fp.sum() / (fp.sum() + tn.sum() + 1e-9)
    fnr = fn.sum() / (fn.sum() + tp.sum() + 1e-9)

    print("\n==== Model Evaluation Metrics ====")
    print(f"Precision:           {precision:.4f}")
    print(f"Recall:              {recall:.4f}")
    print(f"F1-Score:            {f1:.4f}")
    print(f"mAP@0.5:             {results.box.map50:.4f}")
    print(f"mAP@0.5:0.95:        {results.box.map:.4f}")
    print(f"Accuracy:            {accuracy:.4f}")
    print(f"False Positive Rate: {fpr:.4f}")
    print(f"False Negative Rate: {fnr:.4f}")
    print("=================================\n")

if __name__ == "__main__":
    evaluate_model()
