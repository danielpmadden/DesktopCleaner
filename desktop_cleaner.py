"""High-level utility for automatically categorising desktop files."""

from __future__ import annotations

import datetime
import json
import os
import shutil
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

# Absolute path to the default JSON configuration bundled with the project.
DEFAULT_CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), "config-json.json")

# Fallback configuration used when a custom configuration file is unavailable
# or invalid. Keeping this dictionary in the source ensures the script always
# has a sane set of categories to work with.
DEFAULT_CATEGORIES: Dict[str, List[str]] = {
    "Documents": [
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
        ".rtf",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".odt",
    ],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".msi"],
    "Code": [
        ".py",
        ".js",
        ".html",
        ".css",
        ".java",
        ".c",
        ".cpp",
        ".php",
        ".rb",
        ".go",
    ],
    "Shortcuts": [".lnk"],
    "Others": [],
}


def get_desktop_path() -> str:
    """Return the absolute path to the user's desktop directory.

    The function relies on :func:`os.path.expanduser` to resolve the home
    directory, making it portable across Windows, macOS, and Linux. No
    additional environment checks are required because the "Desktop"
    directory is a conventional sub-directory for all major operating systems.
    """

    # Compose the desktop path by joining the user's home directory with the
    # Desktop folder name. This will work even if the home directory uses a
    # different drive letter on Windows (e.g., ``C:\Users\Alice``).
    return os.path.join(os.path.expanduser("~"), "Desktop")


def load_config(config_path: Optional[str] = None) -> Dict[str, List[str]]:
    """Load file categorisation rules from JSON.

    Parameters
    ----------
    config_path:
        Optional path to a JSON file that describes the available categories.
        When ``None`` (the default), the loader attempts to read the bundled
        ``config-json.json`` file before falling back to :data:`DEFAULT_CATEGORIES`.

    Returns
    -------
    Dict[str, List[str]]
        Mapping of category names to a list of recognised file extensions.

    Notes
    -----
    * The loader validates that the JSON structure is a mapping of strings to
      iterables of strings. Any other structure results in falling back to the
      default configuration.
    * All extensions are normalised to lower-case to simplify lookups.
    """

    # Decide which configuration file to read. ``config_path`` takes priority,
    # otherwise we fall back to the default bundle path. The file may still not
    # exist, so we must guard the read operation.
    candidate_path: str = config_path or DEFAULT_CONFIG_PATH

    try:
        with open(candidate_path, "r", encoding="utf-8") as config_file:
            loaded_config: MutableMapping[str, Iterable[str]] = json.load(config_file)

        # Normalise the loaded JSON into the expected format while validating
        # the contents. If the structure is invalid an exception is raised and
        # handled by the ``except`` block below.
        normalised_config: Dict[str, List[str]] = {}
        for category, extensions in loaded_config.items():
            if not isinstance(category, str):
                raise TypeError("Category names must be strings")
            if not isinstance(extensions, Iterable):
                raise TypeError("Extensions must be provided as an iterable")

            # Only keep string extensions and ensure they are lower-case with a
            # leading dot so lookups are consistent.
            normalised_extensions = [
                ext.lower() if ext.startswith(".") else f".{ext.lower()}"
                for ext in extensions
                if isinstance(ext, str)
            ]
            normalised_config[category] = normalised_extensions

        # Guarantee that the catch-all "Others" category exists to avoid key
        # errors later on when categorising files.
        normalised_config.setdefault("Others", [])
        return normalised_config

    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError) as exc:
        # Provide a descriptive debug message so users understand why the
        # fallback configuration is being used.
        print(
            "⚠️  Configuration file could not be loaded. Using default categories instead."
        )
        print(f"   Reason: {exc}")
        return DEFAULT_CATEGORIES.copy()


def ensure_folders_exist(base_path: str, categories: Mapping[str, Iterable[str]]) -> None:
    """Create category directories inside ``base_path`` when necessary.

    Parameters
    ----------
    base_path:
        Root directory that should contain the category sub-folders.
    categories:
        Mapping of category names to file extensions. Only the keys are used,
        therefore passing the full configuration is convenient.
    """

    for category in categories.keys():
        category_path = os.path.join(base_path, category)
        if not os.path.exists(category_path):
            # ``exist_ok`` is intentionally avoided so that we can provide a
            # single place to add logging or permissions handling later on.
            os.makedirs(category_path)


