import streamlit as st
from ultralytics import YOLO
import numpy as np
import cv2

st.title("Cow Behaviour Detection")

@st.cache_resource
def load_model():
    return YOLO(r"runs\detect\train10\weights\best.pt")

model = load_model()

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.1, 0.05)

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, 1)

    results = model.predict(source=img_bgr, conf=conf_threshold, save=False, show=False)

    result_img = results[0].plot()
    result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

    st.image(result_img_rgb, caption="YOLO Detections", use_container_width=True)
