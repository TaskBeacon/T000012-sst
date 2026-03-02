# Task Logic Audit

## 1. Paradigm Intent

- Task: Stop-Signal Task (SST)
- Primary construct: Motor response inhibition under a horse-race process (go vs stop)
- Manipulated factors:
  - Go/Stop trial type
  - Stimulus direction (left/right)
  - Adaptive stop-signal delay (SSD)
- Dependent measures:
  - Go hit/miss rate
  - Stop success/failure rate
  - SSD trajectory and derived inhibition efficiency metrics
- Key citations:
  - `LOGAN1984`
  - `BAND2003`
  - `VERBRUGGEN2019`
  - `KOK2004`

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3 (human); 1 (qa/sim)
- Trials per block: 70 (human); 24 (qa/sim)
- Randomization/counterbalancing:
  - Generated per block with local RNG and sequence constraints (minimum initial go trials, capped stop clustering).
- Condition generation method:
  - Custom generator via `src/utils.generate_sst_conditions(...)`.
  - Why custom: SST requires explicit stop ratio and local run-length constraints that are not expressible as simple independent weighted labels.
  - Generated data shape: flat list of condition tokens (`go_left`, `go_right`, `stop_left`, `stop_right`) consumed by `run_trial.py`.
- Runtime-generated trial values:
  - SSD sampled from adaptive controller state at stop trial onset.
  - Determinism: block conditions are generator-seeded; trial-level SSD updates are deterministic given response stream.

### Trial State Machine

1. State name: fixation
   - Onset trigger: `fixation_onset`
   - Stimuli shown: central fixation cross
   - Valid keys: `task.key_list`
   - Timeout behavior: auto-advance after sampled fixation duration
   - Next state: go_response_window or pre_stop_go_window (by condition)

2. State name: go_response_window (go trials)
   - Onset trigger: `go_onset`
   - Stimuli shown: white directional arrow
   - Valid keys: `task.key_list`
   - Timeout behavior: records go miss and optional no-response feedback
   - Next state: trial end

3. State name: pre_stop_go_window (stop trials)
   - Onset trigger: `go_onset`
   - Stimuli shown: white directional arrow
   - Valid keys: `task.key_list`
   - Timeout behavior: runs for current SSD window
   - Next state: stop_signal_window

4. State name: stop_signal_window (stop trials)
   - Onset trigger: `stop_onset`
   - Stimuli shown: red directional arrow (stop signal)
   - Valid keys: `task.key_list`
   - Timeout behavior: stop success if no response during remaining go window
   - Next state: trial end

## 3. Condition Semantics

- Condition ID: `go_left`
  - Participant-facing meaning: respond left to left-pointing white arrow.
  - Concrete stimulus realization: `shape` arrow (white), left-pointing vertices.
  - Outcome rules: hit if correct key in go window, else miss/error.

- Condition ID: `go_right`
  - Participant-facing meaning: respond right to right-pointing white arrow.
  - Concrete stimulus realization: `shape` arrow (white), right-pointing vertices.
  - Outcome rules: hit if correct key in go window, else miss/error.

- Condition ID: `stop_left`
  - Participant-facing meaning: prepare left response to white arrow, then inhibit on red left arrow.
  - Concrete stimulus realization: `go_left` then `stop_left` after SSD.
  - Outcome rules: stop failure if any keypress in pre-stop or stop windows.

- Condition ID: `stop_right`
  - Participant-facing meaning: prepare right response to white arrow, then inhibit on red right arrow.
  - Concrete stimulus realization: `go_right` then `stop_right` after SSD.
  - Outcome rules: stop failure if any keypress in pre-stop or stop windows.

Participant-facing text/stimulus source:

- Participant-facing text source: `config/*.yaml` `stimuli` entries (`instruction_text`, `block_break`, `no_response_feedback`, `good_bye`).
- Why this source is appropriate: preserves localization and keeps runtime logic auditable without string literals in code.
- Localization strategy: swap language content in config stimuli while keeping `src/run_trial.py` unchanged.

## 4. Response and Scoring Rules

- Response mapping:
  - Left arrow -> `task.left_key`
  - Right arrow -> `task.right_key`
- Response key source: config fields (`task.key_list`, `task.left_key`, `task.right_key`).
- Missing-response policy:
  - Go trials: no keypress within `go_duration` -> go miss + miss feedback stage.
  - Stop trials: no keypress in both windows -> stop success.
- Correctness logic:
  - Go hit follows StimUnit correctness against `correct_keys`.
  - Stop failure flag set if pre-stop or stop window receives any response.
- Reward/penalty updates:
  - No monetary reward logic in this baseline SST.
- Running metrics:
  - Block-level go hit rate and stop success rate displayed in `block_break`.
  - SSD updated by staircase controller after each stop trial.

## 5. Stimulus Layout Plan

- Screen name: fixation
  - Stimulus IDs shown together: `fixation`
  - Layout anchors (`pos`): centered default origin
  - Size/spacing: default text size; single item
  - Readability/overlap checks: no overlap risk
  - Rationale: neutral baseline before response window

- Screen name: go/stop signal
  - Stimulus IDs shown together: one arrow at a time (`go_*` or `stop_*`)
  - Layout anchors (`pos`): centered default origin
  - Size/spacing: `size: 8`, single item
  - Readability/overlap checks: single centered object, high contrast
  - Rationale: isolate response and stop cues

- Screen name: instruction_text / block_break / good_bye
  - Stimulus IDs shown together: single `textbox` or `text`
  - Layout anchors (`pos`): centered, `size: [20, 5]` for textbox content
  - Size/spacing: `letterHeight: 0.78`, multiline text
  - Readability/overlap checks: single text layer to avoid overlap
  - Rationale: clear participant guidance and transitions

## 6. Trigger Plan

- `exp_onset` / `exp_end`: task start and end markers
- `block_onset` / `block_end`: per-block boundaries
- `fixation_onset`: fixation phase onset
- `go_onset`: go stimulus onset (go and stop trials)
- `go_response`: go response in go-only trials
- `go_miss`: go timeout in go-only trials
- `stop_onset`: stop-signal onset
- `pre_stop_response`: response before stop signal on stop trials
- `on_stop_response`: response after stop signal onset
- `no_response_feedback_onset`: miss-feedback onset

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: single mode-aware flow (`human|qa|sim`) with shared setup/teardown.
- `utils.py` used: yes.
- `utils.py` purpose:
  - adaptive SSD staircase controller
  - constrained stop/go condition generation
- Custom controller used: yes.
- Why PsyFlow-native path is insufficient:
  - SST requires online SSD adaptation tied to stop success history.
- Legacy/backward-compatibility fallback logic required: no.

## 8. Inference Log

- Decision: stop trial ratio fixed to 25% in generator defaults.
  - Why inference was required: selected papers discuss minority stop-trial schedules but not one mandatory constant for all implementations.
  - Citation-supported rationale: `BAND2003` simulation framing and `VERBRUGGEN2019` implementation guidance.

- Decision: fixed trigger code values for local EEG marker map.
  - Why inference was required: papers define event classes but not this repository’s numeric trigger scheme.
  - Citation-supported rationale: `KOK2004` requires separable go/stop/response events for ERP analysis.

- Decision: QA/sim reduced trial counts.
  - Why inference was required: contracts require short smoke profiles in non-human modes.
  - Citation-supported rationale: `VERBRUGGEN2019` quality guidance applies to human data collection; QA/sim are infrastructure checks.
