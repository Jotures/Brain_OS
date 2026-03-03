#!/usr/bin/env python3
"""
Create a new NotebookLM notebook.

Three modes:
  1. Automatic (default): Headless browser automation — clicks "New Notebook",
     renames it, captures URL. No user interaction needed.
  2. Manual (--manual): Opens NotebookLM in the USER'S default browser,
     then asks for the URL via stdin. Simple and reliable.
  3. Show-browser (--show-browser): Same as automatic but with the browser
     visible for debugging purposes.
"""

import argparse
import sys
import time
import re
import webbrowser
from pathlib import Path

from patchright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import BrowserFactory, StealthUtils
from config import PAGE_LOAD_TIMEOUT


NOTEBOOKLM_HOME = "https://notebooklm.google.com/"
NOTEBOOK_URL_PATTERN = re.compile(
    r"^https://notebooklm\.google\.com/notebook/([a-f0-9\-]+)"
)


def create_notebook_manual(name: str) -> str | None:
    """
    Manual mode: opens NotebookLM in the user's default browser
    and asks for the URL via stdin.

    Args:
        name: Suggested name for the notebook.

    Returns:
        The URL provided by the user, or None if cancelled.
    """
    print(f"📓 Creating notebook: {name}")
    print(f"   Modo: manual (tu navegador)\n")

    # Open NotebookLM in the user's real browser
    webbrowser.open(NOTEBOOKLM_HOME)

    print("=" * 55)
    print(f"  � Se abrió NotebookLM en tu navegador.")
    print(f"  📌 Crea un nuevo notebook y nómbralo: \"{name}\"")
    print(f"  📌 Luego copia la URL del notebook y pégala abajo.")
    print("=" * 55)

    while True:
        print()
        url_input = input("  🔗 Pega la URL del notebook (o 'cancelar'): ").strip()

        if url_input.lower() in ("cancelar", "cancel", "q", "exit"):
            print("  ❌ Cancelado por el usuario.")
            return None

        match = NOTEBOOK_URL_PATTERN.match(url_input)
        if match:
            notebook_url = url_input.split("?")[0]
            print(f"\n  ✅ Notebook registrado!")
            print(f"  🔗 URL: {notebook_url}")
            return notebook_url
        else:
            print("  ⚠️ URL no válida. Debe ser como:")
            print("     https://notebooklm.google.com/notebook/xxxxxxxx-xxxx-xxxx-xxxx")


def create_notebook_auto(name: str, headless: bool = True) -> str | None:
    """
    Automatic mode: uses Patchright to create the notebook.

    Args:
        name: Display name for the new notebook.
        headless: If True, run browser in headless mode.

    Returns:
        The URL of the newly created notebook, or None on failure.
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        print("⚠️ Not authenticated. Run: python scripts/run.py auth_manager.py setup")
        return None

    print(f"📓 Creating notebook: {name}")
    mode_label = "automático" if headless else "automático (browser visible)"
    print(f"   Modo: {mode_label}")

    playwright = None
    context = None

    try:
        playwright = sync_playwright().start()
        context = BrowserFactory.launch_persistent_context(
            playwright, headless=headless
        )

        page = context.new_page()
        print("  🌐 Opening NotebookLM home...")
        page.goto(NOTEBOOKLM_HOME, wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT)

        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com"), timeout=15000)
        time.sleep(3)

        # Click "New Notebook" button
        new_notebook_selectors = [
            'button:has-text("New notebook")',
            'button:has-text("Nuevo notebook")',
            'button:has-text("Create")',
            'button:has-text("Crear")',
            'button[aria-label="Create new notebook"]',
            'button[aria-label="Crear notebook nuevo"]',
            'button.create-new-notebook-button',
            '[data-test-id="create-notebook-button"]',
        ]

        print("  🔍 Looking for 'New notebook' button...")
        clicked = False

        for selector in new_notebook_selectors:
            try:
                btn = page.wait_for_selector(selector, timeout=5000, state="visible")
                if btn:
                    print(f"  ✓ Found: {selector}")
                    StealthUtils.random_delay(300, 800)
                    btn.click()
                    clicked = True
                    break
            except:
                continue

        if not clicked:
            print("  ❌ Could not find 'New notebook' button")
            return None

        # Wait for navigation to the new notebook
        print("  ⏳ Waiting for new notebook to load...")
        notebook_url = _wait_for_notebook_url(page, timeout_seconds=45)

        if not notebook_url:
            # Sometimes NotebookLM opens the notebook in a new tab
            print("  🔍 Checking other tabs...")
            for p in context.pages:
                match = NOTEBOOK_URL_PATTERN.match(p.url)
                if match:
                    notebook_url = p.url.split("?")[0]
                    page = p  # Switch to that page for renaming
                    break

        if notebook_url:
            _try_rename(page, name)
            print(f"\n  ✅ Notebook created!")
            print(f"  � URL: {notebook_url}")
            return notebook_url
        else:
            print("\n  ❌ Could not capture notebook URL")
            print("  � Use --manual mode instead:")
            print(f'     python scripts/run.py create_notebook.py --name "{name}" --manual')
            return None

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print(f'\n  💡 Use --manual mode: python scripts/run.py create_notebook.py --name "{name}" --manual')
        return None

    finally:
        if context:
            try:
                context.close()
            except:
                pass
        if playwright:
            try:
                playwright.stop()
            except:
                pass


def _wait_for_notebook_url(page, timeout_seconds: int = 30) -> str | None:
    """Poll the browser URL until a notebook URL pattern is detected."""
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        current_url = page.url
        match = NOTEBOOK_URL_PATTERN.match(current_url)
        if match:
            return current_url.split("?")[0]
        time.sleep(1)

    return None


def _try_rename(page, name: str):
    """Attempt to rename the notebook to the desired name."""
    rename_selectors = [
        'input[aria-label="Notebook title"]',
        'input[aria-label="Título del notebook"]',
        'input.notebook-title',
        '[data-test-id="notebook-title-input"]',
        'h1[contenteditable="true"]',
        'div[contenteditable="true"][role="textbox"]',
    ]

    print(f"  ✏️ Renaming to: {name}")
    StealthUtils.random_delay(1000, 2000)

    for selector in rename_selectors:
        try:
            el = page.wait_for_selector(selector, timeout=5000, state="visible")
            if el:
                el.click()
                StealthUtils.random_delay(200, 500)
                page.keyboard.press("Control+A")
                StealthUtils.random_delay(100, 200)
                page.keyboard.type(name, delay=50)
                StealthUtils.random_delay(200, 400)
                page.keyboard.press("Enter")
                print(f"  ✓ Renamed successfully")
                # Wait for backend save
                time.sleep(3)
                return
        except:
            continue

    print("  ⚠️ Could not rename — rename manually in NotebookLM")


def main():
    parser = argparse.ArgumentParser(
        description="Create a new NotebookLM notebook"
    )
    parser.add_argument(
        "--name", required=True,
        help="Name for the new notebook (e.g., 'research-pomodoro-2026')"
    )
    parser.add_argument(
        "--manual", action="store_true",
        help="Manual mode: opens your browser and asks for the URL"
    )
    parser.add_argument(
        "--show-browser", action="store_true",
        help="Show the automated browser (for debugging)"
    )

    args = parser.parse_args()

    if args.manual:
        url = create_notebook_manual(name=args.name)
    else:
        url = create_notebook_auto(
            name=args.name,
            headless=not args.show_browser
        )

    if url:
        print(f"\nNOTEBOOK_URL={url}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
