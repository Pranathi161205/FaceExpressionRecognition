import cv2
import numpy as np
from tensorflow.keras.models import load_model
import winsound

# Load trained model
model = load_model("emotion_model.h5")

# Emotion labels
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Color dictionary
color_dict = {
    "angry": (0, 0, 255),
    "happy": (0, 255, 0),
    "sad": (255, 0, 0),
    "surprise": (0, 255, 255),
    "neutral": (255, 255, 255),
    "fear": (255, 0, 255),
    "disgust": (0, 128, 128)
}

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Start webcam
cap = cv2.VideoCapture(0)

last_emotion = None  # To avoid continuous beeping

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face / 255.0
        face = np.reshape(face, (1, 48, 48, 1))

        prediction = model.predict(face, verbose=0)
        confidence = np.max(prediction) * 100
        emotion = emotion_labels[np.argmax(prediction)]

        color = color_dict.get(emotion, (0, 255, 0))
        label = f"{emotion} ({confidence:.2f}%)"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, color, 2)

        # 🔔 Play sound only when emotion changes
        if emotion != last_emotion:
            if emotion == "happy":
                winsound.Beep(1000, 200)
            elif emotion == "sad":
                winsound.Beep(500, 200)
            elif emotion == "angry":
                winsound.Beep(200, 300)
            elif emotion == "surprise":
                winsound.Beep(1500, 200)

            last_emotion = emotion

    cv2.imshow("Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()