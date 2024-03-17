import PyPDF2
import os
import google.generativeai as genai


def configure_api():
    # Fetch the API key from environment variables
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # Configure the Gemini API with the obtained API key
    genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_from_pdf(pdf_path):
  with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()
  return text


def list_models():
    # List available models and print their names if they support generateContent method
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


def generate_response(prompt):
    # Initialize the generative model with 'gemini-pro' for text-only prompts
    model = genai.GenerativeModel('gemini-pro')

    # Generate content based on the provided prompt
    response = model.generate_content(prompt)

    # Check if there's any prompt feedback indicating safety concerns
    if response.prompt_feedback:
        print("Prompt feedback:", response.prompt_feedback)

    # Return the generated text
    return response.text

configure_api()


# def main():

#     configure_api()
    

#     text = extract_text_from_pdf("cory.pdf")

#     if text:
#         print("successfully paresed pdf")
#     else:
#         print("error parsing pdf!")

#     query = input("Enter your search query: ")

#     while query.lower() != "exit":
#         response_text = generate_response(query+text)
#         if response_text:
#             print(response_text)
#         else:
#             print("Error occurred during API call.")
        
#         query = input("Enter your search query: ")


# if __name__ == "__main__":
#     main()








