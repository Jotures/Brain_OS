#!/usr/bin/env python3
"""
Genera un Mapa Mental (Mind Map) desde un notebook de NotebookLM.

Uso:
    python scripts/run.py generate_mind_map.py --notebook-id economia-internacional-i --output mapa.json
    python scripts/run.py generate_mind_map.py --notebook-id economia-ambiental --instructions "Enfócate en instrumentos de política ambiental" --output mapa.json
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notebooklm_client import generate_mind_map, check_auth, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Mind Map from NotebookLM")
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--notebook-url", help="NotebookLM URL")
    parser.add_argument("--output", required=True, help="Output file path (.json)")
    parser.add_argument("--language", default="es", help="Language code (default: es)")
    parser.add_argument("--instructions", help="Custom instructions for mind map generation")
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

    print(f"🗺️  Generando Mapa Mental para: {notebook_id}")
    print("⏳ Generando estructura conceptual...")

    result = generate_mind_map(
        notebook_id=notebook_id,
        output_path=args.output,
        language=args.language,
        instructions=args.instructions,
    )

    if result["success"]:
        print(f"\n✅ Mapa Mental guardado en: {result['output_path']}")
        return 0
    print(f"\n❌ Error: {result['error']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
