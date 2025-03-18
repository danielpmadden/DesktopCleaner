#!/usr/bin/env python3
"""
Desktop Cleanup Tool

Automatically organizes your desktop files into categorized folders
based on file types, making it easier to maintain a clean workspace.
"""

import os
import shutil
import datetime
import json
import argparse
from typing import Dict, List, Optional, Tuple


def get_desktop_path() -> str:
    """Returns the path to the user's desktop."""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def load_config(config_path: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Loads file categories from config.json if it exists, 
    otherwise returns default categories.
    """
    # Default configuration
    default_categories = {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
        "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Executables": [".exe", ".msi"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php", ".rb", ".go"],
        "Shortcuts": [".lnk"],  # These will be skipped
        "Others": []
    }
    
    # If a config path is provided, use it
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Error parsing config file: {config_path}")
            print("Using default categories instead.")
            return default_categories
    
    # Look for config.json in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Error parsing config.json")
            print("Using default categories instead.")
    
    return default_categories


def ensure_folders_exist(base_path: str, categories: Dict[str, List[str]]):
    """Creates necessary folders if they do not exist."""
    for category in categories.keys():
        category_path = os.path.join(base_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            print(f"📁 Created folder: {category}")


def categorize_file(file_name: str, categories: Dict[str, List[str]]) -> str:
    """Determines the category for a given file based on its extension."""
    file_ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in categories.items():
        if file_ext in extensions:
            return category
    return "Others"


def move_file(file_path: str, destination_folder: str, dry_run: bool = False) -> bool:
    """
    Moves a file to the destination folder, handling errors safely.
    In dry-run mode, it only simulates the operation.
    """
    try:
        dest_file_path = os.path.join(destination_folder, os.path.basename(file_path))
        
        # Check if file already exists in destination
        if os.path.exists(dest_file_path):
            base, ext = os.path.splitext(os.path.basename(file_path))
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"{base}_{timestamp}{ext}"
            dest_file_path = os.path.join(destination_folder, new_file_name)
        
        if dry_run:
            print(f"🔍 Would move {file_path} to {dest_file_path}")
            return True
        else:
            shutil.move(file_path, dest_file_path)
            print(f"✅ Moved {os.path.basename(file_path)} to {os.path.basename(destination_folder)}")
            return True
    except Exception as e:
        print(f"❌ Error moving {file_path}: {e}")
        return False


def cleanup_desktop(base_path: str, skip_categories: List[str] = None, dry_run: bool = False):
    """
    Scans, categorizes, moves files, and logs the process.
    
    Args:
        base_path: Path to clean up (usually desktop)
        skip_categories: List of categories to skip
        dry_run: If True, only simulate operations without moving files
    """
    if skip_categories is None:
        skip_categories = []
    
    # Always skip "Shortcuts" category
    if "Shortcuts" not in skip_categories:
        skip_categories.append("Shortcuts")
    
    print(f"🚀 Starting desktop cleanup on: {base_path}")
    if dry_run:
        print("🔍 DRY RUN MODE: No files will be moved")
    
    categories = load_config()
    ensure_folders_exist(base_path, categories)
    
    log_entries = []
    total_files = 0
    moved_files = 0
    
    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path, file_name)
        
        # Skip directories and the log file itself
        if os.path.isdir(file_path) or file_name == "desktop_cleanup_log.json":
            continue
        
        total_files += 1
        
        # Categorize the file
        category = categorize_file(file_name, categories)
        
        # Skip files in specified categories
        if category in skip_categories:
            log_entries.append({
                "file": file_name, 
                "category": category, 
                "success": None,
                "skipped": True,
                "reason": "Category skipped"
            })
            continue
        
        # Move the file
        destination_folder = os.path.join(base_path, category)
        success = move_file(file_path, destination_folder, dry_run)
        
        if success:
            moved_files += 1
        
        # Log the result
        log_entries.append({
            "file": file_name, 
            "category": category, 
            "success": success,
            "skipped": False,
            "timestamp": str(datetime.datetime.now())
        })
    
    # Write structured log file
    log_file_path = os.path.join(base_path, "desktop_cleanup_log.json")
    log_data = {
        "timestamp": str(datetime.datetime.now()),
        "base_path": base_path,
        "dry_run": dry_run,
        "files_processed": total_files,
        "files_moved": moved_files,
        "files": log_entries
    }
    
    if not dry_run:
        with open(log_file_path, "w") as log_file:
            json.dump(log_data, log_file, indent=4)
        print(f"📄 Log file saved at: {log_file_path}")
    
    print(f"✨ Desktop Cleanup Complete!")
    print(f"📊 Summary: {moved_files}/{total_files} files were processed.")


def parse_arguments() -> Tuple[str, List[str], bool, Optional[str]]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Desktop Cleanup Tool")
    parser.add_argument("--path", 
                        help="Path to clean up (defaults to Desktop)")
    parser.add_argument("--skip-categories",
                        help="Comma-separated list of categories to skip")
    parser.add_argument("--dry-run", 
                        action="store_true",
                        help="Simulate cleanup without moving files")
    parser.add_argument("--config",
                        help="Path to custom configuration file")
    
    args = parser.parse_args()
    
    # Set the base path
    base_path = args.path if args.path else get_desktop_path()
    
    # Parse categories to skip
    skip_categories = []
    if args.skip_categories:
        skip_categories = [cat.strip() for cat in args.skip_categories.split(",")]
    
    return base_path, skip_categories, args.dry_run, args.config


def main():
    """Main entry point for the script."""
    base_path, skip_categories, dry_run, config_path = parse_arguments()
    cleanup_desktop(base_path, skip_categories, dry_run)


if __name__ == "__main__":
    main()
