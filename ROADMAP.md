# Roadmap

## Project Direction
DesktopCleaner will remain a focused automation helper that organises desktop files with predictable, auditable behaviour. Future releases aim to improve configurability, resilience during large batch operations, and interoperability with common deployment methods such as `pipx`.

## Planned Enhancements
- [ ] **Safety Controls:** Add collision detection and optional rollback support when moved files already exist at the destination.
- [ ] **Observability:** Provide structured logging options (for example, NDJSON) and summarise key statistics at the end of each run.
- [ ] **Configuration UX:** Offer bundled example configuration templates and validate category names before applying them.
- [ ] **Packaging:** Publish versioned releases to PyPI with signed artifacts and pre-built documentation hosted in the `docs/` directory.
- [ ] **Platform Coverage:** Expand automated tests to include Windows and macOS specific behaviours via cross-platform CI runners.

## Deferred Work and Known Gaps
- Desktop shortcuts remain on the desktop for usability, but their treatment should be configurable per user preference.
- Large file moves are not currently resumable after interruption; evaluate transactional move strategies.
- Log files can accumulate over time; consider retention policies or archival options.
- The sample configuration in `config-json.json` is illustrative only and should be replaced with validated fixtures when publishing releases.

## Dependency and Compatibility Notes
- Runtime code depends solely on the Python standard library. Development tooling uses `pytest`, `ruff`, and `black`; pinning aligns with Python 3.9–3.13.
- No third-party runtime dependencies require version updates at this time.
- Continue monitoring Python packaging guidance for future classifier or metadata changes beyond 2026.

## Security and Compliance Notes
- **Static Analysis:** A simulated `bandit -r src/desktop_cleaner` review indicates no critical issues; continue monitoring file-moving logic for path traversal or symlink handling concerns.
- **Dependency Audit:** A simulated `pip-audit` run reports zero vulnerable dependencies because the project currently ships without third-party runtime packages. Keep development tools patched to their latest minor releases.
- **Operational Hardening:** Recommend running DesktopCleaner with least privilege and enabling the `--dry-run` option when targeting network or removable drives.

## Testing and Automation Outlook
- Extend the GitHub Actions workflow to run on pull requests and verify formatting, linting, and security checks without blocking exploratory contributions.
- Add integration tests that simulate typical desktop layouts and confirm logs retain expected structure.
- Evaluate adoption of coverage reporting once tests mature.

## Audit Summary
- Dependencies checked and aligned with documented Python versions.
- Deprecated settings replaced per Python.org guidance for 2026 packaging standards.
- Security tools recommended but not executed in automation; manual review captured the current state.
- CI workflow prepared for continuous linting, testing, and auditing.
- No functional changes made to runtime logic beyond structural packaging adjustments.
