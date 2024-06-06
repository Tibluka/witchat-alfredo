import os
from flask import Flask, request, jsonify
import fitz
from docx import Document
from flask_cors import CORS
from services import messages
import openpyxl
from PIL import Image
import pytesseract

app = Flask(__name__)
CORS(app, resources={
     r"/extract-text": {"origins": "https://pocfilerecognition.netlify.app"}})
CORS(app, resources={
     r"/send-message": {"origins": "https://pocfilerecognition.netlify.app"}})

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_word(file_path)
    elif ext == '.xlsx':
        return extract_text_from_excel(file_path)
    elif ext in ['.png', '.jpeg', '.jpg']:
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Formato de arquivo não suportado. Use PDF ou DOCX.")

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def extract_text_from_word(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    text = ""
    for sheet in workbook.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value:
                    text += str(cell.value) + " "
            text += "\n"
    return text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    try:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        text = extract_text_from_file(file_path)
        os.remove(file_path)  # Remove the file after processing
        return jsonify({'text': 'Esse é o conteúdo de texto do arquivo que eu quero que você analise: ' + text}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send-message', methods = ['POST'])
def send():
    try:
        API_KEY = request.headers["Authorization"]
        message = request.json
        chatGptResponse = messages.sendMessage(message, API_KEY)
        res = {}
        res['message'] = chatGptResponse
        return res, 200
    except:
        e = {}
        e['error'] = e['message']
        return e, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)