"""DesktopCleaner core module.

This module provides utilities for organizing files within a target directory.
It supports configurable file categories loaded from JSON configuration files and
exposes a simple CLI with dry-run support so users can review changes before
moving any files.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
from pathlib import Path
from typing import Dict, Iterable, List, MutableMapping, Optional

# Default categorisation rules used when no configuration file is supplied. The
# "Shortcuts" category is treated specially and is never moved – these files are
# left untouched on the desktop but still appear in the run log.
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
        ".csv",
        ".md",
    ],
    "Images": [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".tiff",
        ".webp",
        ".ico",
        ".raw",
    ],
    "Videos": [
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".flv",
        ".wmv",
        ".webm",
        ".m4v",
        ".3gp",
    ],
    "Audio": [
        ".mp3",
        ".wav",
        ".aac",
        ".ogg",
        ".flac",
        ".m4a",
        ".wma",
    ],
    "Archives": [
        ".zip",
        ".rar",
        ".tar",
        ".gz",
        ".7z",
        ".bz2",
        ".xz",
        ".iso",
    ],
    "Executables": [
        ".exe",
        ".msi",
        ".app",
        ".bat",
        ".sh",
        ".com",
        ".cmd",
    ],
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
        ".ts",
        ".swift",
        ".json",
        ".xml",
        ".sql",
        ".yml",
        ".yaml",
    ],
    "Shortcuts": [".lnk", ".url", ".desktop"],
    "Others": [],
}


def get_desktop_path() -> Path:
    """Return the current user's Desktop directory."""

    return Path.home() / "Desktop"


def _normalise_extension(ext: str) -> str:
    """Ensure extensions start with a leading dot and are lower case."""

    ext = ext.strip()
    if not ext:
        return ""
    if not ext.startswith("."):
        ext = f".{ext}"
    return ext.lower()


def load_config(config_path: Optional[Path]) -> Dict[str, List[str]]:
    """Load categorisation rules from *config_path*.

    The configuration must be a JSON object mapping category names to iterables
    of file extensions.  Extensions are normalised to lower-case and are stored
    with a leading dot to match :func:`pathlib.Path.suffix` behaviour.

    Args:
        config_path: Path to a JSON file. ``None`` falls back to
            :data:`DEFAULT_CATEGORIES`.

    Returns:
        A dictionary mapping category name to a list of extensions.

    Raises:
        ValueError: If the configuration file cannot be parsed into the expected
            structure.
    """

    if config_path is None:
        return {k: list(v) for k, v in DEFAULT_CATEGORIES.items()}

    try:
        with Path(config_path).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:  # pragma: no cover - simple passthrough
        raise ValueError(f"Configuration file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON configuration: {exc}") from exc

    if not isinstance(data, MutableMapping):
        raise ValueError("Configuration must be an object mapping categories to extensions")

    normalised: Dict[str, List[str]] = {}
    for category, extensions in data.items():
        if not isinstance(category, str):
            raise ValueError("Category names must be strings")
        if not isinstance(extensions, Iterable) or isinstance(extensions, (str, bytes)):
            raise ValueError(f"Extensions for '{category}' must be a list of strings")

        cleaned: List[str] = []
        for ext in extensions:
            if not isinstance(ext, str):
                raise ValueError(f"Extension {ext!r} in category '{category}' is not a string")
            normalised_ext = _normalise_extension(ext)
            if normalised_ext:
                cleaned.append(normalised_ext)
        normalised[category] = cleaned

    # Ensure an "Others" bucket exists so unknown extensions have a destination.
    normalised.setdefault("Others", [])
    return normalised


def ensure_folders_exist(base_path: Path, categories: Dict[str, List[str]]) -> None:
    """Create folders for each category within *base_path* if required."""

    for category in categories.keys():
        if category == "Shortcuts":
            continue
        target_dir = base_path / category
        target_dir.mkdir(parents=True, exist_ok=True)


def categorise_file(file_name: str, categories: Dict[str, List[str]]) -> str:
    """Return the destination category for *file_name* based on its suffix."""

    suffix = _normalise_extension(Path(file_name).suffix)
    for category, extensions in categories.items():
        if suffix in extensions:
            return category
    return "Others"


