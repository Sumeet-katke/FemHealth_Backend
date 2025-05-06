# import numpy as np
# import pickle
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array

# class PCOSDetector:
#     def __init__(self, model_path="pcos_detection_model.h5"):
#         self.model = load_model(model_path)

#     def preprocess_image(self, image_path):
#         """
#         Preprocess image for prediction.
#         Input: image_path (str) - path to an ultrasound image
#         Output: numpy array shaped for model
#         """
#         img = load_img(image_path, target_size=(224, 224))
#         img_array = img_to_array(img) / 255.0
#         return np.expand_dims(img_array, axis=0)

#     def predict(self, image_array):
#         """
#         Predicts PCOS from preprocessed image array.
#         Input: numpy array (1, 224, 224, 3)
#         Output: dict with raw score and label
#         """
#         score = float(self.model.predict(image_array)[0][0])
#         label = "PCOS Detected" if score < 0.5 else "PCOS Not Detected"
#         return {
#             "score": round(score, 4),
#             "label": label
#         }

# # Only run this when you want to create the .pkl file
# if __name__ == "__main__":
#     # Initialize detector and save as pickle
#     detector = PCOSDetector()
#     with open("pcos_detector.pkl", "wb") as f:
#         pickle.dump(detector, f)
#     print("✅ Model wrapped and saved as pcos_detector.pkl")

# femhealth/backend/pcosdetector_model_wrapper.py

import numpy as np
from PIL import Image
import onnxruntime as ort

class PCOSDetector:
    def __init__(self, model_path):
        self.session    = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name

    def preprocess_image(self, image_path):
        img = Image.open(image_path).convert("RGB").resize((224,224))
        arr= np.array(img, dtype=np.float32)/255.0
        return arr[np.newaxis, ...]

    def predict(self, image_array):
        pred  = self.session.run(None, {self.input_name: image_array})[0]
        score = float(pred[0][0])
        label = "PCOS Detected" if score < 0.5 else "PCOS Not Detected"
        return {"score": round(score,4), "label": label}