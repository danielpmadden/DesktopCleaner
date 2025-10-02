# Desktop Cleaner

Desktop Cleaner is a pure-Python utility that organises the contents of a
directory (usually your desktop) into category-specific folders. The project is
designed to be easy to customise and offers detailed logging so every action is
traceable.

## Key features

* **Automatic categorisation** – Files are sorted into folders such as
  ``Documents`` or ``Images`` based on file extension.
* **Configurable behaviour** – Category definitions can be adjusted by editing
  ``config-json.json`` or by supplying a custom configuration file at runtime.
* **Dry-run support** – Preview how files would be organised without moving
  them.
* **Comprehensive logging** – Every processed file is captured in
  ``desktop_cleanup_log.json`` alongside a timestamp.
* **Safe defaults** – Hidden files and common desktop shortcuts remain in place
  to avoid disrupting a personalised workspace.

## Installation

Clone this repository and ensure you are using Python 3.9 or newer (the script
relies only on the standard library).

```bash
git clone https://github.com/yourusername/desktop-cleaner.git
cd desktop-cleaner
```

## Usage

### Quick start

Run the module directly to organise your desktop using the bundled
configuration file:

```bash
python desktop_cleaner.py
```

### Programmatic usage

The :func:`desktop_cleaner.cleanup_desktop` function can be imported into other
Python scripts for advanced automation. The example below performs a dry run of
the cleanup routine using a temporary directory.

```python
from pathlib import Path

from desktop_cleaner import cleanup_desktop

temp_path = Path("/tmp/desktop-preview")
temp_path.mkdir(exist_ok=True)

cleanup_desktop(str(temp_path), dry_run=True)
```

### Optional arguments

``cleanup_desktop`` accepts two keyword arguments:

* ``config_path`` – Path to a JSON file describing the category mapping.
* ``dry_run`` – When ``True`` the log file is created but no files are moved.

## Configuration format

Configuration files are JSON documents whose top-level keys correspond to
category folder names. Each value is an array of recognised extensions. The
``Others`` key acts as a catch-all bucket and should remain present.

```json
{
  "Documents": [".pdf", ".docx", ".txt"],
  "Images": [".png", ".jpg"],
  "Others": []
}
```

Any extensions missing the leading dot will be normalised automatically. You
can expand the bundled ``config-json.json`` file or provide an alternative file
using the ``config_path`` argument.

## Development

Run the unit tests to validate changes before submitting a pull request:

```bash
python -m unittest
```

Contributions of all sizes are welcome. Please open an issue if you plan to add
a significant new feature so we can discuss the approach beforehand.

## License

This project is licensed under the MIT License. See ``LICENSE`` for the full
text.
