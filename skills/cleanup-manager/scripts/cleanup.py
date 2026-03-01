"""
Cleanup Manager — Escaneo y limpieza inteligente para Brain OS.

Uso:
    python cleanup.py --scan                    # Solo escanear (Nivel 0)
    python cleanup.py --clean --level 1         # Limpieza rápida
    python cleanup.py --clean --level 2         # Limpieza conservadora
    python cleanup.py --clean --level 3         # Limpieza profunda
    python cleanup.py --restore SESSION_DATE    # Restaurar desde archivo
    python cleanup.py --report                  # Reporte semanal
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Resolución de rutas mediante variable de entorno o detección
BRAIN_OS_ROOT = Path(os.getenv(
    "BRAIN_OS_ROOT",
    r"c:\Users\Ruben J\Documents\Antigravito Proyects\Brain_OS"
))
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "cleanup_config.json"
HISTORY_PATH = BRAIN_OS_ROOT / "cleanup_history.json"
ARCHIVE_DIR = BRAIN_OS_ROOT / "cleanup_archive"

# Zonas protegidas: nunca eliminar sin confirmación explícita
PROTECTED_PATTERNS = [
    "carrera/semestres",
    "config",
    ".agent/workflows",
    "brain_config.md",
    "INICIO.md",
    "README.md",
    "Flujo_Maestro_BrainOS_v2.md",
]


def load_config() -> dict:
    """Carga la configuración del cleanup-manager."""
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  cleanup_config.json no encontrado, usando defaults.")
        return {"thresholds": {"healthy_mb": 10, "warning_mb": 50}}


def is_protected(rel_path: str) -> bool:
    """Verifica si una ruta relativa está en zona protegida."""
    rel_normalized = rel_path.replace("\\", "/")
    for pattern in PROTECTED_PATTERNS:
        if rel_normalized.startswith(pattern) or rel_normalized == pattern:
            return True
    return False


def scan_system() -> dict:
    """Escanea el sistema completo y categoriza la basura encontrada."""
    results = {
        "pycache": [],
        "old_files": [],
        "debug_files": [],
        "temp_files": [],
        "browser_cache": [],
        "empty_dirs_browser": [],
        "empty_dirs_course": [],
        "log_files": [],
        "scan_temp": [],
        "totals": {
            "files": 0,
            "size_kb": 0,
            "categories": {},
        },
    }

    for dirpath, dirnames, filenames in os.walk(BRAIN_OS_ROOT):
        rel = os.path.relpath(dirpath, BRAIN_OS_ROOT)

        # Ignorar .git y .gemini
        if ".git" in rel.split(os.sep) or ".gemini" in rel.split(os.sep):
            continue

        # __pycache__
        if os.path.basename(dirpath) == "__pycache__":
            size = sum(
                os.path.getsize(os.path.join(dirpath, f))
                for f in filenames
                if os.path.exists(os.path.join(dirpath, f))
            )
            results["pycache"].append({
                "path": rel,
                "files": len(filenames),
                "size_kb": size // 1024,
            })
            continue

        # Carpetas vacías
        if not dirnames and not filenames:
            rel_norm = rel.replace("\\", "/")
            if "browser_state" in rel_norm or "notebooklm" in rel_norm:
                results["empty_dirs_browser"].append(rel)
            elif "carrera/" in rel_norm or "cursos_personales/" in rel_norm:
                results["empty_dirs_course"].append(rel)

        for f in filenames:
            fpath = os.path.join(dirpath, f)
            frel = os.path.join(rel, f)
            try:
                size_kb = os.path.getsize(fpath) // 1024
            except OSError:
                continue

            rel_norm = frel.replace("\\", "/")

            # .old en browser_state
            if f.endswith(".old") and "browser_state" in rel_norm:
                results["old_files"].append({"path": frel, "size_kb": size_kb})

            # debug_
            if f.startswith("debug_"):
                results["debug_files"].append({"path": frel, "size_kb": size_kb})

            # temp_
            if f.startswith("temp_") and "site-packages" not in rel_norm:
                results["temp_files"].append({"path": frel, "size_kb": size_kb})

            # .log en browser_state
            if f.endswith(".log") and "browser_state" in rel_norm:
                results["log_files"].append({"path": frel, "size_kb": size_kb})

            # Browser cache (subdirs grandes)
            if "browser_state" in rel_norm and any(
                d in rel_norm for d in ["Cache_Data", "Code Cache", "GrShaderCache"]
            ):
                results["browser_cache"].append({"path": frel, "size_kb": size_kb})

            # Scan temp files (de esta propia skill)
            if f in ("_scan_system.py", "_scan_results.txt"):
                results["scan_temp"].append({"path": frel, "size_kb": size_kb})

    # Calcular totales
    for cat_name, items in results.items():
        if cat_name in ("totals", "empty_dirs_course"):
            continue
        if isinstance(items, list):
            cat_files = len(items)
            cat_size = sum(item.get("size_kb", 0) if isinstance(item, dict) else 0 for item in items)
            if cat_name == "pycache":
                cat_size = sum(item["size_kb"] for item in items)
                cat_files = sum(item["files"] for item in items)
            results["totals"]["categories"][cat_name] = {
                "files": cat_files,
                "size_kb": cat_size,
            }
            results["totals"]["files"] += cat_files
            results["totals"]["size_kb"] += cat_size

    return results


def print_scan_report(results: dict) -> None:
    """Imprime el reporte de escaneo en formato legible."""
    print("\n" + "=" * 60)
    print("🧹 ESCANEO DE BASURA — Brain OS")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    categories_display = {
        "pycache": ("__pycache__", "1 (auto)"),
        "old_files": (".old browser", "1 (auto)"),
        "scan_temp": ("Scan temporales", "1 (auto)"),
        "empty_dirs_browser": ("Dirs vacíos browser", "1 (auto)"),
        "debug_files": ("debug_*", "2 (confirmar)"),
        "temp_files": ("temp_*", "2 (confirmar)"),
        "browser_cache": ("Browser cache", "2 (confirmar)"),
        "log_files": (".log browser", "2 (confirmar)"),
    }

    print(f"\n{'Categoría':<25} {'Archivos':>8} {'Tamaño':>10} {'Nivel':>16}")
    print("-" * 62)

    total_files = 0
    total_kb = 0

    for cat_key, (display_name, level) in categories_display.items():
        stats = results["totals"]["categories"].get(cat_key, {"files": 0, "size_kb": 0})
        files = stats["files"]
        size_kb = stats["size_kb"]
        total_files += files
        total_kb += size_kb

        if size_kb >= 1024:
            size_str = f"{size_kb / 1024:.1f} MB"
        else:
            size_str = f"{size_kb} KB"

        print(f"  {display_name:<23} {files:>8} {size_str:>10} {level:>16}")

    print("-" * 62)
    if total_kb >= 1024:
        total_str = f"{total_kb / 1024:.1f} MB"
    else:
        total_str = f"{total_kb} KB"
    print(f"  {'TOTAL RECUPERABLE':<23} {total_files:>8} {total_str:>10}")

    # Health indicator
    config = load_config()
    thresholds = config.get("thresholds", {})
    total_mb = total_kb / 1024

    if total_mb < thresholds.get("healthy_mb", 10):
        health = "🟢 Sistema limpio"
    elif total_mb < thresholds.get("warning_mb", 50):
        health = "🟡 Limpieza recomendada"
    else:
        health = "🔴 Limpieza urgente"

    print(f"\n  Estado: {health}")

    # Protected zones
    course_empty = len(results.get("empty_dirs_course", []))
    if course_empty:
        print(f"\n  🛡️  {course_empty} carpetas vacías de cursos PROTEGIDAS (estructura intencional)")

    print(f"\n  💡 Ejecuta con --clean --level 1 para limpieza automática segura.")
    print()


def archive_file(filepath: Path, session_dir: Path) -> dict:
    """Mueve un archivo al directorio de archivo para rollback."""
    session_dir.mkdir(parents=True, exist_ok=True)
    dest = session_dir / filepath.name

    # Evitar colisiones de nombre
    counter = 1
    while dest.exists():
        stem = filepath.stem
        suffix = filepath.suffix
        dest = session_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    shutil.move(str(filepath), str(dest))
    return {
        "original_path": str(filepath.relative_to(BRAIN_OS_ROOT)),
        "archived_as": dest.name,
        "size_kb": os.path.getsize(dest) // 1024 if dest.exists() else 0,
    }


def execute_cleanup(results: dict, level: int) -> dict:
    """Ejecuta la limpieza según el nivel especificado."""
    session = {
        "date": datetime.now().isoformat(),
        "level": level,
        "files_removed": 0,
        "dirs_removed": 0,
        "space_recovered_kb": 0,
        "archived_files": [],
        "errors": [],
    }

    session_date = datetime.now().strftime("%Y-%m-%d_%H%M")
    session_dir = ARCHIVE_DIR / session_date

    # ── Nivel 1: Limpieza automática segura ──
    if level >= 1:
        # Eliminar __pycache__
        for item in results["pycache"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            try:
                shutil.rmtree(full_path)
                session["dirs_removed"] += 1
                session["space_recovered_kb"] += item["size_kb"]
                print(f"  🗑️  {item['path']} ({item['size_kb']}KB)")
            except OSError as e:
                session["errors"].append(f"pycache {item['path']}: {e}")

        # Eliminar .old en browser_state
        for item in results["old_files"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            try:
                os.remove(full_path)
                session["files_removed"] += 1
                session["space_recovered_kb"] += item["size_kb"]
            except OSError as e:
                session["errors"].append(f"old {item['path']}: {e}")
        if results["old_files"]:
            print(f"  🗑️  {len(results['old_files'])} archivos .old eliminados")

        # Eliminar carpetas vacías de browser
        for item in results["empty_dirs_browser"]:
            full_path = BRAIN_OS_ROOT / item
            try:
                os.rmdir(full_path)
                session["dirs_removed"] += 1
            except OSError:
                pass  # No es error si no se puede (puede tener contenido nuevo)
        if results["empty_dirs_browser"]:
            print(f"  🗑️  {len(results['empty_dirs_browser'])} carpetas vacías eliminadas")

        # Eliminar scan temp files
        for item in results["scan_temp"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            try:
                os.remove(full_path)
                session["files_removed"] += 1
                session["space_recovered_kb"] += item["size_kb"]
                print(f"  🗑️  {item['path']}")
            except OSError as e:
                session["errors"].append(f"scan_temp {item['path']}: {e}")

    # ── Nivel 2: Archivar con confirmación ──
    if level >= 2:
        # Archivar debug_*
        for item in results["debug_files"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            if full_path.exists():
                archived = archive_file(full_path, session_dir)
                session["archived_files"].append(archived)
                session["files_removed"] += 1
                session["space_recovered_kb"] += item["size_kb"]
                print(f"  📦 Archivado: {item['path']}")

        # Archivar temp_*
        for item in results["temp_files"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            if full_path.exists():
                archived = archive_file(full_path, session_dir)
                session["archived_files"].append(archived)
                session["files_removed"] += 1
                session["space_recovered_kb"] += item["size_kb"]
                print(f"  📦 Archivado: {item['path']}")

        # Archivar .log de browser
        for item in results["log_files"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            if full_path.exists() and item["size_kb"] > 0:
                try:
                    os.remove(full_path)
                    session["files_removed"] += 1
                    session["space_recovered_kb"] += item["size_kb"]
                except OSError:
                    pass
        if results["log_files"]:
            print(f"  🗑️  {len(results['log_files'])} logs de browser eliminados")

        # Browser cache
        for item in results["browser_cache"]:
            full_path = BRAIN_OS_ROOT / item["path"]
            try:
                if full_path.exists():
                    os.remove(full_path)
                    session["files_removed"] += 1
                    session["space_recovered_kb"] += item["size_kb"]
            except OSError:
                pass
        if results["browser_cache"]:
            cache_mb = sum(i["size_kb"] for i in results["browser_cache"]) / 1024
            print(f"  🗑️  Browser cache eliminado ({cache_mb:.1f} MB)")

    # ── Nivel 3: Limpieza profunda (reporta, no ejecuta automáticamente) ──
    if level >= 3:
        print("\n  ⚠️  Nivel 3: Los archivos grandes requieren revisión manual.")
        print("  Los siguientes archivos podrían ser candidatos a eliminación:")
        print("  (No se eliminan automáticamente — usa confirmación explícita)")

    # Guardar manifest si se archivaron archivos
    if session["archived_files"] and session_dir.exists():
        manifest = {
            "date": session["date"],
            "level": level,
            "files": session["archived_files"],
        }
        with open(session_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    return session


def save_history(session: dict) -> None:
    """Registra la sesión de limpieza en el historial."""
    history = {"last_scan": None, "last_cleanup": None, "total_recovered_mb": 0, "sessions": []}

    if HISTORY_PATH.exists():
        try:
            with open(HISTORY_PATH, encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass

    history["last_cleanup"] = session["date"]
    history["total_recovered_mb"] += session["space_recovered_kb"] / 1024
    history["sessions"].append({
        "date": session["date"],
        "level": session["level"],
        "files_removed": session["files_removed"],
        "dirs_removed": session["dirs_removed"],
        "space_recovered_mb": round(session["space_recovered_kb"] / 1024, 2),
        "errors": len(session["errors"]),
    })

    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def restore_from_archive(session_date: Optional[str] = None) -> None:
    """Restaura archivos desde el directorio de archivo."""
    if not ARCHIVE_DIR.exists():
        print("❌ No hay archivos en cleanup_archive/")
        return

    sessions = sorted(ARCHIVE_DIR.iterdir())
    if not sessions:
        print("❌ No hay sesiones de archivo disponibles.")
        return

    if session_date:
        target = ARCHIVE_DIR / session_date
        if not target.exists():
            print(f"❌ Sesión {session_date} no encontrada.")
            return
        sessions = [target]
    else:
        print("📦 Sesiones disponibles:")
        for s in sessions:
            manifest_path = s / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path, encoding="utf-8") as f:
                    manifest = json.load(f)
                file_count = len(manifest.get("files", []))
                print(f"  {s.name} → {file_count} archivos")
            else:
                print(f"  {s.name}")
        return

    for session_path in sessions:
        manifest_path = session_path / "manifest.json"
        if not manifest_path.exists():
            continue

        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        for file_info in manifest.get("files", []):
            archived = session_path / file_info["archived_as"]
            original = BRAIN_OS_ROOT / file_info["original_path"]

            if archived.exists():
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(archived), str(original))
                print(f"  ✅ Restaurado: {file_info['original_path']}")
            else:
                print(f"  ⚠️  No encontrado: {file_info['archived_as']}")


def print_weekly_report() -> None:
    """Muestra el reporte semanal de limpieza."""
    if not HISTORY_PATH.exists():
        print("📊 Sin historial de limpieza. Ejecuta un escaneo primero.")
        return

    with open(HISTORY_PATH, encoding="utf-8") as f:
        history = json.load(f)

    week_ago = datetime.now() - timedelta(days=7)
    recent = [
        s for s in history.get("sessions", [])
        if datetime.fromisoformat(s["date"]) > week_ago
    ]

    print("\n" + "=" * 50)
    print("📊 REPORTE DE LIMPIEZA SEMANAL")
    print("=" * 50)
    print(f"  Limpiezas esta semana: {len(recent)}")
    print(f"  Espacio recuperado (semana): {sum(s['space_recovered_mb'] for s in recent):.1f} MB")
    print(f"  Espacio recuperado (total): {history.get('total_recovered_mb', 0):.1f} MB")
    print(f"  Última limpieza: {history.get('last_cleanup', 'Nunca')}")

    if ARCHIVE_DIR.exists():
        archive_count = sum(1 for _ in ARCHIVE_DIR.rglob("*") if _.is_file())
        print(f"  Archivos en cleanup_archive/: {archive_count}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Cleanup Manager — Brain OS")
    parser.add_argument("--scan", action="store_true", help="Escanear sin modificar nada")
    parser.add_argument("--clean", action="store_true", help="Ejecutar limpieza")
    parser.add_argument("--level", type=int, choices=[1, 2, 3], default=1, help="Nivel de limpieza")
    parser.add_argument("--restore", nargs="?", const="list", help="Restaurar desde archivo")
    parser.add_argument("--report", action="store_true", help="Reporte semanal")
    args = parser.parse_args()

    if args.report:
        print_weekly_report()
        return

    if args.restore:
        if args.restore == "list":
            restore_from_archive()
        else:
            restore_from_archive(args.restore)
        return

    # Escanear siempre primero
    print("🔍 Escaneando sistema...")
    results = scan_system()

    if args.scan or not args.clean:
        print_scan_report(results)

        # Guardar timestamp del scan en el historial
        history = {"last_scan": None, "last_cleanup": None, "total_recovered_mb": 0, "sessions": []}
        if HISTORY_PATH.exists():
            try:
                with open(HISTORY_PATH, encoding="utf-8") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, KeyError):
                pass
        history["last_scan"] = datetime.now().isoformat()
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return

    if args.clean:
        print(f"\n🧹 Ejecutando limpieza Nivel {args.level}...")
        print("-" * 40)
        session = execute_cleanup(results, args.level)
        save_history(session)

        recovered_mb = session["space_recovered_kb"] / 1024
        print("-" * 40)
        print(f"\n✅ Limpieza completada")
        print(f"   Archivos eliminados: {session['files_removed']}")
        print(f"   Directorios eliminados: {session['dirs_removed']}")
        print(f"   Espacio recuperado: {recovered_mb:.1f} MB")
        if session["archived_files"]:
            print(f"   Archivos archivados: {len(session['archived_files'])} (en cleanup_archive/)")
        if session["errors"]:
            print(f"   ⚠️  Errores: {len(session['errors'])}")
            for err in session["errors"][:5]:
                print(f"      {err}")


if __name__ == "__main__":
    main()
