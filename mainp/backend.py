import streamlit as st
import cv2
import easyocr
from ultralytics import YOLO
import tempfile
from PIL import Image
import numpy as np
from streamlit.components.v1 import html
from pyfcm import FCMNotification

import firebase_admin
from firebase_admin import credentials, messaging
DEVICE_FCM_TOKEN = "erOLoSW7QTeigNTdkKkJGl:APA91bHR1zRdbpG_2skeA_nNa1Wzg1fxrSzMGPOinZvE8kuyVoGDy7VKMEggeAfyJQtRCzbJth1tvW466KGcYEyBOb9E_Q66KK8ub7q1g8PXRLsDUqtKfyg"

# Initialize the Firebase app
cred = credentials.Certificate('heatsentinel-aa296-firebase-adminsdk-fbsvc-4448a21d9a.json')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def send_push_notification(title: str, body: str, token: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    print(f"Successfully sent message: {response}")



#load model
@st.cache_resource
def load_yolo_model():
    return YOLO(r"runs\detect\train2\weights\best.pt")  
yolo_model = load_yolo_model()
reader = easyocr.Reader(['en'], gpu=True)

st.title("Cattle monitoring backend system dashboard")

#detection part
st.header("1. Cattle detection")
uploaded_file = st.file_uploader("Upload an image for YOLO detection", type=["jpg", "jpeg", "png"], key="yolo")

conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.1, 0.05)

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, 1)

    results = yolo_model.predict(source=img_bgr, conf=conf_threshold, save=False, show=False)
    result_img = results[0].plot()
    result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

    st.image(result_img_rgb, caption="Cattle detections", use_container_width=True)

    # --- New: Show detected classes ---
    detected_classes = []
    for box in results[0].boxes:
        class_index = int(box.cls[0])  # class index
        class_name = results[0].names[class_index]  # map index to name
        
    classnames = ["SITTING", "STANDING", "STANDING"]
    if class_name:
        st.markdown("**Detected cow classes:**")
        st.write(classnames[int(class_name)])
    else:
        st.write("No cows detected.")


#thermal part
st.header("2. Thermal reading")
thermal_file = st.file_uploader(
    "Upload a thermal image", 
    type=["jpg", "jpeg", "png"], 
    key="thermal"
)

if thermal_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(thermal_file.read())
        tmp_path = tmp_file.name

    st.image(tmp_path, caption="Uploaded thermal data", use_container_width=True)

    img = cv2.imread(tmp_path)
    results = reader.readtext(img, detail=0)

    if results:
        try:
            first_value = float(results[0])
        except ValueError:
            first_value = None

        if first_value is not None:
            if first_value < 36:
                st.success(f"Temperature: {first_value}°C — No high temperature detected.")
            else:
                st.error(f"Temperature: {first_value}°C — High temperature detected!")
                send_push_notification(
                    title="High temperature detected",
                    body=f"Temperature: {first_value}°C",
                    token=DEVICE_FCM_TOKEN
                )
                
        else:
            st.warning("Could not parse temperature from the image.")
    else:
        st.warning("No text detected in the image.")
