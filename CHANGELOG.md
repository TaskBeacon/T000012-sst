# CHANGELOG

All notable development changes for `T000012-sst` are documented here.

## [1.1.0] - 2026-02-16

### Added
- Added standardized task entry flow in `main.py` with explicit modes: `human`, `qa`, `sim`.
- Added mode-specific configs:
  - `config/config_qa.yaml`
  - `config/config_scripted_sim.yaml`
  - `config/config_sampler_sim.yaml`
- Added responder-ready trial context wiring in `src/run_trial.py` via `set_trial_context(...)`.
- Added task contract adoption metadata in `taskbeacon.yaml`:
  - `contracts.psyflow_taps: v0.1.0`

### Changed
- Refactored `main.py` to use new psyflow runtime infra:
  - `TaskRunOptions`
  - `parse_task_run_options(...)`
  - `context_from_config(...)`
  - `runtime_context(...)`
- Updated trigger schema in config to new structured format:
  - `triggers.map`
  - `triggers.driver.type`
  - `triggers.policy`
  - `triggers.timing`
- Added `task.voice_enabled` and standardized `qa`/`sim` runtime sections in config.
- Updated `.gitignore` to ignore `outputs/` artifacts.

### Fixed
- Aligned responder trial context metadata with required simulation phases in `src/run_trial.py`.

### Notes
- This migration intentionally preserves the existing task logic and trial behavior.
- Behavioral/model changes are deferred to a separate logic review pass.
