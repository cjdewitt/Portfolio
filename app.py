from flask import Flask, request, jsonify, render_template
import PyPDF2
import os
import tempfile
from io import BytesIO
import gemini
import gemini_pb2
import PyPDF2
import os
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/SensorLoader')
def sensor_loader():
    return render_template('SensorLoader.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/Research-GPT')
def research_gpt():
    return render_template('ResearchGPT.html')

# Route for generating chat responses
@app.route('/generate-response', methods=['POST'])
def generate_chat_response():
    data = request.json
    prompt = data.get('prompt')
    query_request = gemini_pb2.UserQueryRequest()
    query_request.query = prompt

    try:
        response_text = gemini.generate_response(query_request.query)
        response_proto = gemini_pb2.GeminiResponse()
        response_proto.success = True
        response_proto.message = response_text

        return jsonify({"success": response_proto.success, "response": response_proto.message})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Route for processing and including PDF content in chat responses
@app.route('/generate-response-with-pdf', methods=['POST'])
def generate_response_with_pdf():
    print("*ENTERED PDF CHAT*")
    text = extract_text_from_pdf("templates/SensorLoader.pdf")
    if text:
        print("successfully paresed pdf")
    else:
        print("error parsing pdf!")
    data = request.json
    prompt = data.get('prompt')
    full_prompt = prompt + text if text else prompt

    try:
        response_text = gemini.generate_response("KEEP RESPONSE CONCISE" + full_prompt)
        response_proto = gemini_pb2.GeminiResponse()
        response_proto.success = True
        response_proto.message = response_text
        return jsonify({"success": response_proto.success, "response": response_proto.message})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() if page.extract_text() else ""
        print("Successfully extracted text from PDF.")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
