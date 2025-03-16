# working code below

# import argparse
# from typing import List
# import cv2
# import matplotlib.pyplot as plt
# from pathlib import Path
# import numpy as np
# import matplotlib
# import sys
# import os
# import importlib.util

# from translator import translate_text

# # Dynamically import extract_text_from_image from word_main.py
# BASE_DIR = Path(__file__).resolve().parent
# HANDWRITING_RECOGNITION_PATH = BASE_DIR / "../03_handwriting_recognition/word_main.py"

# spec = importlib.util.spec_from_file_location("word_main", str(HANDWRITING_RECOGNITION_PATH))
# word_main = importlib.util.module_from_spec(spec)
# sys.modules["word_main"] = word_main
# spec.loader.exec_module(word_main)
# extract_text_from_image = word_main.extract_text_from_image  # Import function

# from word_detector import detect, prepare_img, sort_multiline

# def get_img_files(data_dir: Path) -> List[Path]:
#     """Return all image files contained in a folder."""
#     res = []
#     for ext in ['*.png', '*.jpg', '*.bmp']:
#         res += list(data_dir.glob(ext))
#     return res

# def main():
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     DATA_PATH = BASE_DIR / "data" / "page"

#     parser = argparse.ArgumentParser()
#     parser.add_argument('--data', type=Path, default=DATA_PATH)
#     parser.add_argument('--kernel_size', type=int, default=25)
#     parser.add_argument('--sigma', type=float, default=11)
#     parser.add_argument('--theta', type=float, default=5)
#     parser.add_argument('--min_area', type=int, default=100)
#     parser.add_argument('--img_height', type=int, default=1000)
#     parsed = parser.parse_args()

#     print(f"Resolved data path: {parsed.data.resolve()}")

#     if not parsed.data.exists():
#         print(f"Error: Directory {parsed.data} does not exist.")
#         exit(1)

#     for fn_img in get_img_files(parsed.data):
#         print(f'Processing file {fn_img}')
        
#         # Load and preprocess the image
#         img = prepare_img(cv2.imread(str(fn_img)), parsed.img_height)
#         detections = detect(img, 
#                             kernel_size=parsed.kernel_size, 
#                             sigma=parsed.sigma, 
#                             theta=parsed.theta, 
#                             min_area=parsed.min_area)

#         # Sort detections into lines
#         lines = sort_multiline(detections)
#         extracted_text = []  # Store extracted words

#         for line_idx, line in enumerate(lines):
#             for word_idx, det in enumerate(line):
#                 # Extract word region from the image
#                 x, y, w, h = det.bbox.x, det.bbox.y, det.bbox.w, det.bbox.h
#                 word_img = img[y:y+h, x:x+w]  # Cropping the word
                
#                 # Convert the word image to temporary file
#                 temp_path = "temp_word.png"
#                 cv2.imwrite(temp_path, word_img)  # Save temporary file
                
#                 # Pass the word image to OCR model
#                 text = extract_text_from_image(temp_path)
#                 extracted_text.append(text)
#                 os.remove(temp_path)  # Remove the temporary file
        
#         # Print the full extracted text
#         print("Extracted Text:", " ".join(extracted_text))

#         #translating
#         translated = ""
#         lang = "hi"
#         for word in extracted_text:
#             translated_word = translate_text(word, lang)  # Translate word
            
#             if translated_word is None:  
#                 translated_word = "[ERROR]"  # Handle failure gracefully

#             translated += translated_word + " "  # Append translated word with space

#         print("Translated Text:", translated.strip())

    
# if __name__ == '__main__':
#     main()

# Checking code below

import argparse
from typing import List
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import matplotlib
import sys
import os
import importlib.util

from translator import translate_text

# Dynamically import extract_text_from_image from word_main.py
BASE_DIR = Path(__file__).resolve().parent
HANDWRITING_RECOGNITION_PATH = BASE_DIR / "../03_handwriting_recognition/word_main.py"

spec = importlib.util.spec_from_file_location("word_main", str(HANDWRITING_RECOGNITION_PATH))
word_main = importlib.util.module_from_spec(spec)
sys.modules["word_main"] = word_main
spec.loader.exec_module(word_main)
extract_text_from_image = word_main.extract_text_from_image  # Import function

from word_detector import detect, prepare_img, sort_multiline

def get_img_files(data_dir: Path) -> List[Path]:
    """Return all image files contained in a folder."""
    res = []
    for ext in ['*.png', '*.jpg', '*.bmp']:
        res += list(data_dir.glob(ext))
    return res

def process_images(language: str) -> str:
    """Processes images from the specified directory and returns the translated text."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "data" / "page"
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=DATA_PATH)
    parser.add_argument('--kernel_size', type=int, default=25)
    parser.add_argument('--sigma', type=float, default=11)
    parser.add_argument('--theta', type=float, default=5)
    parser.add_argument('--min_area', type=int, default=100)
    parser.add_argument('--img_height', type=int, default=1000)
    parsed, _ = parser.parse_known_args()
    
    print(f"Resolved data path: {parsed.data.resolve()}")
    
    if not parsed.data.exists():
        print(f"Error: Directory {parsed.data} does not exist.")
        return ""
    
    extracted_text = []
    for fn_img in get_img_files(parsed.data):
        print(f'Processing file {fn_img}')
        
        # Load and preprocess the image
        img = prepare_img(cv2.imread(str(fn_img)), parsed.img_height)
        detections = detect(img, 
                            kernel_size=parsed.kernel_size, 
                            sigma=parsed.sigma, 
                            theta=parsed.theta, 
                            min_area=parsed.min_area)

        # Sort detections into lines
        lines = sort_multiline(detections)
        
        for line_idx, line in enumerate(lines):
            for word_idx, det in enumerate(line):
                # Extract word region from the image
                x, y, w, h = det.bbox.x, det.bbox.y, det.bbox.w, det.bbox.h
                word_img = img[y:y+h, x:x+w]  # Cropping the word
                
                # Convert the word image to temporary file
                temp_path = "temp_word.png"
                cv2.imwrite(temp_path, word_img)  # Save temporary file
                
                # Pass the word image to OCR model
                text = extract_text_from_image(temp_path)
                extracted_text.append(text)
                os.remove(temp_path)  # Remove the temporary file
        
    # Print the full extracted text
    print("Extracted Text:", " ".join(extracted_text))

    # Translating
    translated = ""
    for word in extracted_text:
        translated_word = translate_text(word, language)  # Translate word
        
        if translated_word is None:  
            translated_word = ""  # Handle failure gracefully

        translated += translated_word + " "  # Append translated word with space

    print("Translated Text:", translated.strip())
    return translated.strip()




