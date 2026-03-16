from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
from tensorflow.keras.models import load_model

import os
app = Flask(__name__)
CORS(app)

# Load trained model


model = load_model("emotion_model.h5")
emotion_labels = ['angry','disgust','fear','happy','neutral','sad','surprise']

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

@app.route("/")
def home():
    return "Emotion Detection API Running"

@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.json

        if not data or "image" not in data:
            return jsonify({"emotion": "No Image Received", "confidence": 0})

        image_data = data["image"]

        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(",")[1])
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Fix mirror webcam issue
        img = cv2.flip(img, 1)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Improve contrast
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30,30)
        )

        if len(faces) == 0:
            return jsonify({"emotion": "No Face Detected", "confidence": 0})

        # Use first detected face
        (x, y, w, h) = faces[0]

        # Expand face region slightly
        y1 = max(0, y-10)
        y2 = y+h+10
        x1 = max(0, x-10)
        x2 = x+w+10

        face = gray[y1:y2, x1:x2]

        # Resize to model input size
        face = cv2.resize(face, (48,48))

        # Normalize
        face = face / 255.0
        face = np.reshape(face, (1,48,48,1))

        # Predict emotion
        prediction = model.predict(face, verbose=0)

        emotion_index = np.argmax(prediction)
        emotion = emotion_labels[emotion_index]

        confidence = float(np.max(prediction) * 100)

        if confidence < 45:
            emotion = "Uncertain"

        return jsonify({
            "emotion": emotion,
            "confidence": round(confidence,2)
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"emotion": "Processing Error", "confidence": 0})




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)