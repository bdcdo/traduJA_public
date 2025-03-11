from mistralai import Mistral
import os
from typing import List
from streamlit_app.config import get_mistral_api_key

def process_pdf_ocr(pdf_path: str) -> List[str]:
    """
    Process a PDF file using Mistral's OCR service.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        
    Returns:
        List[str]: List of extracted text in markdown format, one item per page
    """
    # Initialize Mistral client
    try:
        api_key = get_mistral_api_key()
        client = Mistral(api_key=api_key)
    except ValueError as e:
        raise ValueError(f"Erro ao inicializar cliente Mistral: {str(e)}")

    # Upload the PDF file
    with open(pdf_path, "rb") as pdf_file:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": os.path.basename(pdf_path),
                "content": pdf_file,
            },
            purpose="ocr"
        )

    # Get signed URL for the uploaded file
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

    # Process the document with OCR
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )

    # Extract text from all pages
    extracted_pages = []
    for page in ocr_response.pages:
        extracted_pages.append(page.markdown)

    return extracted_pages

def save_to_markdown(text: str, output_path: str) -> None:
    """
    Save text content to a markdown file.
    
    Args:
        text (str): Text content to save
        output_path (str): Path where to save the markdown file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def process_single_pdf(pdf_path: str, output_path: str) -> None:
    """
    Process a single PDF file and save the OCR results as markdown.
    
    Args:
        pdf_path (str): Path to the PDF file to process
        output_path (str): Path where to save the markdown file
    """
    try:
        print(f"Processing: {os.path.basename(pdf_path)}")
        
        # Process PDF
        extracted_pages = process_pdf_ocr(pdf_path)
        
        # Combine all pages into a single string with page separators
        full_text = ""
        for i, page_text in enumerate(extracted_pages):
            if i > 0:
                full_text += "\n\n---\n\n"  # Add page separator in markdown format
            full_text += page_text
        
        # Save to markdown file
        save_to_markdown(full_text, output_path)
        print(f"Saved: {os.path.basename(output_path)}")
        
    except Exception as e:
        print(f"Error processing {os.path.basename(pdf_path)}: {str(e)}")

if __name__ == "__main__":
    # Specify the PDF file to process
    pdf_path = "C:/Users/bruno/OneDrive/Git/all-oab-exams/exams/pdf/example.pdf"
    
    # Specify the output markdown file
    output_path = "C:/Users/bruno/OneDrive/Git/all-oab-exams/exams/md/example_ocr.md"
    
    print("Starting OCR processing...")
    process_single_pdf(pdf_path, output_path)
    print("\nOCR processing completed!")
