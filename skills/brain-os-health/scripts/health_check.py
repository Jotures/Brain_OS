#!/usr/bin/env python3
"""
Brain OS Health Check — Auditoría automática del sistema.

Ejecuta verificaciones de integridad y genera un reporte con score 0-100.
Registra resultados en config/audit_log.json.

Usage:
    python health_check.py           # Auditoría completa
    python health_check.py --quick   # Solo archivos core + git
"""

import os
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class HealthCheck:
    """Ejecuta auditoría de salud de Brain OS."""

    def __init__(self, brain_os_root: Path):
        self.root = brain_os_root
        self.results: Dict[str, Dict] = {}
        self.score: float = 0
        self.issues: List[str] = []
        self.healthy: List[str] = []
        self.critical: List[str] = []

    # --- Verificación 1: Archivos Core (20%) ---
    def check_core_files(self) -> Tuple[float, List[str]]:
        """Verifica que los archivos esenciales existan y sean legibles."""
        core_files = [
            "brain_config.md",
            "INICIO.md",
            "Flujo_Maestro_BrainOS_v2.md",
            "CHANGELOG.md",
            "config/audit_log.json",
            "config/hemingway_bridge.json",
            "config/notebooklm_registry.json",
            "config/dev_registry.json",
        ]

        found = 0
        issues = []

        for f in core_files:
            path = self.root / f
            if path.exists():
                # Verificar que sea legible y no vacío
                try:
                    size = path.stat().st_size
                    if size < 10:
                        issues.append(f"⚠️ {f} existe pero está casi vacío ({size} bytes)")
                    else:
                        found += 1
                except OSError:
                    issues.append(f"🔴 {f} existe pero no es legible")
            else:
                issues.append(f"⚠️ {f} no encontrado")

        score = (found / len(core_files)) * 100
        return score, issues

    # --- Verificación 2: Skills Health (20%) ---
    def check_skills(self) -> Tuple[float, List[str]]:
        """Verifica integridad de las skills."""
        skills_dir = self.root / "skills"
        issues = []
        total_skills = 0
        valid_skills = 0
        ghost_skills = []

        if not skills_dir.exists():
            return 0, ["🔴 Directorio skills/ no encontrado"]

        # Archivos alias conocidos (punteros a *-official)
        alias_files = {"docx", "pptx", "xlsx"}

        for item in skills_dir.iterdir():
            if item.name.startswith(".") or item.name.startswith("_"):
                continue

            # Ignorar alias conocidos
            if item.name in alias_files and item.is_file():
                continue

            if item.is_dir():
                total_skills += 1
                skill_md = item / "SKILL.md"
                if skill_md.exists():
                    valid_skills += 1
                else:
                    # Verificar si tiene al menos algún archivo .md
                    md_files = list(item.glob("*.md"))
                    if md_files:
                        valid_skills += 1
                    else:
                        ghost_skills.append(item.name)

        if ghost_skills:
            issues.append(f"⚠️ Skills sin SKILL.md: {', '.join(ghost_skills[:5])}")

        score = (valid_skills / max(total_skills, 1)) * 100
        return score, issues

    # --- Verificación 3: Config Válida (15%) ---
    def check_config(self) -> Tuple[float, List[str]]:
        """Verifica que brain_config.md tenga la info necesaria."""
        config_path = self.root / "brain_config.md"
        issues = []
        checks_passed = 0
        total_checks = 4

        if not config_path.exists():
            return 0, ["🔴 brain_config.md no encontrado"]

        try:
            content = config_path.read_text(encoding="utf-8")
        except Exception:
            return 0, ["🔴 brain_config.md no es legible"]

        # Check 1: IDs de BD principales
        if "BD_TAREAS_MAESTRAS" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ ID de BD_TAREAS_MAESTRAS no encontrado")

        # Check 2: IDs de cursos
        if "CURSO_ECONOMIA_AMBIENTAL" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ IDs de cursos no encontrados")

        # Check 3: Config de NotebookLM
        if "NOTEBOOK_" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ Config de NotebookLM no encontrada")

        # Check 4: Config de Pomodoro
        if "POMODORO_TOOL" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ Config de Pomodoro no encontrada")

        score = (checks_passed / total_checks) * 100
        return score, issues

    # --- Verificación 4: Workflows (15%) ---
    def check_workflows(self) -> Tuple[float, List[str]]:
        """Verifica integridad de los workflows."""
        workflows_dir = self.root / ".agent" / "workflows"
        issues = []
        total = 0
        valid = 0

        if not workflows_dir.exists():
            return 0, ["🔴 Directorio .agent/workflows/ no encontrado"]

        for wf in workflows_dir.glob("*.md"):
            total += 1
            try:
                content = wf.read_text(encoding="utf-8")
                # Verificar frontmatter YAML
                if content.startswith("---"):
                    if "description:" in content[:500]:
                        valid += 1
                    else:
                        issues.append(f"⚠️ {wf.name}: frontmatter sin 'description'")
                else:
                    issues.append(f"⚠️ {wf.name}: sin frontmatter YAML")
            except Exception:
                issues.append(f"🔴 {wf.name}: no legible")

        score = (valid / max(total, 1)) * 100
        return score, issues

    # --- Verificación 5: Dashboard (15%) ---
    def check_dashboard(self) -> Tuple[float, List[str]]:
        """Verifica que INICIO.md esté actualizado."""
        inicio_path = self.root / "INICIO.md"
        issues = []
        checks_passed = 0
        total_checks = 3

        if not inicio_path.exists():
            return 0, ["🔴 INICIO.md no encontrado"]

        try:
            content = inicio_path.read_text(encoding="utf-8")
        except Exception:
            return 0, ["🔴 INICIO.md no legible"]

        # Check 1: Tiene sección de desarrollo
        if "DESARROLLO DEL SISTEMA" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ Falta sección de Desarrollo del Sistema")

        # Check 2: Tiene comandos listados
        if "brain-os-dev" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ Comandos de desarrollo no registrados")

        # Check 3: Tiene estado actual
        if "ESTADO ACTUAL" in content:
            checks_passed += 1
        else:
            issues.append("⚠️ Falta sección de Estado Actual")

        score = (checks_passed / total_checks) * 100
        return score, issues

    # --- Verificación 6: Git Status (15%) ---
    def check_git(self) -> Tuple[float, List[str]]:
        """Verifica estado de Git."""
        issues = []

        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=str(self.root),
            )

            if result.returncode != 0:
                return 50, ["⚠️ Git no disponible o no es un repo"]

            uncommitted = result.stdout.strip()
            if uncommitted:
                lines = uncommitted.split("\n")
                count = len(lines)
                issues.append(f"⚠️ {count} archivo(s) sin commitear")
                return 50, issues

            return 100, []

        except FileNotFoundError:
            return 50, ["⚠️ Git no instalado"]
        except Exception as e:
            return 50, [f"⚠️ Error al verificar Git: {e}"]

    # --- Ejecutar Auditoría Completa ---
    def run(self, quick: bool = False) -> Dict:
        """Ejecuta todas las verificaciones y calcula el score."""
        # Pesos de cada categoría
        weights = {
            "core_files": 20,
            "skills": 20,
            "config": 15,
            "workflows": 15,
            "dashboard": 15,
            "git": 15,
        }

        checks = {
            "core_files": self.check_core_files,
            "skills": self.check_skills,
            "config": self.check_config,
            "workflows": self.check_workflows,
            "dashboard": self.check_dashboard,
            "git": self.check_git,
        }

        if quick:
            # Solo core + git
            checks = {k: v for k, v in checks.items() if k in ("core_files", "git")}
            weights = {"core_files": 60, "git": 40}

        total_score = 0

        for name, check_fn in checks.items():
            score, issues = check_fn()
            self.results[name] = {"score": score, "issues": issues}

            weighted = score * (weights[name] / 100)
            total_score += weighted

            if score == 100:
                self.healthy.append(name)
            elif score >= 70:
                self.issues.extend(issues)
            else:
                self.critical.extend(issues)

        self.score = round(total_score, 1)
        return self.generate_report()

    def generate_report(self) -> Dict:
        """Genera el reporte de salud."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        report = {
            "date": now,
            "score": self.score,
            "results": self.results,
            "healthy": self.healthy,
            "warnings": self.issues,
            "critical": self.critical,
        }

        # Imprimir reporte visual
        print(f"\n🔍 AUDITORÍA BRAIN OS — {now}")
        print(f"\n📊 Score General: {self.score}/100")

        if self.healthy:
            print("\n✅ Saludable:")
            for h in self.healthy:
                print(f"   - {h}: OK")

        if self.issues:
            print("\n⚠️ Atención:")
            for w in self.issues:
                print(f"   - {w}")

        if self.critical:
            print("\n🔴 Crítico:")
            for c in self.critical:
                print(f"   - {c}")

        # Acciones recomendadas
        actions = []
        if self.critical:
            actions.append("Resolver problemas críticos primero")
        if any("sin commitear" in w for w in self.issues):
            actions.append("Hacer git commit de los cambios pendientes")
        if any("sin SKILL.md" in w for w in self.issues):
            actions.append("Revisar skills sin SKILL.md (usar /brain-os-upgrade)")
        if not actions:
            actions.append("Sistema saludable — seguir con el plan")

        print("\n📋 Acciones Recomendadas:")
        for i, a in enumerate(actions, 1):
            print(f"   {i}. {a}")

        return report

    def save_audit_log(self, report: Dict) -> None:
        """Registra resultados en config/audit_log.json."""
        log_path = self.root / "config" / "audit_log.json"

        try:
            if log_path.exists():
                with open(log_path, "r", encoding="utf-8") as f:
                    log = json.load(f)
            else:
                log = {"audits": []}
        except (json.JSONDecodeError, Exception):
            log = {"audits": []}

        # Agregar nueva entrada
        entry = {
            "date": report["date"],
            "score": report["score"],
            "healthy_count": len(report["healthy"]),
            "warnings_count": len(report["warnings"]),
            "critical_count": len(report["critical"]),
        }
        log["audits"].append(entry)

        # Mantener solo las últimas 20 auditorías
        log["audits"] = log["audits"][-20:]

        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)

        print(f"\n📝 Registrado en config/audit_log.json")


def main():
    parser = argparse.ArgumentParser(description="Brain OS Health Check")
    parser.add_argument("--quick", action="store_true", help="Auditoría rápida (solo core + git)")
    args = parser.parse_args()

    # Encontrar raíz de Brain OS
    script_dir = Path(__file__).parent
    brain_os_root = script_dir.parent.parent.parent

    checker = HealthCheck(brain_os_root)
    report = checker.run(quick=args.quick)
    checker.save_audit_log(report)


if __name__ == "__main__":
    main()
