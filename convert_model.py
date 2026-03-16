# convert_model.py
from tensorflow.keras.models import load_model

model = load_model("emotion_model.h5")   # the original trained model
model.save("emotion_model_tf213.keras")  # save in modern Keras format
print("Converted model saved!")