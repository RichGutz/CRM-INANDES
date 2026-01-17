
import os
import pdfplumber
import docx2txt

def extract_fields_from_docs():
    folder = 'DB_PARTICIPES_DESIGN'
    
    print(f"📂 Analizando dcoumentos en: {folder}")
    
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        
        if filename.endswith('.pdf'):
            print(f"\n📄 PDF: {filename}")
            try:
                with pdfplumber.open(filepath) as pdf:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text()
                    print("--- Texto extraído (Primeras 500 chars) ---")
                    print(text[:500])
                    print("-------------------------------------------")
            except Exception as e:
                print(f"❌ Error leyendo PDF: {e}")
                
        elif filename.endswith('.docx'):
            print(f"\n📝 WORD: {filename}")
            try:
                text = docx2txt.process(filepath)
                print("--- Texto extraído (Primeras 500 chars) ---")
                print(text[:500])
                print("-------------------------------------------")
            except Exception as e:
                print(f"❌ Error leyendo Word: {e}")

if __name__ == "__main__":
    extract_fields_from_docs()
