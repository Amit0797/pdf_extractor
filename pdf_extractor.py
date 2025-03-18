import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')


def process_directory(prompt_path, pdf_files):
    
    try:
        # Load the prompt from the text file
        with open(prompt_path, 'r') as f:
            prompt_text = f.read()
             # Debugging

        # Upload PDF files and create a list of file parts for the Gemini API
        file_parts = []
        for file_path in pdf_files:
            try:
                sample_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path))  # Use filename as display name
                file_parts.append(sample_file)
               
            except FileNotFoundError as e:
                print(f"Error: File not found: {file_path} - {e}")
                return None  # Or handle the error as appropriate
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")
                return None

        # Add the prompt to the content parts
        content = file_parts + [prompt_text]  # Combine files and prompt
        print(f"Content: {content}")  # Inspect the content

        # Generate content using the Gemini model
        try:
            response = model.generate_content(content)
            print(f"Raw Response: {response}")
            print(response.candidates[0].content.parts[0].text)  # Print the text response.  Accessing the text is important.
            return response.candidates[0].content.parts[0].text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None


    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Handle any other errors

