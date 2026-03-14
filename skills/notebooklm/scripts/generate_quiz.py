#!/usr/bin/env python3
"""
Genera un quiz desde un notebook de NotebookLM.

Funcionalidad nueva habilitada por notebooklm-py — ideal para Active Recall
post-sesión del Flujo Maestro Brain OS v2.

Uso:
    python scripts/run.py generate_quiz.py --notebook-id economia-ambiental --format markdown
    python scripts/run.py generate_quiz.py --notebook-id investigacion-operativa --format json --output quiz.json
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from notebooklm_client import generate_quiz, check_auth, _resolve_notebook_id, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate quiz from NotebookLM notebook"
    )
    parser.add_argument("--notebook-id", help="Notebook ID from library")
    parser.add_argument("--notebook-url", help="NotebookLM notebook URL")
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "html"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument("--output", required=True, help="Output file path (.md / .json)")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium",
                        help="Difficulty (default: medium)")
    parser.add_argument("--quantity", choices=["fewer", "standard", "more"], default="standard",
                        help="Number of questions (default: standard)")
    parser.add_argument("--instructions", help="Custom instructions for quiz generation")
    args = parser.parse_args()

    # Verificar autenticación
    auth_status = check_auth()
    if not auth_status["success"]:
        print(f"⚠️ {auth_status['error']}")
        return 1

    # Resolver notebook ID
    notebook_id = args.notebook_id or ""
    if args.notebook_url:
        extracted = _extract_notebook_id_from_url(args.notebook_url)
        if extracted:
            notebook_id = extracted

    if not notebook_id:
        print("❌ Debes especificar --notebook-id o --notebook-url")
        return 1

    print(f"📝 Generando Quiz para: {notebook_id}")
    print(f"    Dificultad: {args.difficulty} | Cantidad: {args.quantity}")
    print("⏳ Generando preguntas...")

    result = generate_quiz(
        notebook_id=notebook_id,
        output_path=args.output,
        difficulty=args.difficulty,
        quantity=args.quantity,
        instructions=args.instructions,
    )

    if result["success"]:
        print(f"\n✅ Quiz guardado en: {result['output_path']}")
        return 0
    else:
        print(f"\n❌ Error: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
