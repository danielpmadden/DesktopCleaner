# DesktopCleaner

DesktopCleaner organises files within a target directory (typically a user desktop) into sensible category folders while recording a timestamped JSON activity log. The project is intentionally lightweight, depends only on the Python standard library, and is suitable for demonstrations of safe filesystem automation workflows.

## Key Features
- Categorises documents, media, archives, executables, code assets, and miscellaneous files based on configurable extension lists.
- Preserves desktop shortcuts in place to avoid breaking workflow entry points.
- Supports a dry-run mode so prospective changes can be reviewed without moving files.
- Emits a detailed JSON log for every run, including skipped files and errors.
- Provides a command-line interface exposed through `python -m desktop_cleaner` or the `desktop-cleaner` console script.

## Installation
DesktopCleaner targets Python 3.9 through 3.13. Create an isolated environment and install the package together with its development tooling when needed:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

For runtime-only usage you may omit the `[dev]` extras suffix.

## Quick Start
Run the utility using the console script or Python module entry point. Both commands organise the current user's desktop by default:

```bash
desktop-cleaner
# or
python -m desktop_cleaner
```

A JSON report named `desktop_cleanup_log_<timestamp>.json` is written alongside the files that were processed unless a custom log path is provided.

## Usage Examples
Tidy a specific folder without moving any files and send the report to a dedicated location:

```bash
desktop-cleaner --path /path/to/folder --dry-run --log /tmp/desktop-cleaner-report.json
```

Load a JSON configuration that overrides the default extension groups:

```bash
desktop-cleaner --config config-json.json
```

The configuration file must contain a mapping of category names to lists of file extensions. Unknown extensions fall back to the `Others` category automatically.

## Troubleshooting and Support
- Ensure the configured target directory exists and is writable. Permission errors are logged per file in the run report.
- When testing on network shares, enable the `--dry-run` option first to confirm connectivity and permissions.
- On Windows systems using PowerShell, activate the virtual environment with `.venv\Scripts\Activate.ps1`.
- If the console script is unavailable after installation, verify that the virtual environment's `bin/` (or `Scripts/`) directory is in your `PATH`.

Questions and contributions can be raised through the issue tracker or pull requests. Please include environment details and a copy of the generated log when reporting bugs.

## Project Layout and Dependency Overview
```
DesktopCleaner
 ├── src/desktop_cleaner/   → core logic and CLI entry points
 ├── tests/                 → unit tests covering configuration, CLI, and file operations
 ├── docs/                  → historical documentation, security notes, and archived audits
 ├── config-json.json       → sample configuration illustrating custom categories
 ├── README.md              → project overview and setup guide
 ├── ROADMAP.md             → forward-looking maintenance plan and audit summary
 └── CHANGELOG.md           → release highlights and repository updates
```

## Testing
Run the automated test suite from an activated virtual environment:

```bash
pytest
```

Static analysis recommendations include `ruff`, `black`, `bandit`, and `pip-audit`, all of which are installed via the development extras group.

## License and Credits
DesktopCleaner is distributed under the MIT License. See `LICENSE` for full terms.

Author: Daniel Madden
