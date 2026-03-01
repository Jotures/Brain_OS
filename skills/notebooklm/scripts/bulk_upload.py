import sys
import os
import time
import json
import re
from pathlib import Path
from patchright.sync_api import sync_playwright

# Modificar sys.path para importar librerías de NotebookLM
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

# Encontrar raíz de Brain_OS
brain_os_dir = current_dir.parent.parent.parent

from auth_manager import AuthManager
from browser_utils import BrowserFactory

def sync_notebooks():
    registry_path = brain_os_dir / "config" / "notebooklm_registry.json"
    if not registry_path.exists():
        print(f"❌ No se encontró registry en {registry_path}")
        return
        
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
        
    notebooks = registry.get("notebooks", [])
    
    with sync_playwright() as p:
        auth = AuthManager()
        if not auth.is_authenticated():
            print("❌ No estás autenticado en NotebookLM. Usa auth_manager.py primero.")
            return

        print("🚀 Lanzando navegador en segundo plano (1080p)...")
        context = BrowserFactory.launch_persistent_context(p, headless=True)
        page = context.new_page()
        
        for nb in notebooks:
            curso_path = nb.get("curso_path")
            url = nb.get("url")
            
            if not curso_path or not url:
                continue
                
            base_dir = brain_os_dir / curso_path / "01_Materiales"
            if not base_dir.exists():
                print(f"⏩ Omitiendo (Directorio no existe): {base_dir}")
                continue
                
            files = [f for f in base_dir.iterdir() if f.is_file() and f.suffix.lower() in [".pdf", ".md", ".docx", ".txt"]]
            if not files:
                continue
                
            print(f"\n======== Sincronizando: {nb['name']} ========")
            print(f"🌐 Navegando a libreta...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(8) # Espera adicional para carga de UI
            
            body_text = page.locator("body").inner_text()
            
            for f in files:
                # NotebookLM trunca los nombres de archivos largos. Comparamos los primeros 25 caracteres.
                name_prefix = f.name[:25]
                
                if name_prefix in body_text:
                    print(f"✅ Ya existe: {f.name}")
                    continue
                    
                print(f"📤 Subiendo nuevo documento: {f.name[:40]}...")
                
                # Proceso de subida via UI
                clicked = False
                try:
                    elements = page.get_by_text(re.compile(r"agregar fuentes?|add sources?", re.I)).all()
                    for el in elements:
                        if el.is_visible():
                            el.click()
                            clicked = True
                            break
                    if not clicked:
                        page.get_by_text(re.compile(r"agregar fuentes?|add sources?", re.I)).first.click(force=True)
                except Exception as e:
                    print(f"   ⚠️ Error abriendo modal de fuentes: {e}")
                    continue
                    
                time.sleep(4)
                
                upload_clicked = False
                try:
                    elements = page.get_by_text(re.compile(r"subir archivos?|upload files?", re.I)).all()
                    for el in elements:
                        if el.is_visible():
                            with page.expect_file_chooser(timeout=15000) as fc_info:
                                el.click()
                            file_chooser = fc_info.value
                            file_chooser.set_files(str(f))
                            upload_clicked = True
                            print("   ✅ Inyectado en NotebookLM via selector standard.")
                            break
                except Exception as e:
                    pass
                    
                if not upload_clicked:
                    try:
                        page.locator("input[type='file']").first.set_input_files(str(f))
                        print("   ✅ Inyectado en NotebookLM via input oculto.")
                    except:
                        print("   ❌ Error al inyectar archivo. Saltando...")
                        continue
                        
                print("   ⏳ Esperando que NotebookLM procese (15s)...")
                time.sleep(15)
                
                # Actualizar el body text para futuras comparaciones de esta misma libreta
                body_text = page.locator("body").inner_text()

        context.close()
        print("\n✨ SINCRONIZACIÓN MASIVA HACIA NOTEBOOKLM FINALIZADA ✨")

if __name__ == "__main__":
    sync_notebooks()
