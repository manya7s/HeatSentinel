from ultralytics import YOLO
import numpy as np

def main():
    # Load trained model
    model = YOLO(r"C:\Users\manya\Desktop\yolo12\mainp\runs\detect\train2\weights\best.pt")

    # Validate on the test split
    results = model.val(
        data="data.yaml",
        split="test",
        imgsz=736,
        batch=16,
        device=0,
        plots=False
    )

    # Precision & Recall
    precision = results.box.mp.item()
    recall = results.box.mr.item()
    f1_score = 2 * (precision * recall) / (precision + recall + 1e-16)

    # mAP
    map50 = results.box.map50.item()
    map5095 = results.box.map.item()

    # Confusion matrix
    cm = results.confusion_matrix.matrix.astype(np.float64)
    tp = np.diag(cm)

    # Instead of cm.sum(), use TP+FN for actual ground truth count
    total_instances = cm.sum(axis=1).sum()  # sum over rows = ground truth per class
    accuracy = tp.sum() / (total_instances + 1e-16)

    # FPR and FNR
    fpr_list, fnr_list = [], []
    for i in range(len(cm)):
        fp = cm[:, i].sum() - tp[i]
        fn = cm[i, :].sum() - tp[i]
        tn = total_instances - (tp[i] + fp + fn)

        fpr = fp / (fp + tn + 1e-16)
        fnr = fn / (fn + tp[i] + 1e-16)

        fpr_list.append(fpr)
        fnr_list.append(fnr)

    macro_fpr = np.mean(fpr_list)
    macro_fnr = np.mean(fnr_list)

    print("\n==== Model Evaluation Metrics ====")
    print(f"Precision (mean):   {precision:.4f}")
    print(f"Recall (mean):      {recall:.4f}")
    print(f"F1-Score (mean):    {f1_score:.4f}")
    print(f"mAP@0.5:            {map50:.4f}")
    print(f"mAP@0.5:0.95:       {map5095:.4f}")
    print(f"Accuracy:           {accuracy:.4f}")
    print(f"False Positive Rate (macro): {macro_fpr:.4f}")
    print(f"False Negative Rate (macro): {macro_fnr:.4f}")
    print("=================================\n")

if __name__ == "__main__":
    main()