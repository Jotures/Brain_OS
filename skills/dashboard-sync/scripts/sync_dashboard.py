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
        self.dev_registry_path = self.root / "config" / "dev_registry.json"
        self.changelog_path = self.root / "CHANGELOG.md"

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
            "🎓 Académico": [],
            "🔄 Sistema": []
        }
        
        doc_skills = ['docx', 'xlsx', 'pptx', 'pdf', 'docx-official', 'pptx-official', 'xlsx-official', 'pdf-official', 'documentation-templates']
        writing_skills = ['copywriting', 'copy-editing', 'content-creator', 'writing-skills', 'doc-coauthoring']
        planning_skills = ['brainstorming', 'writing-plans', 'concise-planning', 'plan-writing', 'executing-plans', 'kaizen']
        research_skills = ['notebooklm', 'research-engineer', 'prompt-engineer', 'prompt-engineering', 'prompt-library', 'deep-research']
        academic_skills = ['aula-virtual', 'library-manager', 'pomodoro']
        system_skills = ['dashboard-sync', 'skill-creator', 'skill-orchestrator', 'system-coordinator', 'notion-template-business']
        
        if not self.skills_path.exists():
            return categories
            
        for skill_dir in self.skills_path.iterdir():
            name = skill_dir.name
            if name in doc_skills:
                categories["📄 Docs"].append(name)
            elif name in writing_skills:
                categories["✍️ Escribir"].append(name)
            elif name in planning_skills:
                categories["📋 Planificar"].append(name)
            elif name in research_skills:
                categories["🔍 Investigar"].append(name)
            elif name in academic_skills:
                categories["🎓 Académico"].append(name)
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

    def generate_dev_section(self) -> str:
        """Generate development status section from dev_registry.json."""
        if not self.dev_registry_path.exists():
            return ""

        try:
            with open(self.dev_registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"\u26a0\ufe0f Error loading dev_registry: {e}")
            return ""

        entries = data.get('entries', [])
        # Últimas 5 entradas, más recientes primero
        recent = entries[-5:][::-1]

        type_emojis = {
            'feat': '\u2728',
            'refactor': '\ud83d\udd04',
            'fix': '\ud83d\udc1b',
            'docs': '\ud83d\udcdd',
            'cleanup': '\ud83e\uddf9'
        }

        lines = [
            "### \u00daltimos Cambios",
            "",
            "| Fecha | Tipo | Descripci\u00f3n |",
            "|-------|------|-------------|"  
        ]

        for entry in recent:
            date = entry.get('date', '')
            change_type = entry.get('type', '')
            desc = entry.get('description', '')
            emoji = type_emojis.get(change_type, '')
            lines.append(f"| {date} | {emoji} `{change_type}` | {desc} |")

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
        dev_section = self.generate_dev_section()
        
        if preview:
            print("\n📋 Preview de cambios:")
            print("\n--- NotebookLM Section ---")
            print(notebooklm_section)
            print("\n--- Skills Section ---")
            print(skills_section)
            print("\n--- Dev Section ---")
            print(dev_section)
            return result
        
        # Read current INICIO.md
        if not self.inicio_path.exists():
            print("❌ INICIO.md not found")
            return result
        
        content = self.inicio_path.read_text(encoding='utf-8')
        original_content = content
        
        # Update Skills Section
        # Regex to find: ## 🛠️ SKILLS DISPONIBLES.*\n(table...)
        # We look for the header and consume until the next H2 (##) or end of string
        skills_pattern = re.compile(r"(## 🛠️ SKILLS DISPONIBLES.*?\n)((\|.*\|\n)+)(\n.*)?", re.MULTILINE)
        
        # Construct new skill section content (Header + Table + Footer)
        # Note: generate_skills_section returns the whole block including header.
        # We need to replace the existing block.
        
        # Simpler approach: Replace from Header until "---" or next section
        section_pattern = r"(## 🛠️ SKILLS DISPONIBLES.*?)(\n---|\Z)"
        match = re.search(section_pattern, content, re.DOTALL)
        if match:
             new_content = self.generate_skills_section(skills) + "\n\n" + match.group(2)
             # Use string replace for safety if unique, or regex replace
             content = content.replace(match.group(1), self.generate_skills_section(skills) + "\n")
             result['sections_updated'].append('Skills')

        # Update NotebookLM Section (Microscope)
        # Header: ### 🔬 NotebookLM (Conectado ✅)
        nb_pattern = r"(### 🔬 NotebookLM \(Conectado ✅\).*?)(\n####|\n###|\Z)"
        match_nb = re.search(nb_pattern, content, re.DOTALL)
        if match_nb:
            # Reconstruct section
            # generate_notebooklm_section returns lines starting with ### ...
            new_nb_section = self.generate_notebooklm_section(notebooks)
            content = content.replace(match_nb.group(1), new_nb_section + "\n")
            result['sections_updated'].append('NotebookLM')

        # Update Status Section (Metrics)
        # ## 📊 ESTADO ACTUAL
        status_pattern = r"(## 📊 ESTADO ACTUAL.*?)(\n---|\Z)"
        match_status = re.search(status_pattern, content, re.DOTALL)
        if match_status:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            total_skills = result['skills_found']
            
            # Update specific lines within the block
            status_block = match_status.group(1)
            status_block = re.sub(r"\| Skills \| \d+ \|", f"| Skills | {total_skills} |", status_block)
            status_block = re.sub(r"\| Última verificación \| .* \|", f"| Última verificación | {current_date} |", status_block)
            
            content = content.replace(match_status.group(1), status_block)
            result['sections_updated'].append('Estado Actual')

        # Update Dev Section (Últimos Cambios)
        dev_pattern = r"(### \u00daltimos Cambios.*?)(\n## |\n---|\.Z)"
        match_dev = re.search(dev_pattern, content, re.DOTALL)
        if match_dev and dev_section:
            content = content.replace(match_dev.group(1), dev_section + "\n")
            result['sections_updated'].append('Desarrollo')

        # Write changes
        if content != original_content:
            self.inicio_path.write_text(content, encoding='utf-8')
            print("✅ Dashboard updated successfully.")
            for sec in result['sections_updated']:
                print(f"   - Updated {sec}")
        else:
            print("✨ No changes needed. Dashboard is up to date.")
            
        return result


def main():
    parser = argparse.ArgumentParser(description='Sync Brain OS Dashboard')
    parser.add_argument('--preview', action='store_true', help='Preview without modifying')
    args = parser.parse_args()
    
    # Find Brain OS root (parent of skills directory)
    script_dir = Path(__file__).parent
    brain_os_root = script_dir.parent.parent.parent
    
    syncer = DashboardSync(brain_os_root)
    syncer.sync(preview=args.preview)


if __name__ == "__main__":
    main()
