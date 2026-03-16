import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image

# Load model

model.save("emotion_model_tf213.h5")
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

st.title("AI Facial Emotion Detection")

uploaded_file = st.file_uploader("Upload an image", type=["jpg","png","jpeg"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face = cv2.resize(gray, (48,48))
    face = face/255.0
    face = face.reshape(1,48,48,1)

    prediction = model.predict(face)
    emotion = emotion_labels[np.argmax(prediction)]

    st.subheader(f"Detected Emotion: {emotion}")