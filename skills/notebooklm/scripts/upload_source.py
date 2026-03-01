import sys
import os
import time
from pathlib import Path
from patchright.sync_api import sync_playwright

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import StealthUtils, BrowserFactory

def upload_file(notebook_url, file_path):
    print(f"🚀 Starting upload process...")
    print(f"📂 File: {file_path}")
    print(f"📓 Notebook: {notebook_url}")

    with sync_playwright() as p:
        auth = AuthManager() # No args
        if not auth.is_authenticated():
            print("❌ Not authenticated. Please run auth_manager.py setup first.")
            return

        # Use BrowserFactory to get the persistent context
        context = BrowserFactory.launch_persistent_context(p, headless=True)
        page = context.new_page()
        stealth = StealthUtils()

        try:
            # Navigate to notebook
            print("🌐 Navigating to NotebookLM...")
            page.goto(notebook_url, wait_until="domcontentloaded", timeout=60000)
            
            print("⏳ Waiting for page load...")
            page.wait_for_selector("body", state="visible")
            time.sleep(6) # Wait for app hydration
            
            print("🔍 Opening 'Add Sources' modal...")
            import re
            
            clicked = False
            try:
                # Find all elements with matching text
                elements = page.get_by_text(re.compile(r"agregar fuentes?|add sources?", re.I)).all()
                for el in elements:
                    if el.is_visible():
                        el.click()
                        clicked = True
                        print("🖱️ Clicked add sources button!")
                        break
            except Exception as e:
                print(f"⚠️ Error iterating elements: {e}")
                
            if not clicked:
                print("⚠️ Fallback: Trying to force click...")
                try:
                    page.get_by_text(re.compile(r"agregar fuentes?|add sources?", re.I)).first.click(force=True)
                except Exception as e:
                    print(f"⚠️ Force click failed: {e}")

            time.sleep(4) # wait for modal animation
            
            print("📥 Looking for 'Subir archivos' button...")
            upload_clicked = False
            try:
                # 2. Click 'Subir archivos' and intercept the file chooser
                elements = page.get_by_text(re.compile(r"subir archivos?|upload files?", re.I)).all()
                for el in elements:
                    if el.is_visible():
                        with page.expect_file_chooser(timeout=15000) as fc_info:
                            el.click()
                        file_chooser = fc_info.value
                        file_chooser.set_files(file_path)
                        print("✅ File uploaded via UI standard file chooser.")
                        upload_clicked = True
                        break
            except Exception as e:
                print(f"⚠️ Error in upload UI interaction: {e}")
                
            if not upload_clicked:
                print("⚠️ UI upload button not visible, falling back to hidden input...")
                page.locator("input[type='file']").first.set_input_files(file_path)
                print("✅ File injected via fallback locator")
            
            # Wait for upload to complete
            # We look for a progress indicator or the file name appearing in the list
            print("⏳ Waiting for upload to process (20s)...")
            time.sleep(20) 
            
            # Optional: Check if file name appears in page text
            filename = os.path.basename(file_path)
            if page.get_by_text(filename, exact=False).is_visible():
                print(f"✅ Success: '{filename}' found in source list!")
            else:
                print("⚠️ Warning: Could not verify if file appeared in list, but upload command was sent.")

        except Exception as e:
            print(f"❌ Error during upload: {e}")
            page.screenshot(path="debug_upload_error.png")
        finally:
            context.close()
            print("🔒 Context closed")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_source.py <notebook_url> <file_path>")
        sys.exit(1)
    
    upload_file(sys.argv[1], sys.argv[2])
