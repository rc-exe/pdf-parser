import os
from flask import Flask, request, render_template, send_from_directory
import fitz  # PyMuPDF
import shutil
from PIL import Image
import pytesseract
# Add this line to specify the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        if pdf_file and pdf_file.filename.endswith('.pdf'):
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
            pdf_file.save(pdf_path)

            # Clear previous output folder content
            if os.path.exists(OUTPUT_FOLDER):
                shutil.rmtree(OUTPUT_FOLDER)  # delete entire output folder
            os.makedirs(OUTPUT_FOLDER, exist_ok=True)
            image_dir = os.path.join(OUTPUT_FOLDER, "images")
            os.makedirs(image_dir, exist_ok=True)

            # Extract text and images
            pdf = fitz.open(pdf_path)
            full_text = ""
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
                    try:
                        ocr_text = pytesseract.image_to_string(Image.open(image_path))
                        full_text += f"--- OCR from {image_filename} ---\n{ocr_text}\n\n"
                    except Exception as e:
                        full_text += f"[Error performing OCR on {image_filename}: {str(e)}]\n"

            # Save the extracted text to a text file
            text_path = os.path.join(OUTPUT_FOLDER, "text.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            # List images for the HTML template
            images = os.listdir(image_dir)

            return render_template("index.html", success=True, images=images)

    return render_template("index.html", success=False)


@app.route('/output/<path:filename>')
def download_file(filename):
    # Serve text.txt and any other files in the output directory
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


@app.route('/output/images/<path:filename>')
def get_image(filename):
    # Serve image files from the images folder
    return send_from_directory(os.path.join(OUTPUT_FOLDER, "images"), filename)


if __name__ == '__main__':
    app.run(debug=True)
