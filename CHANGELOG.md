# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `POST /compute_eradication_bayesian_model_results` accepts trap survey data with a `model_type` of `traps` or `traps-and-cameras` and returns eradication-model results, including `cameras_q` for the latter.

### Fixed

### Changed
- `POST /write_eradication_bayesian_model_results` now returns `E_critical`, `is_progress`, `is_progress_from_births` and `n_birth` instead of `prob_extinction`, using growth-rate bounds `r` between `5e-2` and `1` and the prior `normal(0.08, 0.03)`.

### Removed

## [0.2.0] - 2026-02-19
### Added
- First working version of `write_eradication_bayesian_model_results`

## [0.1.0] - 2026-02-18
### Added
- First dummy entrypoint `write_eradication_bayesian_model_results`



[unreleased]: https://github.com/IslasGECI/eradication_stan/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/IslasGECI/eradication_stan/releases/tag/v0.2.0
[0.1.0]: https://github.com/IslasGECI/eradication_stan/releases/tag/v0.1.0
