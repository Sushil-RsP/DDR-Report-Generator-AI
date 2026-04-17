import fitz  # PyMuPDF
import os
from pathlib import Path


def extract_text(pdf_input):
    try:
        # Handle both file paths and Streamlit uploaded files
        if isinstance(pdf_input, str):
            doc = fitz.open(pdf_input)
        else:
            # For Streamlit UploadedFile
            pdf_bytes = pdf_input.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text = ""
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            text += page_text + "\n"
        
        return text
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_images(pdf_input, output_folder="images"):
    try:
        os.makedirs(output_folder, exist_ok=True)
        
        # Handle both file paths and Streamlit uploaded files
        if isinstance(pdf_input, str):
            doc = fitz.open(pdf_input)
        else:
            # For Streamlit UploadedFile
            pdf_bytes = pdf_input.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        image_paths = []
        
        for page_index in range(len(doc)):
            page = doc[page_index]
            images = page.get_images(full=True)
            
            for img_index, img in enumerate(images):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    image_ext = base_image["ext"]
                    image_name = f"page{page_index+1}_img{img_index}.{image_ext}"
                    image_path = os.path.join(output_folder, image_name)
                    
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                    
                    image_paths.append(image_path)
                
                except Exception as e:
                    print(f"Warning: Could not extract image from page {page_index+1}: {str(e)}")
                    continue
        
        return image_paths
    
    except Exception as e:
        raise Exception(f"Error extracting images from PDF: {str(e)}")


def combine_texts(text1, text2, separator="\n\n" + "="*80 + "\n\n"):
    return f"{text1}{separator}{text2}"


def clean_text(text):
    # Remove excessive newlines
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(cleaned_lines)
