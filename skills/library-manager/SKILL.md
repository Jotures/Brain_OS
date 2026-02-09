---
name: library-manager
description: Manages the bidirectional sync between local files and Notion 'Library' (BD_RECURSOS). Handles 'Smart Ingest': moving files to correct folders and registering them in Notion.
---

# Library Manager Skill

## Purpose
Acts as the bridge between the physical file system and the Notion 'Library' index.
1. **Ingest**: Moves a file from a temp location (e.g. Downloads) to the standardized course folder structure and logs it in Notion.
2. **Sync**: Checks Notion for files that exist in the index but not locally, and downloads them (future).

## Components
- `scripts/ingest_file.py`: Core logic for moving and registering files.
- `scripts/notion_adapter.py`: Helper to talk to Notion MCP.

## Usage
- "Guarda este archivo en [Curso]"
- "Registra el PDF X en [Curso]"
