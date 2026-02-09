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
            time.sleep(5) # Wait for app hydration
            
            # Find the file input
            # NotebookLM typically has a hidden file input for uploads
            print("🔍 Looking for file input...")
            
            # Strategy: Simply set input files on the first file input found
            # This often works even if the input is hidden
            try:
                # First try to click the "Add Source" button to ensure the input is active/present in DOM
                # Usually a button with specific aria-label or class in the sidebar
                
                # Check for common "Add" buttons
                add_buttons = page.locator("button[aria-label*='Add'], button[aria-label*='Upload'], button[aria-label*='Source']").all()
                clicked = False
                for btn in add_buttons:
                    if btn.is_visible():
                        # Heuristic: verify it's in the sidebar
                        # For now, just try to find the input directly first as it's safer
                        pass

                # Try to interact with the sidebar header to trigger any lazy loading
                page.mouse.move(100, 300) 
            except:
                pass

            # Direct file upload approach
            file_input = page.locator("input[type='file']").first
            
            if not file_input:
               print("⚠️ No file input found immediately. Trying to open 'Add Source' menu...")
               # Try to find the Plus button in the sidebar (Sources)
               # Usually :text("Sources") then sibling button
               page.get_by_text("Sources", exact=False).first.click() 
               time.sleep(1)

            file_input.set_input_files(file_path)
            print("✅ File injected into input field")
            
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
