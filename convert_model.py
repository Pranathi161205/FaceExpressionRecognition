from tensorflow.keras.models import load_model

# Load original TF 2.20 model
model = load_model("emotion_model.h5")

# Save in TF 2.13 compatible format
model.save("emotion_model_tf213.h5")
print("Model converted to TF 2.13 successfully!")