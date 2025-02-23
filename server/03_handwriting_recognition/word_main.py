# Works perfectly fine

# import os
# import cv2
# import numpy as np
# from mltu.configs import BaseModelConfigs
# from inferenceModel import ImageToWordModel

# # Get the absolute path of the script
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Load configurations
# config_path = os.path.normpath(os.path.join(BASE_DIR, "..", "Models", "03_handwriting_recognition", "1", "configs.yaml"))
# print(f"Loading config from: {config_path}")

# if not os.path.exists(config_path):
#     raise FileNotFoundError(f"Config file not found at: {config_path}")

# configs = BaseModelConfigs.load(config_path)

# # Resolve model path
# model_path = os.path.normpath(os.path.join(BASE_DIR, "..", configs.model_path))
# print(f"Resolved model path: {model_path}")

# if not os.path.exists(model_path):
#     raise FileNotFoundError(f"Model path does not exist: {model_path}")

# # Load the model
# model = ImageToWordModel(model_path=model_path, char_list=configs.vocab)

# def extract_text_from_image(word_image_path):
#     """Extracts text from a given handwritten word image."""
    
#     # Load the image
#     image = cv2.imread(word_image_path)

#     if image is None:
#         print(f"Error: Could not load image from {word_image_path}")
#         return None

#     prediction_text = model.predict(image)
#     return prediction_text

# # Load your test image
# image_path = os.path.normpath("server/data/words/a01-003-00-02.png")  # Update if needed

# if __name__ == "__main__":
#     print(f"Current working directory: {os.getcwd()}")

#     if not os.path.exists(image_path):
#         print(f"Error: Test image not found at {image_path}")
#     else:
#         extracted_text = extract_text_from_image(image_path)
#         print(f"Prediction: {extracted_text}")

#         # Display the image
#         image = cv2.imread(image_path)
#         image = cv2.resize(image, (image.shape[1] * 4, image.shape[0] * 4))
#         cv2.imshow("Test Image", image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

import os
import sys
import cv2
import numpy as np
from mltu.configs import BaseModelConfigs

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add 03_handwriting_recognition to Python's module search path
HANDWRITING_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "03_handwriting_recognition"))
if HANDWRITING_DIR not in sys.path:
    sys.path.append(HANDWRITING_DIR)

# Now import inferenceModel
from inferenceModel import ImageToWordModel  

# Load configurations
config_path = os.path.normpath(os.path.join(BASE_DIR, "..", "Models", "03_handwriting_recognition", "1", "configs.yaml"))
print(f"Loading config from: {config_path}")

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file not found at: {config_path}")

configs = BaseModelConfigs.load(config_path)

# Resolve model path
model_path = os.path.normpath(os.path.join(BASE_DIR, "..", configs.model_path))
print(f"Resolved model path: {model_path}")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model path does not exist: {model_path}")

# Load the model
model = ImageToWordModel(model_path=model_path, char_list=configs.vocab)

def extract_text_from_image(word_image_path):
    """Extracts text from a given handwritten word image."""
    
    # Load the image
    image = cv2.imread(word_image_path)

    if image is None:
        print(f"Error: Could not load image from {word_image_path}")
        return None

    prediction_text = model.predict(image)
    return prediction_text



