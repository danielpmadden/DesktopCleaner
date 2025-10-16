# DesktopCleaner

DesktopCleaner is a lightweight Python utility that organises the files in a folder (typically your Desktop) into category
sub-directories. It now provides a small but reliable CLI, dry-run safety checks, timestamped JSON logs, and optional rule files
so that documentation and behaviour stay aligned.

## Features
- **Cross-platform path detection** – defaults to the current user's Desktop directory on Windows, macOS, and Linux.
- **Configurable rules** – load extension-to-folder mappings from JSON files such as [`config-json.json`](config-json.json).
- **Dry-run support** – preview which files would be moved without touching the filesystem.
- **Timestamped logs** – every run writes a JSON report describing the actions performed (or planned in dry-run mode).

## Installation
DesktopCleaner targets Python 3.9 or newer and has no third-party dependencies.

Clone the repository and install it in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e .
```

The editable install exposes the `desktop-cleaner` console script. Alternatively you can run the module directly without
installation (`python -m desktop_cleaner`).

## Usage
Organise your Desktop with the default rules:

```bash
desktop-cleaner
```

Preview the actions first:

```bash
desktop-cleaner --dry-run
```

Point to another folder or use a custom configuration file:

```bash
desktop-cleaner --path ~/Downloads --config ~/rules.json
```

By default logs are written to the target directory using the pattern `desktop_cleanup_log_<timestamp>.json`. Provide
`--log` to specify an explicit path.

## Configuration
Rules are expressed as a JSON object that maps category names to lists of file extensions. Extensions are matched
case-insensitively, with or without the leading dot. A minimal example:

```json
{
  "Documents": [".pdf", "docx"],
  "Images": [".png", ".jpg"],
  "Shortcuts": [".lnk"],
  "Others": []
}
```

Any category named `Shortcuts` is skipped instead of being moved, which keeps launchers on the Desktop while still logging them.
Unknown extensions fall back to the `Others` folder.

The repository includes [`config-json.json`](config-json.json) as a ready-to-use rule set.

## Logging
Every run produces a structured JSON log containing the timestamp, target path, dry-run state, and an entry per file. Example:

```json
{
  "timestamp": "2024-05-20T12:00:00",
  "base_path": "/Users/alex/Desktop",
  "dry_run": false,
  "entries": [
    {"file": "report.pdf", "category": "Documents", "moved": true, "skipped": false, "error": null},
    {"file": "launch.desktop", "category": "Shortcuts", "moved": false, "skipped": true, "error": null}
  ]
}
```

## Testing
The project uses the built-in `unittest` framework:

```bash
python -m unittest
```

Tests create temporary directories so they are safe to run locally and in CI environments.

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-improvement`.
3. Install the project with `pip install -e .` and run `python -m unittest` before submitting.
4. Open a pull request with a description of the change and any relevant screenshots or logs.

## License
DesktopCleaner is released under the [MIT License](LICENSE).
