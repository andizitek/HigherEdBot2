import os
import fitz  # PyMuPDF

PDF_FOLDER = "pdfs"
OUTPUT_FOLDER = "context"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def batch_extract():
    for filename in os.listdir(PDF_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, filename)
            output_filename = os.path.splitext(filename)[0] + "_context.txt"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            print(f"Extrahiere: {filename}")
            text = extract_text_from_pdf(pdf_path)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"=> gespeichert: {output_filename}")

if __name__ == "__main__":
    batch_extract()
