from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

def process_document(file_path: str):
    # Example: If it's a PDF file, extract text from the pages
    if file_path.endswith('.pdf'):
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        # Check if text is extracted
        # print("Extracted text:", text[:500])  # Print first 500 characters for debugging

        # Process the text (e.g., split it into chunks)
        processed_chunks = text.split('\n')  # This is just a simple example
        return processed_chunks

    # If it's a TXT file, just read the content
    elif file_path.endswith('.txt'):
        with open(file_path, "r") as f:
            text = f.read()

        # Process the text (e.g., split into chunks)
        processed_chunks = text.split('\n')  # This is just a simple example
        return processed_chunks

    return []

