import sys
import os
from pathlib import Path
import win32com.client
import pythoncom

def convert_pptx_to_pdf(input_path, output_path):
    print(f"🔄 Convirtiendo PPTX: {input_path}")
    powerpoint = win32com.client.DispatchEx("Powerpoint.Application")
    # powerpoint.Visible = 1
    try:
        deck = powerpoint.Presentations.Open(str(input_path), WithWindow=False)
        deck.SaveAs(str(output_path), 32) # 32 is the enum for PDF in PPT
        deck.Close()
        print(f"✅ Guardado: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error convirtiendo {input_path}: {e}")
        return False
    finally:
        powerpoint.Quit()

def convert_docx_to_pdf(input_path, output_path):
    print(f"🔄 Convirtiendo DOCX: {input_path}")
    word = win32com.client.DispatchEx("Word.Application")
    # word.Visible = 0
    try:
        doc = word.Documents.Open(str(input_path))
        doc.SaveAs(str(output_path), FileFormat=17) # 17 is the enum for PDF in Word
        doc.Close()
        print(f"✅ Guardado: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error convirtiendo {input_path}: {e}")
        return False
    finally:
        word.Quit()

def convert_xlsx_to_pdf(input_path, output_path):
    print(f"🔄 Convirtiendo XLSX: {input_path}")
    excel = win32com.client.DispatchEx("Excel.Application")
    # excel.Visible = False
    try:
        wb = excel.Workbooks.Open(str(input_path))
        wb.ExportAsFixedFormat(0, str(output_path)) # 0 is the enum for PDF xlTypePDF
        wb.Close(False)
        print(f"✅ Guardado: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error convirtiendo {input_path}: {e}")
        return False
    finally:
        excel.Quit()

def main():
    if len(sys.argv) < 2:
        print("Uso: python convert_to_pdf.py <ruta_carpeta>")
        sys.exit(1)
        
    target_dir = Path(sys.argv[1]).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"❌ La ruta {target_dir} no es un directorio válido.")
        sys.exit(1)
        
    # Inicializar COM en este hilo
    pythoncom.CoInitialize()
    
    converted_count = 0
    error_count = 0
    
    print(f"📂 Escaneando {target_dir} en busca de PPTX, DOCX y XLSX...")
    for file_path in target_dir.glob("*"):
        if file_path.is_file() and not file_path.name.startswith("~"):
            ext = file_path.suffix.lower()
            if ext in ['.pptx', '.doc', '.docx', '.ppt', '.xls', '.xlsx']:
                output_path = file_path.with_suffix('.pdf')
                if output_path.exists():
                    print(f"⏩ Saltando (ya existe PDF): {output_path.name}")
                    continue
                    
                success = False
                if ext in ['.pptx', '.ppt']:
                    success = convert_pptx_to_pdf(file_path, output_path)
                elif ext in ['.docx', '.doc']:
                    success = convert_docx_to_pdf(file_path, output_path)
                elif ext in ['.xlsx', '.xls']:
                    success = convert_xlsx_to_pdf(file_path, output_path)
                    
                if success:
                    converted_count += 1
                else:
                    error_count += 1
                    
    print(f"\n🎉 Proceso completado. Convertidos: {converted_count}. Errores: {error_count}.")
    pythoncom.CoUninitialize()

if __name__ == "__main__":
    main()
