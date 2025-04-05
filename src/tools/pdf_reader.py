"""
Tool: PDF Reader
Extracts and returns raw text from a PDF file using PyMuPDF.
"""

import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"[PDF Reader Error] {e}"
