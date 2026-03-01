import os
import subprocess
import time
from pathlib import Path

# Define paths
SCRIPTS_DIR = Path(__file__).parent
DOWNLOAD_SCRIPT = SCRIPTS_DIR / "download_files.py"
SYNC_LOCAL_SCRIPT = SCRIPTS_DIR / "sync_full_local.py"
SYNC_ASSIGN_SCRIPT = SCRIPTS_DIR / "sync_assignments.py"

def run_script(script_path, description):
    print(f"\n{'='*60}")
    print(f"🔄 EJECUTANDO: {description}")
    print(f"{'='*60}")
    
    if not script_path.exists():
        print(f"❌ Error: Script no encontrado en {script_path}")
        return False
        
    try:
        # Run python script
        result = subprocess.run(["python", str(script_path)], check=True)
        if result.returncode == 0:
            print(f"✅ {description} completado con éxito.")
            return True
        else:
            print(f"⚠️ {description} terminó con código {result.returncode}.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🧠 BRAIN OS: SINCRONIZACIÓN TOTAL DE AULA VIRTUAL")
    print("="*60)
    print("Iniciando secuencia de actualización...")
    
    start_time = time.time()
    
    # Step 1: Download Files & URLs
    if not run_script(DOWNLOAD_SCRIPT, "Descarga de Archivos y Generación de URLs (.url)"):
        print("⛔ abortando por error en descarga.")
        return

    # Step 2: Sync Local Files to Notion (Files + URLs)
    if not run_script(SYNC_LOCAL_SCRIPT, "Sincronización Local -> Notion (BD_RECURSOS)"):
        print("⛔ abortando por error en subida a Notion.")
        return

    # Step 3: Sync Assignments
    if not run_script(SYNC_ASSIGN_SCRIPT, "Sincronización de Tareas (BD_TAREAS_MAESTRAS)"):
        print("⛔ abortando por error en tareas.")
        return

    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print(f"✨ SINCRONIZACIÓN COMPLETA FINALIZADA en {elapsed:.2f} segundos.")
    print("="*60)

if __name__ == "__main__":
    main()
