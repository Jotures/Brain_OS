
import os
import argparse
from pathlib import Path

def analyze_directory(path, ignore_dirs=None, max_depth=2):
    """
    Analyzes a directory structure and prints a summary.
    """
    if ignore_dirs is None:
        ignore_dirs = [".git", "__pycache__", "node_modules", ".venv", "backups"]
    
    target_path = Path(path).resolve()
    
    print(f"\n🔍 Analyzing: {target_path}\n")
    
    total_files = 0
    total_dirs = 0
    file_types = {}

    def print_tree(directory, prefix="", level=0):
        nonlocal total_files, total_dirs
        
        if level > max_depth:
            return

        try:
            items = sorted(os.listdir(directory))
        except PermissionError:
            print(f"{prefix}⛔ [Permission Denied]")
            return

        # Separate dirs and files
        dirs = [d for d in items if (directory / d).is_dir() and d not in ignore_dirs]
        files = [f for f in items if (directory / f).is_file()]

        # Print directories
        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1) and (not files)
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}📁 {d}/")
            total_dirs += 1
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(directory / d, new_prefix, level + 1)

        # Print files (only at this level, summarize deeper)
        for i, f in enumerate(files):
            is_last = (i == len(files) - 1)
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}📄 {f}")
            total_files += 1
            
            ext = Path(f).suffix or "no-ext"
            file_types[ext] = file_types.get(ext, 0) + 1

    print_tree(target_path)
    
    print("\n" + "="*30)
    print(f"📊 Summary:")
    print(f"   - Total Files: {total_files}")
    print(f"   - Total Directories: {total_dirs}")
    print("   - File Types:")
    for ext, count in sorted(file_types.items(), key=lambda item: item[1], reverse=True):
        print(f"     • {ext}: {count}")
    print("="*30 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a directory structure.")
    parser.add_argument("path", help="Path to the directory to analyze")
    parser.add_argument("--depth", type=int, default=2, help="Max depth for tree view")
    
    args = parser.parse_args()
    
    analyze_directory(args.path, max_depth=args.depth)
