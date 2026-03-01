import argparse
import sys
import os
import subprocess
import json
import re

def main():
    parser = argparse.ArgumentParser(description="Analyze book structure in NotebookLM to find chapter page ranges.")
    parser.add_argument("--notebook-id", required=True, help="ID of the notebook containing the book.")
    parser.add_argument("--chapters", required=True, help="Comma-separated list of chapters to locate (e.g., '1,8').")
    
    args = parser.parse_args()
    
    chapters = [c.strip() for c in args.chapters.split(',')]
    chapters_str = ", ".join(chapters)
    
    # Construct the prompt
    prompt = (
        f"Analiza la estructura del libro cargado. Necesito ubicar exactamente los rangos de páginas "
        f"para los siguientes capítulos: {chapters}. "
        f"Por favor, entrégame una lista clara con el formato: "
        f"'Capítulo X: Página Inicio - Página Fin'. "
        f"Si el libro no tiene números de página explícitos, describe la ubicación o sección lo mejor posible. "
        f"IMPORTANTE: Usa listas de Markdown o viñetas. NO uses tablas ASCII ni formatos complejos que se rompan en texto plano."
    )
    
    print(f"📚 Analyzing chapters: {chapters_str}...")
    print(f"🔍 Notebook ID: {args.notebook_id}")
    
    # Path to run.py and ask_question.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run_script = os.path.join(script_dir, "run.py")
    ask_script = "ask_question.py"
    
    # Execute ask_question.py via run.py
    cmd = [
        sys.executable,
        run_script,
        ask_script,
        "--notebook-id", args.notebook_id,
        "--question", prompt
    ]
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        # We capture output to parse it, but also print it to stdout for the user to see progress
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8', # Force encoding
            env=env
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print("❌ Error executing query:")
            print(stderr)
            sys.exit(process.returncode)
            
        # Extract the answer part from the logs if possible, or just print the whole thing
        # The ask_question.py usually prints "🤖 Answer: ..." or similar.
        # Let's just print the output for now, as the user wants the info.
        
        # Simple parsing to highlight the result
        print("\n" + "="*50)
        print("🤖 NOTEBOOKLM ANALYSIS RESULT")
        print("="*50 + "\n")
        
        # Filter out some log noise if we want, but raw output is safer
        print(stdout)
        
    except Exception as e:
        print(f"❌ critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
