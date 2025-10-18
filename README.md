# DesktopCleaner

*A calm desktop organiser for curious tinkerers.*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Lab%20Prototype-yellow) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![CI](https://img.shields.io/badge/CI-Manual-lightgrey)

> 📸 Screenshot placeholder lives at [`docs/screenshots/preview.png.placeholder.txt`](docs/screenshots/preview.png.placeholder.txt). Capture a terminal session locally and keep binaries out of the repo.

## Overview
DesktopCleaner is a single-file Python script that sweeps through your Desktop folder and drops files into simple category directories. It is intentionally lightweight, easy to read, and perfect for experimenting with filesystem automation.

## Features
- Moves files into default buckets such as `Documents`, `Images`, `Archives`, and `Others`.
- Skips files that already live inside category folders to avoid endless nesting.
- Writes a timestamped JSON report describing every move performed during the run.
- Runs on Windows, macOS, and Linux using only the Python standard library.

## Getting Started

### Prerequisites
- Python 3.9 or newer.
- Access to a Desktop directory with files you are comfortable moving.

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -e .
```

The editable install exposes a `desktop-cleaner` console script. Alternatively, run the module directly:

```bash
python -m desktop_cleaner
```

### Usage
Run the script to tidy the Desktop detected for the current user:

```bash
desktop-cleaner
```

Logs are timestamped (for example `desktop_cleanup_log_20240527_101500.json`) and saved inside the target directory by default.

Pass `--dry-run` to preview actions without moving files, `--path` to target another folder, `--config` to load a JSON mapping, and `--log` to choose where the report is written.

## Documentation
- [`docs/HELP.md`](docs/HELP.md) — setup, usage, and troubleshooting notes.
- [`docs/CHANGELOG.md`](docs/CHANGELOG.md) — repository maintenance history.
- [`docs/SECURITY.md`](docs/SECURITY.md) — safe-use guidelines and disclosure policy.
- [`ROADMAP.md`](ROADMAP.md) — future improvements and known gaps.
- [`docs/archive/2023-project-audit-report.md`](docs/archive/2023-project-audit-report.md) — historical audit for reference.

## Development Notes
- No automated tests currently pass; see the roadmap for alignment work.
- A lightweight GitHub Actions workflow (`.github/workflows/lint.yml`) is included to encourage linting and security scanning once dependencies are installed locally.
- The example rules file [`config-json.json`](config-json.json) illustrates how extension mappings might look in a future configurable release.

## Contributing
Suggestions and observations are welcome! File an issue or open a pull request describing your idea.

## Author
**Daniel Madden**  
IT Professional | Technology Enthusiast | Builder of Experiments  
“Not a software engineer — just a guy who loves all things tech.”