def _move_file(source: Path, destination_dir: Path) -> None:
    """Move *source* into *destination_dir* raising errors on failure."""

    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination_dir / source.name))


def cleanup_desktop(
    base_path: Path,
    *,
    categories: Optional[Dict[str, List[str]]] = None,
    dry_run: bool = False,
    log_path: Optional[Path] = None,
) -> Dict[str, object]:
    """Organise files in *base_path* according to *categories*.

    Args:
        base_path: Directory whose immediate files will be organised.
        categories: Mapping of category names to file extensions. Defaults to
            :data:`DEFAULT_CATEGORIES`.
        dry_run: When ``True`` files are not moved and the plan is only logged.
        log_path: Optional explicit log file location. When omitted the log file
            is created inside *base_path* with a timestamped filename.

    Returns:
        A dictionary containing the log path and a list of file operation
        results for further processing or testing.
    """

    base_path = Path(base_path)
    if not base_path.exists():
        raise FileNotFoundError(f"Target path does not exist: {base_path}")
    if not base_path.is_dir():
        raise NotADirectoryError(f"Target path is not a directory: {base_path}")

    category_map = {k: list(v) for k, v in (categories or DEFAULT_CATEGORIES).items()}
    ensure_folders_exist(base_path, category_map)

    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    resolved_log_path = Path(log_path) if log_path else base_path / f"desktop_cleanup_log_{timestamp}.json"

    log_entries = []

    for entry in sorted(base_path.iterdir()):
        if entry.is_dir():
            continue

        category = categorise_file(entry.name, category_map)
        record = {
            "file": entry.name,
            "category": category,
            "moved": False,
            "skipped": False,
            "error": None,
        }

        if category == "Shortcuts":
            record["skipped"] = True
            log_entries.append(record)
            continue

        destination_dir = base_path / category

        if dry_run:
            record["moved"] = True
            record["dry_run"] = True
            log_entries.append(record)
            continue

        try:
            _move_file(entry, destination_dir)
            record["moved"] = True
        except PermissionError as exc:
            record["error"] = f"Permission denied: {exc}"
        except FileNotFoundError as exc:
            record["error"] = f"Missing file: {exc}"
        except shutil.Error as exc:
            record["error"] = f"Move failed: {exc}"
        except Exception as exc:  # pragma: no cover - unexpected but logged for troubleshooting
            record["error"] = f"Unexpected error: {exc}"
        log_entries.append(record)

    log_document = {
        "timestamp": _dt.datetime.now().isoformat(),
        "base_path": str(base_path),
        "dry_run": dry_run,
        "entries": log_entries,
    }

    with resolved_log_path.open("w", encoding="utf-8") as handle:
        json.dump(log_document, handle, indent=2)

    return {"log_path": str(resolved_log_path), "entries": log_entries}


def build_argument_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Organise files on your desktop or any folder.")
    parser.add_argument(
        "--path",
        type=Path,
        default=get_desktop_path(),
        help="Target directory to organise (defaults to the current user's Desktop).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a JSON configuration file describing category to extension mappings.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the operations without moving any files.",
    )
    parser.add_argument(
        "--log",
        type=Path,
        help="Optional log file path. When omitted a timestamped log is created inside the target directory.",
    )
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Entry-point used by ``python -m desktop_cleaner`` and the console script."""

    parser = build_argument_parser()
    args = parser.parse_args(argv)

    try:
        categories = load_config(args.config) if args.config else None
    except ValueError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover - parser.error exits process.

    result = cleanup_desktop(
        args.path,
        categories=categories,
        dry_run=args.dry_run,
        log_path=args.log,
    )

    entries = result["entries"]
    moved = sum(1 for entry in entries if entry.get("moved"))
    skipped = sum(1 for entry in entries if entry.get("skipped"))
    errors = [entry for entry in entries if entry.get("error")]

    print("✅ Desktop cleanup complete")
    print(f"📄 Log file saved at: {result['log_path']}")
    print(f"🔄 Files processed: {len(entries)} (moved: {moved}, skipped: {skipped})")
    if args.dry_run:
        print("ℹ️  Dry-run mode enabled – no files were moved.")
    if errors:
        print("⚠️  Some files could not be moved:")
        for entry in errors:
            print(f"   - {entry['file']}: {entry['error']}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
