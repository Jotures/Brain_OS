
import os
import argparse
import datetime
from pathlib import Path

def create_adr(title, status="Proposed"):
    """
    Creates a new Architecture Decision Record (ADR) file.
    The file is named sequentially (e.g., 001-my-decision.md).
    """

    # --- Configuration ---
    ADR_DIR = Path("docs/adrs")  # Directory to store ADRs (make sure this exists)
    TEMPLATE_FILE = Path("skills/architecture/templates/adr-template.md")

    # --- Ensure directory exists ---
    if not ADR_DIR.exists():
        print(f"Creating directory: {ADR_DIR}")
        ADR_DIR.mkdir(parents=True, exist_ok=True)

    # --- Find next number ---
    existing_files = list(ADR_DIR.glob("*.md"))
    next_number = 1
    if existing_files:
        numbers = []
        for f in existing_files:
            try:
                num_str = f.name.split("-")[0]
                numbers.append(int(num_str))
            except ValueError:
                pass # Ignore files that don't start with a number
        if numbers:
            next_number = max(numbers) + 1

    # --- Format filename ---
    slug = title.lower().replace(" ", "-")
    filename = f"{next_number:03d}-{slug}.md"
    file_path = ADR_DIR / filename

    # --- Generate content ---
    date_str = datetime.date.today().isoformat()
    
    # Try to load template, otherwise use default
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as t:
            content = t.read()
            content = content.replace("{NUMBER}", str(next_number))
            content = content.replace("{TITLE}", title)
            content = content.replace("{DATE}", date_str)
            content = content.replace("{STATUS}", status)
    else:
        # Fallback content if template is missing
        content = f"""# {next_number}. {title}

Date: {date_str}

## Status
{status}

## Context
The issue motivating this decision...

## Decision
The change that we are proposing or have agreed to implement...

## Consequences
What becomes easier or more difficult to do and any risks introduced...
"""

    # --- Write file ---
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ ADR Created: {file_path}")
    return str(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Architecture Decision Record (ADR).")
    parser.add_argument("--title", required=True, help="Title of the decision (e.g., 'Use Supabase for DB')")
    parser.add_argument("--status", default="Proposed", help="Status: Proposed, Accepted, Rejected, Deprecated")
    
    args = parser.parse_args()
    
    create_adr(args.title, args.status)
