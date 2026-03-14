#!/usr/bin/env python3
"""
Ask NotebookLM a question — v2 (notebooklm-py engine).

CLI 100% compatible con ask_question.py original.
Internamente usa notebooklm_client.py en lugar de Patchright browser automation.

Uso:
    python scripts/run.py ask_question_v2.py --question "¿Qué es X?" --notebook-id economia-internacional-i
    python scripts/run.py ask_question_v2.py --question "..." --notebook-url "https://notebooklm.google.com/notebook/..."
"""

import argparse
import json
import sys
from pathlib import Path

# Agregar directorio padre al path
sys.path.insert(0, str(Path(__file__).parent))

from notebooklm_client import ask_question, check_auth, _resolve_notebook_id, _get_notebook_url


# Mismo reminder que ask_question.py para mantener compatibilidad
FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? "
    "You can always ask another question! Think about it carefully: "
    "before you reply to the user, review their original request and this answer. "
    "If anything is still unclear or missing, ask me another comprehensive question "
    "that includes all necessary context."
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ask NotebookLM a question (v2 — HTTP engine)"
    )
    parser.add_argument("--question", required=True, help="Question to ask")
    parser.add_argument("--notebook-url", help="NotebookLM notebook URL")
    parser.add_argument("--notebook-id", help="Notebook ID from library")
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Ignored in v2 (backward compat flag)",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output raw JSON instead of formatted text",
    )

    args = parser.parse_args()

    # Verificar autenticación
    auth_status = check_auth()
    if not auth_status["success"]:
        print(f"⚠️ {auth_status['error']}")
        return 1

    # Resolver notebook
    notebook_url = args.notebook_url
    notebook_id = args.notebook_id

    if not notebook_url and not notebook_id:
        # Intentar obtener el notebook activo desde la biblioteca legacy
        try:
            from notebook_manager import NotebookLibrary

            library = NotebookLibrary()
            active = library.get_active_notebook()
            if active:
                notebook_url = active["url"]
                notebook_id = active.get("id", "")
                print(f"📚 Using active notebook: {active['name']}")
            else:
                notebooks = library.list_notebooks()
                if notebooks:
                    print("\n📚 Available notebooks:")
                    for nb in notebooks:
                        mark = (
                            " [ACTIVE]"
                            if nb.get("id") == library.active_notebook_id
                            else ""
                        )
                        print(f"  {nb['id']}: {nb['name']}{mark}")
                    print("\nSpecify with --notebook-id or --notebook-url")
                else:
                    print("❌ No notebooks in library. Add one first.")
                return 1
        except ImportError:
            print("❌ No notebook specified. Use --notebook-id or --notebook-url")
            return 1

    if not notebook_id:
        notebook_id = "unknown"

    print(f"💬 Asking: {args.question}")
    print(f"📚 Notebook: {notebook_id}")
    print(f"⚡ Engine: notebooklm-py v2 (HTTP direct)")

    # Hacer la pregunta
    result = ask_question(
        notebook_id=notebook_id,
        question=args.question,
        notebook_url=notebook_url,
    )

    if args.json_output:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["success"] else 1

    if result["success"]:
        answer = result["answer"]
        print("\n" + "=" * 60)
        print(f"Question: {args.question}")
        print("=" * 60)
        print()
        print(answer + FOLLOW_UP_REMINDER)
        print()
        print("=" * 60)

        # Mostrar referencias si existen
        refs = result.get("references", [])
        if refs:
            print(f"\n📎 {len(refs)} reference(s) found")
            for i, ref in enumerate(refs, 1):
                cited = ref.get("cited_text", "")
                if cited:
                    preview = cited[:100] + "..." if len(cited) > 100 else cited
                    print(f"  [{i}] {preview}")

        return 0
    else:
        print(f"\n❌ Error: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
