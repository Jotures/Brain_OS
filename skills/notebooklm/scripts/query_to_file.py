import subprocess
import sys
import os
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook-id", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    run_script = script_dir / "run.py"
    ask_script = "ask_question.py"
    
    cmd = [
        sys.executable,
        str(run_script),
        ask_script,
        "--notebook-id", args.notebook_id,
        "--question", args.question
    ]
    
    print(f"🚀 Querying NotebookLM and saving to {args.output}...")
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        # Capture raw bytes to avoid any intermediate decoding issues, then decode as utf-8 manually
        result = subprocess.run(
            cmd,
            capture_output=True,
            env=env
        )
        
        # Decode stdout assuming utf-8 (NotebookLM scripts should output utf-8)
        try:
            output_text = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback for weird cases
            output_text = result.stdout.decode('cp1252', errors='replace')
            
        if result.returncode != 0:
            print(f"❌ Error running query: {result.stderr.decode('utf-8', errors='ignore')}")
            sys.exit(result.returncode)

        # Write to file with explicit utf-8 (with BOM for Windows notepad friendliness if needed, but standard utf-8 is better for Python)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
            
        print(f"✅ Output saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
