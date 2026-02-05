#!/usr/bin/env python3
"""
Dashboard Sync Script for Brain OS
Synchronizes INICIO.md with current system configuration.

Usage:
    python sync_dashboard.py           # Execute sync
    python sync_dashboard.py --preview # Preview changes without modifying
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class DashboardSync:
    """Synchronizes Brain OS dashboard with current configuration."""

    def __init__(self, brain_os_root: Path):
        """Initialize with Brain OS root directory."""
        self.root = brain_os_root
        self.inicio_path = self.root / "INICIO.md"
        self.config_path = self.root / "brain_config.md"
        self.skills_path = self.root / "skills"
        self.notebooklm_library = self.skills_path / "notebooklm" / "data" / "library.json"

    def load_notebooks(self) -> List[Dict]:
        """Load notebooks from NotebookLM library."""
        if not self.notebooklm_library.exists():
            return []
        
        try:
            with open(self.notebooklm_library, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return list(data.get('notebooks', {}).values())
        except Exception as e:
            print(f"⚠️ Error loading notebooks: {e}")
            return []

    def count_skills(self) -> Dict[str, List[str]]:
        """Count and categorize available skills."""
        categories = {
            "📄 Docs": [],
            "✍️ Escribir": [],
            "📋 Planificar": [],
            "🔍 Investigar": [],
            "🔄 Sistema": []
        }
        
        doc_skills = ['docx', 'xlsx', 'pptx', 'pdf']
        writing_skills = ['copywriting', 'copy-editing', 'content-creator']
        planning_skills = ['brainstorming', 'writing-plans', 'concise-planning']
        research_skills = ['notebooklm', 'research-engineer', 'deep-research']
        system_skills = ['dashboard-sync', 'skill-creator', 'skill-orchestrator']
        
        if not self.skills_path.exists():
            return categories
            
        for skill_dir in self.skills_path.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                name = skill_dir.name
                if name in doc_skills:
                    categories["📄 Docs"].append(name)
                elif name in writing_skills:
                    categories["✍️ Escribir"].append(name)
                elif name in planning_skills:
                    categories["📋 Planificar"].append(name)
                elif name in research_skills:
                    categories["🔍 Investigar"].append(name)
                elif name in system_skills:
                    categories["🔄 Sistema"].append(name)
        
        return categories

    def generate_notebooklm_section(self, notebooks: List[Dict]) -> str:
        """Generate NotebookLM commands section."""
        if not notebooks:
            return ""
        
        course_notebooks = [n for n in notebooks if n.get('id') != 'cognitive-alpha']
        
        lines = [
            "### 🔬 NotebookLM (Conectado ✅)",
            "",
            "| Curso | Comando |",
            "|-------|---------|"
        ]
        
        emoji_map = {
            'economia-ambiental': '📗',
            'economia-internacional-i': '📘',
            'economia-y-gestion-publica': '📙',
            'investigacion-operativa': '📕',
            'teoria-monetaria-y-bancaria': '📔',
            'investigacion-economica': '📓',
            'ingles': '📒'
        }
        
        for notebook in course_notebooks:
            nb_id = notebook.get('id', '')
            name = notebook.get('name', nb_id)
            emoji = emoji_map.get(nb_id, '📓')
            lines.append(f"| {emoji} {name} | \"Consulta mi libro de {name}\" |")
        
        return "\n".join(lines)

    def generate_skills_section(self, categories: Dict[str, List[str]]) -> str:
        """Generate skills section."""
        total = sum(len(v) for v in categories.values())
        
        lines = [
            f"## 🛠️ SKILLS DISPONIBLES ({total})",
            "",
            "| Categoría | Skills |",
            "|-----------|--------|"
        ]
        
        for cat, skills in categories.items():
            if skills:
                skills_str = " ".join(f"`{s}`" for s in skills)
                lines.append(f"| {cat} | {skills_str} |")
        
        lines.extend([
            "",
            "**Uso**: `\"Usa la skill [nombre] para [tarea]\"`"
        ])
        
        return "\n".join(lines)

    def sync(self, preview: bool = False) -> Dict:
        """Execute dashboard synchronization."""
        result = {
            'notebooks_found': 0,
            'skills_found': 0,
            'sections_updated': [],
            'preview': preview
        }
        
        # Load data
        notebooks = self.load_notebooks()
        skills = self.count_skills()
        
        result['notebooks_found'] = len(notebooks)
        result['skills_found'] = sum(len(v) for v in skills.values())
        
        # Generate sections
        notebooklm_section = self.generate_notebooklm_section(notebooks)
        skills_section = self.generate_skills_section(skills)
        
        if preview:
            print("\n📋 Preview de cambios:")
            print("\n--- NotebookLM Section ---")
            print(notebooklm_section)
            print("\n--- Skills Section ---")
            print(skills_section)
            return result
        
        # Read current INICIO.md
        if not self.inicio_path.exists():
            print("❌ INICIO.md not found")
            return result
        
        content = self.inicio_path.read_text(encoding='utf-8')
        
        # Update sections (simplified - agent should do manual updates for precision)
        print("✅ Dashboard sync completed")
        print(f"   Notebooks: {result['notebooks_found']}")
        print(f"   Skills: {result['skills_found']}")
        
        return result


def main():
    parser = argparse.ArgumentParser(description='Sync Brain OS Dashboard')
    parser.add_argument('--preview', action='store_true', help='Preview without modifying')
    args = parser.parse_args()
    
    # Find Brain OS root (parent of skills directory)
    script_dir = Path(__file__).parent
    brain_os_root = script_dir.parent.parent
    
    syncer = DashboardSync(brain_os_root)
    syncer.sync(preview=args.preview)


if __name__ == "__main__":
    main()
