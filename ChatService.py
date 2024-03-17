import gemini_pb2
import os
from gemini import generate_response, extract_text_from_pdf

def save_pdf(filename, content):
    # Define a directory to save the PDF files, ensure it exists
    save_dir = "uploaded_pdfs"
    os.makedirs(save_dir, exist_ok=True)

    # Construct the full path where the PDF will be saved
    pdf_path = os.path.join(save_dir, filename)

    # Save the PDF content to the file
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(content)

    # Return the path to the saved PDF file
    return pdf_path

class ChatService:

    
    def handle_pdf_upload(self, request_proto):
        # Extract information from the protobuf request
        filename = request_proto.filename
        content = request_proto.content

        # Assume save_pdf function saves the PDF and returns a path
        pdf_path = save_pdf(filename, content)
        
        # Extract text from the PDF
        parsed_text = extract_text_from_pdf(pdf_path)
        
        # Construct the protobuf response
        if parsed_text:
            response_proto = gemini_pb2.PdfUploadResponse(success=True, message="PDF processed successfully.", parsedText=parsed_text)
        else:
            response_proto = gemini_pb2.PdfUploadResponse(success=False, message="Failed to process PDF.")
        
        return response_proto


    def handle_user_query(self, request_proto):
        # Extract information from the protobuf request
        query = request_proto.query
        context = request_proto.context

        # Generate a response from the Gemini model
        response_text = generate_response(query + " " + context)
        
        # Construct the protobuf response
        response_proto = gemini_pb2.GeminiResponse(success=True, message=response_text, promptFeedback="")
        
        return response_proto
