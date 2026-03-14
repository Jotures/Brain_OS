#!/usr/bin/env python3
"""
Adaptador de notebooklm-py para Brain OS — v2.0 (Completo).

Encapsula el NotebookLMClient async en funciones síncronas.
Cubre TODAS las capacidades de NotebookLM Studio:
  - Chat/Query
  - Audio Overview (generar + descargar)
  - Video Overview (estándar + cinemático)
  - Report (Briefing Doc, Study Guide, Blog Post, Custom)
  - Quiz (con dificultad y cantidad configurables)
  - Flashcards
  - Infografía
  - Slide Deck (presentación)
  - Data Table
  - Mind Map
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

# --- Mapeo de notebooks de Brain OS ---
# Aliases cortos para notebooks frecuentes
ALIASES: dict[str, str] = {
    "ambiental": "economia-ambiental",
    "internacional": "economia-internacional-i",
    "gestion": "economia-y-gestion-publica",
    "publica": "economia-y-gestion-publica",
    "operativa": "investigacion-operativa",
    "monetaria": "teoria-monetaria-y-bancaria",
    "inv-economica": "investigacion-economica",
    "english": "ingles",
}


def _resolve_notebook_id(notebook_id: str) -> str:
    """Resuelve aliases a notebook IDs canónicos."""
    return ALIASES.get(notebook_id.lower().strip(), notebook_id.lower().strip())


def _extract_notebook_id_from_url(url: str) -> Optional[str]:
    """Extrae el ID de notebook de una URL NotebookLM."""
    if "notebooklm.google.com/notebook/" in url:
        parts = url.split("/notebook/")
        if len(parts) > 1:
            return parts[1].split("?")[0].strip("/")
    return None


def _get_notebook_url(notebook_id: str) -> Optional[str]:
    """Obtiene la URL del notebook desde el registry local."""
    candidates = [
        Path(__file__).parent.parent / "config" / "notebooklm_registry.json",
        Path(__file__).parent.parent / "data" / "library.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Formato library.json de notebook_manager
            for nb in data.get("notebooks", []):
                if nb.get("id") == notebook_id:
                    return nb.get("url")
            # Formato registry simple
            mapping = data.get("mapping", {})
            if notebook_id in mapping:
                return mapping[notebook_id]
        except (json.JSONDecodeError, KeyError):
            continue
    return None


async def _get_real_notebook_id(client, notebook_id: str, notebook_url: Optional[str] = None) -> str:
    """Resuelve un ID corto/alias al ID real del notebook via API lista."""
    # Si ya parece un ID largo (UUID-like), no necesitamos buscar
    if len(notebook_id) >= 30:
        return notebook_id

    # Si tenemos URL, extraer el ID directamente 
    if notebook_url:
        extracted = _extract_notebook_id_from_url(notebook_url)
        if extracted and len(extracted) >= 20:
            return extracted

    # Buscar en la lista de notebooks para hacer match por título
    try:
        notebooks = await client.notebooks.list()
        def normalize(s: str) -> str:
            import unicodedata
            s = s.lower().replace("-", " ").strip()
            return "".join(c for c in unicodedata.normalize("NFD", s)
                           if unicodedata.category(c) != "Mn")

        search_term = normalize(notebook_id)
        for nb in notebooks:
            title_norm = normalize(nb.title)
            if search_term in title_norm or notebook_id in nb.id:
                return nb.id
    except Exception:
        pass

    return notebook_id


# ========================================================
# Funciones async (privadas)
# ========================================================

async def _ask_async(notebook_id: str, question: str, notebook_url: Optional[str] = None) -> dict:
    from notebooklm import NotebookLMClient
    async with await NotebookLMClient.from_storage() as client:
        real_id = await _get_real_notebook_id(client, notebook_id, notebook_url)
        result = await client.chat.ask(real_id, question)
        return {
            "success": True,
            "answer": result.answer,
            "conversation_id": result.conversation_id,
            "turn_number": result.turn_number,
            "references": [
                {"source_id": r.source_id, "cited_text": r.cited_text}
                for r in (result.references or [])
            ],
        }


async def _list_notebooks_async() -> dict:
    from notebooklm import NotebookLMClient
    async with await NotebookLMClient.from_storage() as client:
        nbs = await client.notebooks.list()
        return {
            "success": True,
            "notebooks": [{"id": nb.id, "title": nb.title, "sources_count": nb.sources_count} for nb in nbs],
        }


async def _generate_and_download_async(
    notebook_id: str,
    output_path: str,
    artifact_type: str,
    options: dict,
) -> dict:
    """
    Motor genérico de generación: llama al método generate_X, espera y descarga.
    artifact_type: 'audio'|'video'|'cinematic_video'|'report'|'quiz'|'flashcards'|
                   'infographic'|'slide_deck'|'data_table'|'mind_map'|'study_guide'
    """
    from notebooklm import NotebookLMClient
    async with await NotebookLMClient.from_storage() as client:
        real_id = await _get_real_notebook_id(client, notebook_id)

        # Selección de método de generación
        art = client.artifacts
        if artifact_type == "audio":
            status = await art.generate_audio(real_id, **options)
        elif artifact_type == "video":
            status = await art.generate_video(real_id, **options)
        elif artifact_type == "cinematic_video":
            status = await art.generate_cinematic_video(real_id, **options)
        elif artifact_type == "report":
            status = await art.generate_report(real_id, **options)
        elif artifact_type == "study_guide":
            status = await art.generate_study_guide(real_id, **options)
        elif artifact_type == "quiz":
            status = await art.generate_quiz(real_id, **options)
        elif artifact_type == "flashcards":
            status = await art.generate_flashcards(real_id, **options)
        elif artifact_type == "infographic":
            status = await art.generate_infographic(real_id, **options)
        elif artifact_type == "slide_deck":
            status = await art.generate_slide_deck(real_id, **options)
        elif artifact_type == "data_table":
            status = await art.generate_data_table(real_id, **options)
        elif artifact_type == "mind_map":
            status = await art.generate_mind_map(real_id, **options)
        else:
            return {"success": False, "error": f"artifact_type desconocido: {artifact_type}"}

        # Esperar completación
        await art.wait_for_completion(real_id, status.task_id)

        # Descargar según tipo
        if artifact_type == "audio":
            await art.download_audio(real_id, output_path)
        elif artifact_type in ("video", "cinematic_video"):
            await art.download_video(real_id, output_path)
        elif artifact_type in ("report", "study_guide"):
            await art.download_report(real_id, output_path)
        elif artifact_type == "quiz":
            await art.download_quiz(real_id, output_path)
        elif artifact_type == "flashcards":
            await art.download_flashcards(real_id, output_path)
        elif artifact_type == "infographic":
            await art.download_infographic(real_id, output_path)
        elif artifact_type == "slide_deck":
            await art.download_slide_deck(real_id, output_path)
        elif artifact_type == "data_table":
            await art.download_data_table(real_id, output_path)
        elif artifact_type == "mind_map":
            await art.download_mind_map(real_id, output_path)

        return {"success": True, "output_path": output_path}


async def _check_auth_async() -> dict:
    from notebooklm.auth import AuthTokens
    try:
        await AuthTokens.from_storage()
        return {"success": True, "status": "authenticated"}
    except FileNotFoundError:
        return {"success": False, "status": "not_authenticated", "error": "Ejecuta: notebooklm login"}
    except ValueError as e:
        return {"success": False, "status": "expired", "error": str(e)}


# ========================================================
# API pública síncrona (para Brain OS / scripts CLI)
# ========================================================

def _run(coro):
    """Ejecuta una coroutine de forma síncrona."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


