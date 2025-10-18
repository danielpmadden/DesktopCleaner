# Changelog

All notable changes to this project will be documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions and adheres to semantic versioning once official releases begin.

## [Unreleased]
### Added
- Repository-wide audit documentation, including an updated roadmap and dependency overview.
- GitHub Actions workflow refinements for linting, testing, and security recommendations.
- Source layout under `src/` with a dedicated package entry point for `python -m desktop_cleaner`.
- Root-level changelog, roadmap refresh, and clarified README authored by Daniel Madden.

### Changed
- Packaging metadata to comply with current Python packaging guidance and MIT SPDX licensing.
- Standard `.gitignore` rules to cover build artifacts, caches, and virtual environments.

### Security
- Documented outcomes of manual `bandit` and `pip-audit` reviews and captured follow-up actions in the roadmap.
