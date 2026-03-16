# convert_model.py
from tensorflow.keras.models import load_model

# Load your original model (trained with TF 2.20)
model = load_model("emotion_model.h5")

# Resave it in TF 2.13 compatible format
model.save("emotion_model_tf213.h5")

print("Model converted successfully!")