# Desktop Cleanup Tool

A Python utility that automatically organizes your desktop files into categorized folders based on file types.

## Features

- Automatically categorizes desktop files by type
- Creates organized folder structure
- Generates detailed JSON logs of all operations
- Skips shortcuts and system folders
- Error handling for safe file operations
- Customizable file categories and extensions

## Installation

Clone this repository to your local machine. 
git clone https://github.com/yourusername/desktop-cleanup-tool.git
cd desktop-cleanup-tool

No external dependencies required! The tool uses only Python standard library modules.

## Usage

### Basic Usage

Run the script to organize your desktop:
python desktop_cleanup.py

### Advanced Usage

You can customize the tool by providing command-line arguments:
python desktop_cleanup.py --path "/custom/path" --dry-run --skip-categories "Videos,Audio"
Copy
Available options:
- `--path`: Specify a custom path instead of desktop
- `--dry-run`: Preview changes without moving files
- `--skip-categories`: Comma-separated list of categories to skip
- `--config`: Path to custom configuration file

## Configuration

The default file categories and extensions are defined in the script, but you can customize them by editing the `config.json` file:

```json

  "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xls", ".xlsx"],
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff"],
  "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
  "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
  "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
  "Executables": [".exe", ".msi"],
  "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php"],
  "Shortcuts": [".lnk"]

```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