def check_auth() -> dict:
    """Verifica el estado de autenticación."""
    try:
        return _run(_check_auth_async())
    except ImportError:
        return {"success": False, "status": "not_installed", "error": "notebooklm-py no instalado"}


def ask_question(notebook_id: str, question: str, notebook_url: Optional[str] = None) -> dict:
    """Pregunta a un notebook (chat grounded)."""
    return _run(_ask_async(_resolve_notebook_id(notebook_id), question, notebook_url))


def list_notebooks() -> dict:
    """Lista todos los notebooks de la cuenta."""
    return _run(_list_notebooks_async())


# --- Generadores de artefactos ---

def generate_audio(
    notebook_id: str,
    output_path: str,
    instructions: Optional[str] = None,
    language: str = "es",
) -> dict:
    """Audio Overview como .mp3/.mp4."""
    options = {"language": language}
    if instructions:
        options["instructions"] = instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "audio", options))


def generate_video(
    notebook_id: str,
    output_path: str,
    instructions: Optional[str] = None,
    language: str = "es",
) -> dict:
    """Video Overview (presentación animada)."""
    options = {"language": language}
    if instructions:
        options["instructions"] = instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "video", options))


def generate_cinematic_video(
    notebook_id: str,
    output_path: str,
    instructions: Optional[str] = None,
    language: str = "es",
) -> dict:
    """Video Overview cinemático (Veo 3 — requiere AI Ultra, ~30-40 min)."""
    options = {"language": language}
    if instructions:
        options["instructions"] = instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "cinematic_video", options))


