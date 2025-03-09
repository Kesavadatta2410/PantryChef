import tensorflow as tf
import numpy as np
import json
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model("food_classifier.h5")


# Load class labels
with open("class_labels.json", "r") as f:
    class_labels = json.load(f)
    
print("Loaded class labels:", class_labels)
print("Number of classes:", len(class_labels)) 


# Reverse the dictionary to get {index: class_name}
index_to_class = {v: k for k, v in class_labels.items()}

def predict_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)
        confidence = np.max(predictions)

        predicted_label = index_to_class.get(predicted_class, "Unknown")

        return predicted_label, confidence
    except Exception as e:
        return f"Error: {e}", 0.0


# Example usage
img_path = "C:/Users/datta/OneDrive/Documents/pics/test/turnip/Image_9.jpg"
label, conf = predict_image(img_path)
print(f"Predicted Class: {label}, Confidence: {conf:.2f}")
