#!/usr/bin/env python3
"""
Genera un Informe desde un notebook de NotebookLM.

Tipos: briefing_doc, study_guide, blog_post, custom

Uso:
    python scripts/run.py generate_report.py --notebook-id economia-ambiental --type briefing_doc --output briefing.md
    python scripts/run.py generate_report.py --notebook-id investigacion-operativa --type study_guide --output guia.md
    python scripts/run.py generate_report.py --notebook-id economia-ambiental --type custom --prompt "Haz un resumen ejecutivo de política ambiental" --output custom.md
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notebooklm_client import generate_report, generate_study_guide, check_auth, _extract_notebook_id_from_url

REPORT_TYPES = {
    "briefing_doc": "📄 Briefing Doc (resumen ejecutivo con citas clave)",
    "study_guide": "📚 Study Guide (guía de estudio con preguntas y glosario)",
    "blog_post": "📝 Blog Post (artículo accesible con insights)",
    "custom": "⚙️  Custom (prompt personalizado)",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Report from NotebookLM")
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--notebook-url", help="NotebookLM URL")
    parser.add_argument("--type", dest="report_type", choices=list(REPORT_TYPES.keys()),
                        default="briefing_doc", help="Report type (default: briefing_doc)")
    parser.add_argument("--output", required=True, help="Output file path (.md / .html)")
    parser.add_argument("--language", default="es", help="Language code (default: es)")
    parser.add_argument("--prompt", help="Custom prompt (only for --type custom)")
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

    if args.report_type == "custom" and not args.prompt:
        print("❌ El tipo 'custom' requiere --prompt")
        return 1

    label = REPORT_TYPES[args.report_type]
    print(f"📋 Generando: {label}")
    print(f"📚 Notebook: {notebook_id}")
    print("⏳ Esto puede tardar 1-2 minutos...")

    result = generate_report(
        notebook_id=notebook_id,
        output_path=args.output,
        report_format=args.report_type,
        language=args.language,
        custom_prompt=args.prompt,
    )

    if result["success"]:
        print(f"\n✅ Informe guardado en: {result['output_path']}")
        return 0
    print(f"\n❌ Error: {result['error']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
