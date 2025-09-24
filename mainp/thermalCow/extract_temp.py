import easyocr
import cv2
import math
import re
import torch

# Check GPU
if torch.cuda.is_available():
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    print("GPU not detected. Running on CPU.")

# Load EasyOCR with GPU support
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

# Read image
img_path = input("Enter path of image: ").strip()
img = cv2.imread(img_path)

# OCR with bounding boxes
results = reader.readtext(img)

if not results:
    print("No text detected.")
    exit()

# Find text closest to top-left
closest_text = None
closest_dist = float('inf')

for (bbox, text, conf) in results:
    (x, y) = bbox[0]
    dist = math.sqrt(x**2 + y**2)
    if dist < closest_dist:
        closest_dist = dist
        closest_text = text

print("Raw OCR for top-left text:", closest_text)

# Extract numeric value
match = re.search(r"(\d{2}\.\d)", closest_text)
if match:
    temperature = float(match.group(1))
    print("Detected cow temperature:", temperature, "°C")
else:
    print("Could not parse a valid temperature.")
