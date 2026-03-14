#!/usr/bin/env python3
"""
Genera una Infografía desde un notebook de NotebookLM.

Uso:
    python scripts/run.py generate_infographic.py --notebook-id economia-ambiental --output infografia.png
    python scripts/run.py generate_infographic.py --notebook-id investigacion-operativa --orientation landscape --output infografia_io.png
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notebooklm_client import generate_infographic, check_auth, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Infographic from NotebookLM")
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--notebook-url", help="NotebookLM URL")
    parser.add_argument("--output", required=True, help="Output file path (.png)")
    parser.add_argument("--orientation", choices=["portrait", "landscape", "square"],
                        default="portrait", help="Orientation (default: portrait)")
    parser.add_argument("--language", default="es", help="Language code (default: es)")
    parser.add_argument("--instructions", help="Custom instructions for infographic generation")
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

    print(f"🖼️  Generando Infografía para: {notebook_id}")
    print(f"    Orientación: {args.orientation} | Idioma: {args.language}")
    print("⏳ Generando imagen...")

    result = generate_infographic(
        notebook_id=notebook_id,
        output_path=args.output,
        orientation=args.orientation,
        language=args.language,
        instructions=args.instructions,
    )

    if result["success"]:
        print(f"\n✅ Infografía guardada en: {result['output_path']}")
        return 0
    print(f"\n❌ Error: {result['error']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
