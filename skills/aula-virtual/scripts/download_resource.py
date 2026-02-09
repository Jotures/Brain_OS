#!/usr/bin/env python3
import sys
import os
import requests
from pathlib import Path
from moodle_api import MoodleAPI

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("Usage: python download_resource.py <file_url> [output_filename]")
        return

    file_url = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else "downloaded_resource.pdf"
    
    print(f"⬇️ Iniciando descarga de: {file_url}")
    
    try:
        api = MoodleAPI()
        token = api.token
        
        # Append token to URL if not present
        if "token=" not in file_url:
            download_url = f"{file_url}&token={token}"
        else:
            download_url = file_url
            
        print(f"🔑 Token adjuntado. Descargando...")
        
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Save file
        output_path = Path(output_filename)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"✅ Archivo guardado en: {output_path.absolute()}")
        
    except Exception as e:
        print(f"❌ Error descargando archivo: {e}")

if __name__ == "__main__":
    main()
