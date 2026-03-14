#!/usr/bin/env python3
"""
Genera una Tabla de Datos desde un notebook de NotebookLM.

Extrae datos estructurados del notebook en formato CSV/JSON.

Uso:
    python scripts/run.py generate_data_table.py --notebook-id economia-ambiental --output tabla.csv
    python scripts/run.py generate_data_table.py --notebook-id investigacion-operativa --format json --output tabla.json
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notebooklm_client import generate_data_table, check_auth, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Data Table from NotebookLM")
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--notebook-url", help="NotebookLM URL")
    parser.add_argument("--output", required=True, help="Output file path (.csv / .json)")
    parser.add_argument("--language", default="es", help="Language code (default: es)")
    parser.add_argument("--instructions", help="Custom instructions for table generation")
    args = parser.parse_args()

    auth = check_auth()
    if not auth["success"]:
        print(f"⚠️ {auth['error']}")
        return 1

    notebook_id = args.notebook_id or ""
    if args.notebook_url:
        extracted = _extract_notebook_id_from_url(args.notebook_url)
        if extracted:
            notebook_id = extracted

    if not notebook_id:
        print("❌ Especifica --notebook-id o --notebook-url")
        return 1

    print(f"📊 Generando Tabla de Datos para: {notebook_id}")
    print("⏳ Extrayendo datos estructurados...")

    result = generate_data_table(
        notebook_id=notebook_id,
        output_path=args.output,
        language=args.language,
        instructions=args.instructions,
    )

    if result["success"]:
        print(f"\n✅ Tabla guardada en: {result['output_path']}")
        return 0
    print(f"\n❌ Error: {result['error']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
