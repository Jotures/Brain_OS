import PyPDF2
import sys
import os

files = [
    r"c:\Users\Ruben J\Documents\Antigravito Proyects\Brain_OS\carrera\semestres\2026-1\cursos\01_economia_ambiental\01_Materiales\Acta Economia Ambiental.pdf",
    r"c:\Users\Ruben J\Documents\Antigravito Proyects\Brain_OS\carrera\semestres\2026-1\cursos\01_economia_ambiental\01_Materiales\Sílabo de Economia Ambiental 2026-I.pdf"
]

for file in files:
    print(f"\n--- Extracting: {os.path.basename(file)} ---")
    try:
        with open(file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for i in range(min(5, len(reader.pages))): # just first 5 pages, usually assignment info isn't too far or is in the whole
                text += reader.pages[i].extract_text()
            
            # Print lines that contain keywords
            lines = text.split('\n')
            for line in lines:
                if any(kw in line.lower() for kw in ['investigación', 'formativa', 'trabajo', 'rubrica', 'pauta', 'evaluación']):
                    print(line.strip())
    except Exception as e:
        print(f"Error parsing {file}: {e}")