def categorize_file(file_name: str, categories: Mapping[str, Iterable[str]]) -> str:
    """Return the category name for ``file_name`` based on its extension.

    Parameters
    ----------
    file_name:
        Name of the file (not the full path). The extension is extracted with
        :func:`os.path.splitext` so the function can be used on any directory.
    categories:
        Mapping that associates category names with their recognised extensions.

    Returns
    -------
    str
        The category that best matches ``file_name``. When no explicit mapping
        exists the catch-all ``"Others"`` category is returned.
    """

    file_ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in categories.items():
        if file_ext in extensions:
            return category
    return "Others"


def move_file(file_path: str, destination_folder: str, *, dry_run: bool = False) -> bool:
    """Move a file into ``destination_folder`` while optionally simulating the move.

    Parameters
    ----------
    file_path:
        Full path to the file that should be relocated.
    destination_folder:
        Directory where the file should be stored after the move.
    dry_run:
        When ``True`` the function skips the actual move but still reports
        success. This is useful when previewing changes or running tests.

    Returns
    -------
    bool
        ``True`` on success, ``False`` when an exception prevents the move.
    """

    # Short-circuit the move when executing in dry-run mode. This reduces the
    # complexity for callers that only want to verify behaviour.
    if dry_run:
        return True

    try:
        shutil.move(file_path, destination_folder)
        return True
    except Exception as exc:  # pragma: no cover - logging path only
        print(f"❌ Error moving {file_path}: {exc}")
        return False


def cleanup_desktop(
    base_path: str,
    *,
    config_path: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, List[Dict[str, object]]]:
    """Organise files inside ``base_path`` according to the configured categories.

    Parameters
    ----------
    base_path:
        Directory that should be scanned. In most scenarios this will be the
        user's desktop, but the function accepts any path for flexibility and
        to facilitate testing.
    config_path:
        Optional path to a custom configuration file. When omitted the default
        bundled configuration is used.
    dry_run:
        When ``True`` the function collects metadata and writes the log file
        without moving files. This is valuable for validating configuration
        changes prior to performing the actual cleanup.

    Returns
    -------
    Dict[str, List[Dict[str, object]]]
        A dictionary mirroring the log file structure with the timestamp and
        per-file processing metadata. Returning the log makes it easy to
        integrate this function into other automation scripts.
    """

    # Load the configuration from disk (or fallback) and ensure all destination
    # directories exist before any file is processed.
    categories = load_config(config_path)
    ensure_folders_exist(base_path, categories)

    log_entries = []

    for file_name in os.listdir(base_path):
        file_path = os.path.join(base_path, file_name)

        # Ignore directories and the log file itself to avoid recursive moves.
        if os.path.isdir(file_path) or file_name == "desktop_cleanup_log.json":
            continue

        # Skip hidden files (prefixed with a dot) so that user configuration
        # files are not unintentionally relocated.
        if file_name.startswith("."):
            continue

        category = categorize_file(file_name, categories)

        # Shortcuts are intentionally ignored because users typically keep them
        # on the desktop for quick access.
        if category == "Shortcuts":
            continue

        destination_folder = os.path.join(base_path, category)
        success = move_file(file_path, destination_folder, dry_run=dry_run)

        log_entries.append(
            {
                "file": file_name,
                "category": category,
                "success": success,
            }
        )

    log_payload = {
        "timestamp": datetime.datetime.now().isoformat(),
        "files": log_entries,
    }

    log_file_path = os.path.join(base_path, "desktop_cleanup_log.json")
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        json.dump(log_payload, log_file, indent=4)

    print("✅ Desktop Cleanup Complete!")
    print(f"📄 Log file saved at: {log_file_path}")
    print(f"🔄 {len(log_entries)} files were processed.")

    return log_payload


if __name__ == "__main__":
    cleanup_desktop(get_desktop_path())
