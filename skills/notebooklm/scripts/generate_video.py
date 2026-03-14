#!/usr/bin/env python3
"""
Genera un Video Overview desde un notebook de NotebookLM.

Uso:
    python scripts/run.py generate_video.py --notebook-id economia-internacional-i --output video.mp4
    python scripts/run.py generate_video.py --notebook-id economia-ambiental --cinematic --output mini_doc.mp4
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notebooklm_client import generate_video, generate_cinematic_video, check_auth, _extract_notebook_id_from_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Video Overview from NotebookLM")
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--notebook-url", help="NotebookLM URL")
    parser.add_argument("--output", required=True, help="Output file path (.mp4)")
    parser.add_argument("--language", default="es", help="Language code (default: es)")
    parser.add_argument("--instructions", help="Custom instructions for video generation")
    parser.add_argument("--cinematic", action="store_true", help="Use Cinematic Video (Veo 3, requires AI Ultra)")
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

    mode = "Cinemático (Veo 3)" if args.cinematic else "Estándar"
    print(f"🎬 Generando Video Overview ({mode}) para: {notebook_id}")
    if args.cinematic:
        print("⚠️  AVISO: Los videos cinemáticos pueden tardar 30-40 minutos.")
    else:
        print("⏳ Esto puede tardar varios minutos...")

    gen_func = generate_cinematic_video if args.cinematic else generate_video

    result = gen_func(
        notebook_id=notebook_id,
        output_path=args.output,
        instructions=args.instructions,
        language=args.language,
    )

    if result["success"]:
        size = Path(result["output_path"]).stat().st_size / (1024 * 1024) if Path(result["output_path"]).exists() else 0
        print(f"\n✅ Video guardado: {result['output_path']} ({size:.1f} MB)")
        return 0
    print(f"\n❌ Error: {result['error']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
