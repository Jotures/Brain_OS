#!/usr/bin/env python3
"""
Create a new NotebookLM notebook via browser automation.

Two modes:
  - Automatic: Navigates to NotebookLM, clicks "New Notebook", 
               renames it, and returns the URL.
  - Fallback:  Opens NotebookLM visible, user creates the notebook 
               manually, script detects the new URL automatically.
"""

import argparse
import sys
import time
import re
from pathlib import Path

from patchright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import BrowserFactory, StealthUtils
from config import PAGE_LOAD_TIMEOUT


NOTEBOOKLM_HOME = "https://notebooklm.google.com/"
# Regex to capture a notebook URL once it loads
NOTEBOOK_URL_PATTERN = re.compile(
    r"^https://notebooklm\.google\.com/notebook/([a-f0-9\-]+)"
)


def create_notebook(name: str, headless: bool = True) -> str | None:
    """
    Create a new NotebookLM notebook.

    Args:
        name: Display name for the new notebook.
        headless: If True, run browser in headless (automatic) mode.

    Returns:
        The URL of the newly created notebook, or None on failure.
    """
    auth = AuthManager()
    if not auth.is_authenticated():
        print("⚠️ Not authenticated. Run: python scripts/run.py auth_manager.py setup")
        return None

    print(f"📓 Creating notebook: {name}")
    mode_label = "automático" if headless else "manual (browser visible)"
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

        # Wait for page to fully render
        page.wait_for_url(re.compile(r"^https://notebooklm\.google\.com"), timeout=15000)
        time.sleep(2)

        if headless:
            notebook_url = _create_automatic(page, name)
        else:
            notebook_url = _create_with_fallback(page, name)

        if notebook_url:
            print(f"\n  ✅ Notebook created!")
            print(f"  🔗 URL: {notebook_url}")
            return notebook_url
        else:
            print("\n  ❌ Could not capture notebook URL")
            return None

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()

        # If automatic failed, suggest fallback
        if headless:
            print("\n  💡 Try again with --show-browser for manual fallback:")
            print(f'     python scripts/run.py create_notebook.py --name "{name}" --show-browser')
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


def _create_automatic(page, name: str) -> str | None:
    """Automatic mode: click 'New Notebook' and rename it."""

    # Selectors for the "New notebook" / "Create" button (multiple fallbacks)
    new_notebook_selectors = [
        'button:has-text("New notebook")',
        'button:has-text("Nuevo notebook")',
        'button:has-text("Create")',
        'button:has-text("Crear")',
        'button[aria-label="Create new notebook"]',
        'button[aria-label="Crear notebook nuevo"]',
        # Material icon button fallback
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
    return _wait_for_notebook_url(page, name)


def _create_with_fallback(page, name: str) -> str | None:
    """Fallback mode: browser visible, user creates manually, we capture URL."""

    print("\n" + "=" * 50)
    print("  📌 MODO MANUAL: El browser está abierto.")
    print("  📌 Crea un nuevo notebook en NotebookLM.")
    print(f"  📌 Nómbralo: \"{name}\"")
    print("  📌 El script detectará la URL automáticamente.")
    print("=" * 50 + "\n")

    return _wait_for_notebook_url(page, name, timeout_seconds=120)


def _wait_for_notebook_url(page, name: str, timeout_seconds: int = 30) -> str | None:
    """Poll the browser URL until a notebook URL pattern is detected."""

    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        current_url = page.url
        match = NOTEBOOK_URL_PATTERN.match(current_url)
        if match:
            notebook_url = current_url.split("?")[0]  # Strip query params

            # Attempt to rename the notebook
            _try_rename(page, name)
            return notebook_url

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
                # Select all existing text and replace
                page.keyboard.press("Control+A")
                StealthUtils.random_delay(100, 200)
                page.keyboard.type(name, delay=50)
                StealthUtils.random_delay(200, 400)
                page.keyboard.press("Enter")
                print(f"  ✓ Renamed successfully")
                return
        except:
            continue

    print("  ⚠️ Could not rename — you may need to rename manually in NotebookLM")


def main():
    parser = argparse.ArgumentParser(
        description="Create a new NotebookLM notebook"
    )
    parser.add_argument(
        "--name", required=True,
        help="Name for the new notebook (e.g., 'research-pomodoro-2026')"
    )
    parser.add_argument(
        "--show-browser", action="store_true",
        help="Show browser (fallback manual mode)"
    )

    args = parser.parse_args()

    url = create_notebook(
        name=args.name,
        headless=not args.show_browser
    )

    if url:
        # Print clean URL for easy parsing
        print(f"\nNOTEBOOK_URL={url}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
