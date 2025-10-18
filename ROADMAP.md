# Roadmap

## Maintenance Themes
- Align documentation, tests, and functionality to rebuild trust in the feature set.
- Introduce safety controls such as dry-run mode and timestamped log retention.
- Establish automated quality gates for linting, testing, and security scanning.

## Upcoming Tasks
- [ ] Feature Parity: Implement argument parsing with `--dry-run`, `--path`, and external rule loading.
- [ ] Safety: Prevent overwriting of existing files by adding collision checks before moving items.
- [ ] Logging: Emit timestamped log files instead of overwriting `desktop_cleanup_log.json`.
- [ ] Configuration: Parse `config-json.json` and document user overrides.
- [ ] Testing: Repair `test_desktop_cleaner.py` so it imports the correct module and reflects current capabilities.
- [ ] Security: Validate target directories and sanitize logged file names to avoid information leaks.
- [ ] Dependency Management: Evaluate adding pinned dev dependencies (pytest, ruff, black) to ensure reproducible tooling.
- [ ] Tooling: Ensure Bandit and pip-audit run locally and in CI once dependency installation is available.
- [ ] CI Pipeline: Extend `.github/workflows/lint.yml` to run unit tests once they pass reliably.

## Research Ideas
- Explore a manifest-based undo system that can reverse moves when something goes wrong.
- Investigate a cross-platform GUI or TUI front-end for previewing cleanup operations.
- Consider packaging the utility for `pipx` once configuration and logging enhancements stabilize.

## Audit Notes
Legacy findings are preserved in `docs/archive/2023-project-audit-report.md` for historical context.