def generate_report(
    notebook_id: str,
    output_path: str,
    report_format: str = "briefing_doc",
    language: str = "es",
    custom_prompt: Optional[str] = None,
) -> dict:
    """
    Informe/Briefing. report_format: 'briefing_doc'|'study_guide'|'blog_post'|'custom'.
    """
    try:
        from notebooklm.rpc import ReportFormat
        fmt_map = {
            "briefing_doc": ReportFormat.BRIEFING_DOC,
            "study_guide": ReportFormat.STUDY_GUIDE,
            "blog_post": ReportFormat.BLOG_POST,
            "custom": ReportFormat.CUSTOM,
        }
        fmt = fmt_map.get(report_format, ReportFormat.BRIEFING_DOC)
    except ImportError:
        return {"success": False, "error": "notebooklm-py no instalado"}

    options = {"report_format": fmt, "language": language}
    if custom_prompt:
        options["custom_prompt"] = custom_prompt

    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "report", options))


def generate_study_guide(
    notebook_id: str,
    output_path: str,
    language: str = "es",
    extra_instructions: Optional[str] = None,
) -> dict:
    """Study Guide (guía de estudio estructurada)."""
    options = {"language": language}
    if extra_instructions:
        options["extra_instructions"] = extra_instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "study_guide", options))


def generate_quiz(
    notebook_id: str,
    output_path: str,
    difficulty: str = "medium",
    quantity: str = "standard",
    instructions: Optional[str] = None,
) -> dict:
    """Quiz de opción múltiple. difficulty: 'easy'|'medium'|'hard'. quantity: 'fewer'|'standard'|'more'."""
    try:
        from notebooklm.rpc import QuizDifficulty, QuizQuantity
        diff_map = {"easy": QuizDifficulty.EASY, "medium": QuizDifficulty.MEDIUM, "hard": QuizDifficulty.HARD}
        qty_map = {"fewer": QuizQuantity.FEWER, "standard": QuizQuantity.STANDARD, "more": QuizQuantity.MORE}
    except ImportError:
        return {"success": False, "error": "notebooklm-py no instalado"}

    options = {
        "difficulty": diff_map.get(difficulty, QuizDifficulty.MEDIUM),
        "quantity": qty_map.get(quantity, QuizQuantity.STANDARD),
    }
    if instructions:
        options["instructions"] = instructions

    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "quiz", options))


def generate_flashcards(
    notebook_id: str,
    output_path: str,
    difficulty: str = "medium",
    quantity: str = "standard",
    instructions: Optional[str] = None,
) -> dict:
    """Flashcards (tarjetas didácticas). difficulty: 'easy'|'medium'|'hard'."""
    try:
        from notebooklm.rpc import QuizDifficulty, QuizQuantity
        diff_map = {"easy": QuizDifficulty.EASY, "medium": QuizDifficulty.MEDIUM, "hard": QuizDifficulty.HARD}
        qty_map = {"fewer": QuizQuantity.FEWER, "standard": QuizQuantity.STANDARD, "more": QuizQuantity.MORE}
    except ImportError:
        return {"success": False, "error": "notebooklm-py no instalado"}

    options = {
        "difficulty": diff_map.get(difficulty, QuizDifficulty.MEDIUM),
        "quantity": qty_map.get(quantity, QuizQuantity.STANDARD),
    }
    if instructions:
        options["instructions"] = instructions

    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "flashcards", options))


def generate_infographic(
    notebook_id: str,
    output_path: str,
    orientation: str = "portrait",
    language: str = "es",
    instructions: Optional[str] = None,
) -> dict:
    """Infografía. orientation: 'landscape'|'portrait'|'square'."""
    try:
        from notebooklm.rpc import InfographicOrientation
        ori_map = {
            "landscape": InfographicOrientation.LANDSCAPE,
            "portrait": InfographicOrientation.PORTRAIT,
            "square": InfographicOrientation.SQUARE,
        }
    except ImportError:
        return {"success": False, "error": "notebooklm-py no instalado"}

    options = {"orientation": ori_map.get(orientation, InfographicOrientation.PORTRAIT), "language": language}
    if instructions:
        options["instructions"] = instructions

    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "infographic", options))


def generate_slide_deck(
    notebook_id: str,
    output_path: str,
    language: str = "es",
    instructions: Optional[str] = None,
) -> dict:
    """Slide Deck (presentación .pptx / Google Slides)."""
    options = {"language": language}
    if instructions:
        options["instructions"] = instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "slide_deck", options))


def generate_data_table(
    notebook_id: str,
    output_path: str,
    language: str = "es",
    instructions: Optional[str] = None,
) -> dict:
    """Tabla de datos (.csv / .json)."""
    options = {"language": language}
    if instructions:
        options["instructions"] = instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "data_table", options))


def generate_mind_map(
    notebook_id: str,
    output_path: str,
    language: str = "es",
    instructions: Optional[str] = None,
) -> dict:
    """Mapa mental (Mind Map)."""
    options = {"language": language}
    if instructions:
        options["instructions"] = instructions
    return _run(_generate_and_download_async(_resolve_notebook_id(notebook_id), output_path, "mind_map", options))


if __name__ == "__main__":
    result = check_auth()
    print(json.dumps(result, indent=2, ensure_ascii=False))
