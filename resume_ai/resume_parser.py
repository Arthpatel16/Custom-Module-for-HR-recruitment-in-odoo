from PIL import Image
import pytesseract
import fitz 
import io

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            full_text += text + "\n"
        else:
            
            print(f"⚠️ OCR fallback on page {page_num}")
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            full_text += ocr_text + "\n"

    return full_text.strip()
