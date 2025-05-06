 PDF Parser with OCR and Text Extraction

This project allows you to upload a PDF, extract both text and images from it, and apply OCR (Optical Character Recognition) on the images to extract any text. The extracted text and images are made available for download.

 Features
- Extract text from PDF pages.
- Extract images from PDF pages.
- Perform OCR on images to extract text.
- Download the extracted text and images.
- User-friendly web interface built with Flask.

 Requirements

To run this project, make sure you have the following dependencies installed:

- Python 3.x
- Tesseract OCR (installed and configured correctly)

 Install Dependencies

First, install the required Python libraries by running:

bash
pip install -r requirements.txt


Where requirements.txt contains the following dependencies:


Flask==2.2.2
PyMuPDF==1.21.0
Pillow==9.1.0
pytesseract==0.3.9


 Install Tesseract OCR

1. Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
2. Set the path to the Tesseract executable in the app.py file:

python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


Make sure to replace the path with the correct location of the Tesseract executable on your system.

 How to Run the Project

1. Clone this repository to your local machine:

bash
git clone https://github.com/yourusername/pdf-parser.git
cd pdf-parser


2. Run the Flask application:

bash
python app.py


3. Open your browser and go to http://127.0.0.1:5000/ to access the PDF parser.

 Usage

1. Upload a PDF file via the form on the main page.
2. The server will process the PDF, extracting both text and images.
3. Once processing is complete, you can download:

    A .txt file containing the extracted text.
    The images extracted from the PDF (with download options for each image).
4. If any text is found within the images, OCR will be performed to extract the text.

 Folder Structure

 uploads/: Contains uploaded PDF files.
 static/output/: Stores the extracted text and images.

   text.txt: Contains the extracted text.
   images/: Folder containing the extracted images from the PDF.

 License

This project is open-source and available under the [MIT License](LICENSE).



 Explanation:
- Project Overview: Describes what the project does (extracts text and images from PDFs, applies OCR).
- Requirements: Specifies the Python libraries needed for the project.
- How to Run: Instructions for setting up and running the project locally.
- Usage: Explains how the user can interact with the app.
- Folder Structure: Describes the project's directory structure.
- License: A mention of the open-source license (feel free to adjust based on your choice of license).


