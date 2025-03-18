import os
import shutil
import datetime
import json
from typing import Dict, List

def get_desktop_path() -> str:
    """
    Retrieves the path to the user's Desktop directory.
    Works cross-platform for Windows, macOS, and Linux.

    Returns:
        str: The absolute path to the Desktop folder.
    """
    return os.path.join(os.path.expanduser("~"), "Desktop")

def get_file_categories() -> Dict[str, List[str]]:
    """
    Defines file categories and their corresponding extensions.
    This dictionary helps determine where each file should be placed.

    Returns:
        Dict[str, List[str]]: A mapping of folder names to file extensions.
    """
    return {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
        "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Executables": [".exe", ".msi"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php", ".rb", ".go"],
        "Shortcuts": [".lnk"],  # Shortcuts remain on the desktop (not moved)
        "Others": []  # Files with unknown extensions will go here
    }

def ensure_folders_exist(base_path: str, categories: Dict[str, List[str]]):
    """
    Ensures that all necessary category folders exist in the target directory.
    If a category folder does not exist, it is created.

    Args:
        base_path (str): The path where category folders should be created.
        categories (Dict[str, List[str]]): The dictionary of file categories.
    """
    for category in categories.keys():
        category_path = os.path.join(base_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)  # Create the folder if it does not exist

def categorize_file(file_name: str, categories: Dict[str, List[str]]) -> str:
    """
    Determines the appropriate category for a given file based on its extension.

    Args:
        file_name (str): The name of the file to be categorized.
        categories (Dict[str, List[str]]): The dictionary mapping categories to extensions.

    Returns:
        str: The category name the file belongs to.
    """
    file_ext = os.path.splitext(file_name)[1].lower()  # Extract and normalize file extension
    for category, extensions in categories.items():
        if file_ext in extensions:
            return category  # Return the matching category
    return "Others"  # Default to "Others" if no match is found

def move_file(file_path: str, destination_folder: str) -> bool:
    """
    Moves a file to the specified destination folder, handling errors gracefully.

    Args:
        file_path (str): The full path to the file being moved.
        destination_folder (str): The folder where the file should be placed.

    Returns:
        bool: True if the file was moved successfully, False if an error occurred.
    """
    try:
        shutil.move(file_path, destination_folder)  # Move file to the categorized folder
        return True  # Success
    except Exception as e:
        print(f"❌ Error moving {file_path}: {e}")  # Log error
        return False  # Failure

def cleanup_desktop(base_path: str):
    """
    Scans the target directory, categorizes files, moves them to their corresponding folders,
    and logs the process to a JSON file.

    Args:
        base_path (str): The directory to organize (e.g., Desktop).
    """
    categories = get_file_categories()  # Retrieve file category definitions
    ensure_folders_exist(base_path, categories)  # Ensure category folders exist

    log_entries = []  # List to store details of moved files

    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path, file_name)

        # Skip directories (we only want to move files)
        if os.path.isdir(file_path):
            continue

        # Determine the appropriate category for the file
        category = categorize_file(file_name, categories)

        # Skip shortcut files (e.g., .lnk files) as they should remain on the desktop
        if category == "Shortcuts":
            continue

        # Define the target destination for the file
        destination_folder = os.path.join(base_path, category)

        # Attempt to move the file and record the success/failure
        success = move_file(file_path, destination_folder)

        # Log the operation for record-keeping
        log_entries.append({"file": file_name, "category": category, "success": success})

    # Save log entries to a JSON file for detailed tracking
    log_file_path = os.path.join(base_path, "desktop_cleanup_log.json")
    with open(log_file_path, "w") as log_file:
        json.dump({"timestamp": str(datetime.datetime.now()), "files": log_entries}, log_file, indent=4)

    # Print summary to the console
    print("✅ Desktop Cleanup Complete!")
    print(f"📄 Log file saved at: {log_file_path}")
    print(f"🔄 {len(log_entries)} files were processed.")

# Ensure script runs only when executed directly
if __name__ == "__main__":
    cleanup_desktop(get_desktop_path())
