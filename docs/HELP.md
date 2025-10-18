# Help & Operations Guide

## Quick Start
1. Ensure Python 3.9 or newer is installed.
2. Clone the repository and move into the project directory.
3. Run `python -m desktop_cleaner` to execute the utility.

The script scans the current user's Desktop directory and moves files into category folders such as `Documents`, `Images`, and `Others`.

## Configuration
- Categories and extensions are currently hard-coded in `desktop_cleaner.py`.
- A sample `config-json.json` is included for future configuration support; the code does not yet load it automatically.

## Logs
- Each run writes a timestamped JSON log (for example `desktop_cleanup_log_20240527_101500.json`) inside the target directory.
- Review the most recent file after running the script to confirm which files were moved.

## Troubleshooting
- **Nothing happens**: Ensure files exist on the Desktop and that the script has permission to move them.
- **Permission errors**: Run the script from an account with rights to modify the target directory.
- **Unexpected moves**: Inspect the category mapping in `desktop_cleaner.py` and adjust manually if required.

## Support
For questions or ideas, open an issue or reach out to the maintainer noted in the README.
