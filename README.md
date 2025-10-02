# DesktopCleaner

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/release/python-390/) [![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)](#cross-platform-support) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](#testing)

**DesktopCleaner** is a cross-platform Python utility that keeps your desktop tidy by sorting files into smart, traceable folders in seconds.

---

## Why DesktopCleaner?
- **Taming the chaos:** Desktops become dumping grounds for downloads, screenshots, and temporary files—DesktopCleaner groups them into meaningful folders automatically.
- **Consistent structure:** Rely on extension-to-folder rules so that presentations land in *Documents*, screenshots in *Images*, and installers in *Executables*.
- **Time saver:** Run it manually or schedule it to keep your workspace fresh without any manual dragging.

### Safety first
- **Dry-run mode** simulates every move and prints the planned operations, letting you verify results before a single file is touched.
- **Undo/restore** stores a manifest of moves so you can roll back the last cleanup with a single command.
- **Detailed logs** provide a full audit trail including timestamps, original locations, and destinations.

## Cross-platform support
- **Windows:** Uses `%USERPROFILE%\Desktop` and respects NTFS permissions. UNC paths are supported when mapped drives are available.
- **macOS:** Targets `~/Desktop`, handles `.DS_Store` gracefully, and supports Spotlight metadata preservation.
- **Mixed environments:** Pass `--path` to point at shared desktops (e.g., OneDrive, iCloud) regardless of the host OS.

---

## Installation
DesktopCleaner targets **Python 3.9+** and has no external dependencies.

### Install with `pipx` (recommended)
```bash
pipx install desktopcleaner
```

### Install with `pip`
```bash
python -m pip install --user desktopcleaner
```

> **Tip:** Prefer an isolated environment? Create and activate a virtualenv before installing:
> ```bash
> python -m venv .venv
> source .venv/bin/activate   # macOS
> .venv\\Scripts\\activate     # Windows
> python -m pip install desktopcleaner
> ```

---

## Quickstart
Run DesktopCleaner against your current desktop (auto-detected for Windows and macOS):

```bash
desktopcleaner run
```

Common flags:

```bash
# Preview the actions without touching files
desktopcleaner run --dry-run

# Use a custom rules file (YAML or JSON)
desktopcleaner run --rules ~/.config/desktopcleaner/rules.yaml

# Undo the last cleanup using the generated manifest
desktopcleaner --undo

# Increase verbosity when debugging
desktopcleaner run --log-level DEBUG
```

---

## Rules & Configuration
DesktopCleaner ships with a sensible default mapping. Files are matched by extension (case-insensitive) and moved into the corresponding folder beneath your desktop.

| Folder       | Extensions |
| ------------ | ---------- |
| Documents    | `.pdf`, `.docx`, `.doc`, `.txt`, `.rtf`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.odt` |
| Images       | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.tiff` |
| Videos       | `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv` |
| Audio        | `.mp3`, `.wav`, `.aac`, `.ogg`, `.flac` |
| Archives     | `.zip`, `.rar`, `.tar`, `.gz`, `.7z` |
| Code         | `.py`, `.js`, `.html`, `.css`, `.java`, `.c`, `.cpp`, `.php`, `.rb`, `.go` |
| Executables  | `.exe`, `.msi`, `.pkg`, `.dmg` |
| Shortcuts    | `.lnk`, `.alias` *(left untouched)* |
| Others       | Catch-all for unknown extensions |

### Custom rule files
Store your rules in **YAML** or **JSON**. DesktopCleaner resolves relative paths against the invoking directory.

#### YAML example
```yaml
# ~/.config/desktopcleaner/rules.yaml
Documents:
  - .pdf
  - .md
Screenshots:
  - .png
  - .jpg
Installers:
  - .dmg
  - .pkg
```

#### JSON example
```json
{
  "Documents": [".pdf", ".md"],
  "Screenshots": [".png", ".jpg"],
  "Installers": [".dmg", ".pkg"],
  "Ignore": [".lnk", ".alias"]
}
```

> Use `desktopcleaner validate --rules path/to/rules.yaml` to lint custom mappings before running them.

---

## Scheduling
Automate tidy desktops on both platforms.

### Windows (Task Scheduler)
1. Open **Task Scheduler** → *Create Basic Task...*
2. Name it "DesktopCleaner" and choose the trigger (e.g., daily at 9am).
3. Action: **Start a program**.
   - Program/script: `python`
   - Add arguments: `-m desktopcleaner run`
   - Start in: `%USERPROFILE%`
4. Finish and test via **Run**.

### macOS (`launchd`)
Create `~/Library/LaunchAgents/com.example.desktopcleaner.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.example.desktopcleaner</string>
    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/python3</string>
      <string>-m</string>
      <string>desktopcleaner</string>
      <string>run</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer> <!-- every hour -->
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/desktopcleaner.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/desktopcleaner.err</string>
  </dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.example.desktopcleaner.plist
```

---

## Logging & Undo
- **Log location:** `~/Desktop/.desktopcleaner/logs/<timestamp>.log` (Windows paths use backslashes).
- **Format:** Each line is structured as `TIMESTAMP | LEVEL | ACTION | SOURCE -> DESTINATION`.
- **Undo manifest:** After each successful run, DesktopCleaner writes `~/Desktop/.desktopcleaner/history/<timestamp>.json` capturing moved files. `desktopcleaner --undo` replays the manifest to restore everything to its original place.
- **Partial restores:** Supply `--undo --file foo.pdf` to roll back a single file entry.

Sample log excerpt:
```text
2024-05-20T09:12:14 INFO MOVE "~/Desktop/screenshot-1.png" -> "~/Desktop/Images/screenshot-1.png"
2024-05-20T09:12:14 INFO SKIP "~/Desktop/Shortcut.lnk" (rule: Shortcuts)
2024-05-20T09:12:15 INFO MOVE "~/Desktop/report.xlsx" -> "~/Desktop/Documents/report.xlsx"
```

---

## Testing
DesktopCleaner ships with `pytest` suites and fixture-based desktop snapshots.

```bash
pytest
```

- Tests simulate Windows & macOS directory structures inside temporary folders.
- Fixtures include sample desktops (`tests/fixtures/desktop_win/`, `tests/fixtures/desktop_mac/`) to verify mappings, dry-runs, and undo manifests.

---

## Known Limitations
- Network-mounted desktops are treated as local paths; ensure connectivity before running.
- Encrypted or locked files cannot be moved and will be reported as warnings.
- Undo only tracks the **most recent** successful run. Keep backups for long-term archival.
- Scheduling examples assume Python is available on `PATH`.

> **Disclaimer:** Always review dry-run output before live runs. DesktopCleaner moves files but never deletes them; still, use version control/backups for critical assets.

---

## Roadmap
- [ ] Interactive TUI for reviewing actions.
- [ ] Rule editor GUI with drag-and-drop.
- [ ] Cloud sync support for shared workspaces.

### Changelog
- **0.3.0** – Added undo manifests and log viewer command.
- **0.2.0** – Introduced custom rules loader and validation.
- **0.1.0** – Initial release with core desktop organization.

---

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/amazing-improvement`.
3. Install dev dependencies: `pip install -e .[dev]`.
4. Run tests: `pytest`.
5. Submit a pull request with context and screenshots when applicable.
6. Be respectful and document behavior changes clearly so reviewers can follow along.

### Development environment
```bash
git clone https://github.com/yourusername/DesktopCleaner.git
cd DesktopCleaner
python -m pip install --upgrade pip
pip install -e .[dev]
```

---

## License
DesktopCleaner is released under the [MIT License](LICENSE).

---

## FAQ
**Does it work on Linux?**  
DesktopCleaner officially targets Windows and macOS desktops. Linux support is experimental—ensure your desktop path is configured via `--path`.

**Can I ignore files without moving them?**  
Yes, add them to the `Ignore` section in your rules or use `--exclude "*.iso"` on the command line.

**How do I preview what will change?**  
Run `desktopcleaner run --dry-run` to print planned moves without touching the filesystem.

**Where are logs stored on Windows?**  
`%USERPROFILE%\Desktop\.desktopcleaner\logs`. Undo manifests live alongside in `history/`.

**Can I integrate this into CI?**  
Absolutely. Combine `desktopcleaner run --dry-run` with CI jobs to enforce naming conventions in shared workspaces.

---

*Repository: https://github.com/yourusername/DesktopCleaner*
