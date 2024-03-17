from flask import Flask, request, jsonify, render_template
import PyPDF2
import os
import tempfile
from io import BytesIO
import gemini
import gemini_pb2

app = Flask(__name__)

pdf_text = ""

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/generate-response', methods=['POST'])
# def chat_response():
#     global pdf_text  # Ensure access to the global variable
#     data = request.json
#     prompt = data.get('prompt')
    
#     if pdf_text:
#         prompt += f"\n\nExtracted PDF Text: {pdf_text}"
    
#     try:
#         response_text = gemini.generate_response(prompt)
#         return jsonify({"success": True, "response": response_text})
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/generate-response', methods=['POST'])
def chat_response():
    data = request.json
    prompt = data.get('prompt')

    # Use protobuf internally for processing
    query_request = gemini_pb2.UserQueryRequest()
    query_request.query = prompt
    # If you have context or other fields, set them here as well

    # Process the query using your gemini module
    try:
        response_text = gemini.generate_response(query_request.query)  # Adjust as needed based on your gemini module

        # Use protobuf for the response as well internally if needed
        response_proto = gemini_pb2.GeminiResponse()
        response_proto.success = True
        response_proto.message = response_text

        # Convert the protobuf message to a dictionary and then to JSON for the response
        response_dict = {
            "success": response_proto.success,
            "response": response_proto.message,
            # Include other fields from the response as needed
        }
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)