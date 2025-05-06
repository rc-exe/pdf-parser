from flask import Flask, request, render_template, send_from_directory
import pymupdf as fitz  # Updated import
from PIL import Image
import shutil
import os
import subprocess  # For alternative OCR

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def perform_ocr(image_path):
    """Handle OCR using either pytesseract or direct tesseract command"""
    try:
        # Try pytesseract first
        import pytesseract
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        try:
            # Fallback to direct tesseract command
            result = subprocess.run(['tesseract', image_path, 'stdout'], 
                                  capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"[OCR Error: {str(e)}]"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(pdf_path)

            # Clear previous output folder content
            if os.path.exists(OUTPUT_FOLDER):
                shutil.rmtree(OUTPUT_FOLDER)
            os.makedirs(OUTPUT_FOLDER, exist_ok=True)
            image_dir = os.path.join(OUTPUT_FOLDER, "images")
            os.makedirs(image_dir, exist_ok=True)

            # Extract text and images
            full_text = ""
            try:
                with fitz.open(pdf_path) as pdf:
                    for page_number in range(len(pdf)):
                        page = pdf[page_number]
                        full_text += f"--- Page {page_number + 1} ---\n"
                        full_text += page.get_text()
                        full_text += "\n\n"
                        
                        images = page.get_images(full=True)
                        for img_index, img in enumerate(images):
                            xref = img[0]
                            base_image = pdf.extract_image(xref)
                            image_bytes = base_image["image"]
                            ext = base_image["ext"]
                            image_filename = f"image_{page_number+1}_{img_index+1}.{ext}"
                            image_path = os.path.join(image_dir, image_filename)
                            
                            with open(image_path, "wb") as img_file:
                                img_file.write(image_bytes)

                            # OCR on image
                            ocr_text = perform_ocr(image_path)
                            full_text += f"--- OCR from {image_filename} ---\n{ocr_text}\n\n"

                # Save the extracted text
                text_path = os.path.join(OUTPUT_FOLDER, "text.txt")
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(full_text)

                # List images for the template
                images = os.listdir(image_dir)
                return render_template("index.html", success=True, images=images)

            except Exception as e:
                return render_template("index.html", error=str(e))

    return render_template("index.html", success=False)

@app.route('/output/<path:filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

@app.route('/output/images/<path:filename>')
def get_image(filename):
    return send_from_directory(os.path.join(OUTPUT_FOLDER, "images"), filename)

if __name__ == '__main__':
    app.run(debug=True)