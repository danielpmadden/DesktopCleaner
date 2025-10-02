### Roadmap

**Correct documentation to reflect current capabilities**
*Why it matters*: Prevents user confusion by aligning README commands and feature descriptions with what the script actually offers today.
*What to test/check*: Proofread updated README for accuracy and run spell/grammar checks; verify links and code snippets render properly in Markdown preview.

**Normalize configuration file naming and references**
*Why it matters*: Avoids broken configuration workflows by renaming `config-json.json` to the documented `config.json` and updating references, ensuring discoverability of custom category settings.
*What to test/check*: Confirm file rename in Git history, run a quick JSON validation, and ensure the script (after upcoming changes) locates the config file.

**Add lightweight unit tests for existing helpers**
*Why it matters*: Establishes a regression safety net for core utilities like `categorize_file`, `ensure_folders_exist`, and `move_file`, using focused tests aligned with actual signatures in `desktop_cleaner.py`.
*What to test/check*: Execute the new unit test suite (e.g., `pytest` or `python -m unittest`) and verify it passes on all supported platforms.

**Implement CLI argument parsing for path, dry-run, and skip options**
*Why it matters*: Delivers parity with documented advanced usage, enabling users to customize operations without editing code.
*What to test/check*: Run CLI smoke tests for each flag combination, including dry-run to ensure no files move; update unit/integration tests for argument handling.

**Support external configuration overrides**
*Why it matters*: Allows power users to load category mappings from `config.json`, reducing the need to edit source code for customization.
*What to test/check*: Verify fallback to built-in categories, successful load of custom JSON, and error handling for malformed files through automated tests.

**Improve logging and error reporting**
*Why it matters*: Enhances troubleshooting by adding structured console output, optional log verbosity levels, and clearer error paths around file moves and JSON writes.
*What to test/check*: Run cleanup in verbose and quiet modes, inspect generated logs for completeness, and simulate failures (e.g., permission errors) to confirm graceful handling.

**Add scheduling/integration helpers**
*Why it matters*: Provides scripts or documentation snippets to integrate with OS schedulers (Task Scheduler, cron, launchd), increasing automation value.
*What to test/check*: Follow instructions on each platform to ensure scheduled jobs invoke the CLI successfully and log results.

**Enhance desktop safety features**
*Why it matters*: Introduces safeguards like configurable exclusion patterns, disk space checks, and confirmation prompts for bulk moves, reducing the risk of unintended file relocation.
*What to test/check*: Write integration tests for exclusion patterns and manual QA of confirmation flows; verify that excluded items remain untouched.

**Explore optional UI/UX improvements**
*Why it matters*: Builds a simple GUI or system tray menu for non-technical users, bundling CLI functionality into a friendlier package.
*What to test/check*: Conduct usability walkthroughs, ensure packaging/bundling scripts work on target OSes, and run the existing test suite to confirm backend stability.
