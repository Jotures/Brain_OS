#!/usr/bin/env python3
"""
Genera y descarga Audio Overview de un notebook de NotebookLM.

Funcionalidad nueva habilitada por notebooklm-py — imposible con browser automation.

Uso:
    python scripts/run.py download_audio.py --notebook-id economia-internacional-i --output ./audio.mp3
    python scripts/run.py download_audio.py --notebook-url "https://..." --output ./audio.mp3 --instructions "Hazlo conciso"
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from notebooklm_client import generate_audio, check_auth, _resolve_notebook_id, _get_notebook_url, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Audio Overview from NotebookLM"
    )
    parser.add_argument("--notebook-id", help="Notebook ID from library")
    parser.add_argument("--notebook-url", help="NotebookLM notebook URL")
    parser.add_argument(
        "--output", required=True,
        help="Output file path (.mp3)"
    )
    parser.add_argument(
        "--instructions",
        default="Make it engaging and educational, in Spanish",
        help="Instructions for the audio generation"
    )
    parser.add_argument("--wait", action="store_true", default=True, help="Wait for completion (default: True)")

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

    resolved_id = _resolve_notebook_id(notebook_id)

    print(f"🎙️ Generando Audio Overview...")
    print(f"📚 Notebook: {resolved_id}")
    print(f"📝 Instrucciones: {args.instructions}")
    print(f"💾 Destino: {args.output}")
    print("⏳ Esto puede tardar 1-3 minutos...")

    result = generate_audio(
        notebook_id=resolved_id,
        output_path=args.output,
        instructions=args.instructions,
    )

    if result["success"]:
        output_path = Path(result["output_path"])
        size_mb = output_path.stat().st_size / (1024 * 1024) if output_path.exists() else 0
        print(f"\n✅ Audio Overview guardado: {result['output_path']} ({size_mb:.1f} MB)")
        return 0
    else:
        print(f"\n❌ Error: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
