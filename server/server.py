from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
from io import BytesIO
from reportlab.pdfgen import canvas
from fpdf import FPDF
import textwrap
from weasyprint import HTML

# Add the path of "word-detector-main" to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_DETECTOR_PATH = os.path.join(BASE_DIR, "word-detector-main")

if WORD_DETECTOR_PATH not in sys.path:
    sys.path.insert(0, WORD_DETECTOR_PATH)  # Insert at position 0 for priority

# Import process_images from main.py after modifying sys.path
try:
    from main import process_images
except ModuleNotFoundError as e:
    print(f"Error importing main.py: {e}")
    process_images = None  # Handle case where import fails

app = Flask(__name__)
CORS(app)  # Enable CORS to avoid frontend issues

UPLOAD_FOLDER = "data/page"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# def generate_pdf(text):
#     pdf = FPDF()
#     pdf.add_page()

#     # Ensure the font file is present
#     font_path = "NotoSans-Regular.ttf"
#     if not os.path.exists(font_path):
#         raise FileNotFoundError(f"Font file '{font_path}' not found. Please place it in the project directory.")

#     # Add Unicode Font (Noto Sans)
#     pdf.add_font("NotoSans", "", font_path, uni=True)
#     pdf.set_font("NotoSans", "", 12)

#     # Fix: Properly handling text to avoid vertical misalignment
#     pdf.set_auto_page_break(auto=True, margin=15)  # Enable auto page breaks

#     # Fix: Use cell() instead of multi_cell() to prevent vertical printing
#     lines = text.split("\n")  # Ensure proper line breaks
#     for line in lines:
#         pdf.cell(0, 10, line, ln=True)  # Print each line properly

#     # Save PDF
#     pdf_path = "translated_text.pdf"
#     pdf.output(pdf_path, "F")  # "F" ensures it writes to a file

#     return pdf_path

FONT_MAP = {
    "english": "Noto Sans",
    "hindi": "Noto Sans Devanagari",
    "tamil": "Noto Sans Tamil",
    "malayalam": "Noto Sans Malayalam",
    "kannada": "Noto Sans Kannada",
}

def generate_pdf(text, language="english", output_file="translated_text.pdf"):
    """
    Generates a PDF with the given text, supporting multiple languages.
    The PDF is saved to disk and the file path is returned.

    Args:
        text (str): The content to be included in the PDF.
        language (str): The language of the text (default: "english").
        output_file (str): The filename for the saved PDF (default: "translated_text.pdf").

    Returns:
        str: The path of the saved PDF file.
    """
    # ✅ Get the correct font for the selected language
    font_family = FONT_MAP.get(language.lower(), "Noto Sans")

    # ✅ Replace newline characters `\n` with `<br>` for HTML formatting
    text_html = text.replace("\n", "<br>")

    # ✅ Use a regular string (not an f-string)
    html_content = """\
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=""" + font_family.replace(" ", "+") + """&display=swap');
                body {
                    font-family: '""" + font_family + """', sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                }
            </style>
        </head>
        <body>
            <p>""" + text_html + """</p>
        </body>
    </html>
    """

    # ✅ Convert HTML to PDF and Save
    HTML(string=html_content).write_pdf(output_file)

    print(f"✅ PDF saved successfully as: {output_file}")

    # ✅ Return the saved PDF file path
    return os.path.abspath(output_file)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    if process_images is None:
        return jsonify({"error": "Internal server error: main.py not found"}), 500

    file = request.files['file']
    language = request.form.get('language', 'english')

    # Ensure the upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)  # Save file inside data/page/

    try:
        # Call main function to process the image and get translated text
        translated_text = process_images(language)

        # Remove the uploaded image file after processing
        os.remove(file_path)

        # Generate PDF in memory
        pdf_buffer = generate_pdf(translated_text)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name="translated_text.pdf"
        )

    except Exception as e:
        # Ensure file is deleted even if an error occurs
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
