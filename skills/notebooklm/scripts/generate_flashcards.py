#!/usr/bin/env python3
"""
Genera Flashcards (Tarjetas Didácticas) desde un notebook de NotebookLM.

Uso:
    python scripts/run.py generate_flashcards.py --notebook-id economia-internacional-i --output flashcards.md
    python scripts/run.py generate_flashcards.py --notebook-id investigacion-operativa --difficulty hard --quantity more --output flashcards_io.md
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notebooklm_client import generate_flashcards, check_auth, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Flashcards from NotebookLM")
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--notebook-url", help="NotebookLM URL")
    parser.add_argument("--output", required=True, help="Output file path (.md / .json)")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium",
                        help="Difficulty (default: medium)")
    parser.add_argument("--quantity", choices=["fewer", "standard", "more"], default="standard",
                        help="Number of cards (default: standard)")
    parser.add_argument("--instructions", help="Custom instructions for card generation")
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

    print(f"🗂️  Generando Flashcards para: {notebook_id}")
    print(f"    Dificultad: {args.difficulty} | Cantidad: {args.quantity}")
    print("⏳ Generando tarjetas...")

    result = generate_flashcards(
        notebook_id=notebook_id,
        output_path=args.output,
        difficulty=args.difficulty,
        quantity=args.quantity,
        instructions=args.instructions,
    )

    if result["success"]:
        print(f"\n✅ Flashcards guardadas en: {result['output_path']}")
        return 0
    print(f"\n❌ Error: {result['error']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
