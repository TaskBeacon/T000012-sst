# Task Plot Audit

- generated_at: 2026-03-04T19:47:53
- mode: existing
- task_path: E:\Taskbeacon\T000012-sst

## 1. Inputs and provenance

- E:\Taskbeacon\T000012-sst\README.md
- E:\Taskbeacon\T000012-sst\config\config.yaml
- E:\Taskbeacon\T000012-sst\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Fixation | Present fixation cross for sampled duration (`0.8` to `1.0` s). |
- | Go Trial | Show white arrow, collect response up to `go_duration`. Timeout logs go miss and shows miss feedback. |
- | Stop Trial (Phase 1) | Show white arrow during SSD (`pre_stop_go_window`) and capture early responses. |
- | Stop Trial (Phase 2) | Replace with red arrow (`stop_signal_window`) for remaining go window and capture failed-stop responses. |
- | Update | Mark stop success/failure and update SSD staircase. |

## 3. Evidence extracted from config/source

- go_left: phase=fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- go_left: phase=go response window, deadline_expr=settings.go_duration, response_expr=settings.go_duration, stim_expr=str(condition)
- go_right: phase=fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- go_right: phase=go response window, deadline_expr=settings.go_duration, response_expr=settings.go_duration, stim_expr=str(condition)
- stop_left: phase=fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- stop_left: phase=pre stop go window, deadline_expr=ssd, response_expr=ssd, stim_expr=condition.replace('stop', 'go')
- stop_left: phase=stop signal window, deadline_expr=rem, response_expr=rem, stim_expr=str(condition)
- stop_right: phase=fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- stop_right: phase=pre stop go window, deadline_expr=ssd, response_expr=ssd, stim_expr=condition.replace('stop', 'go')
- stop_right: phase=stop signal window, deadline_expr=rem, response_expr=rem, stim_expr=str(condition)

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.050, right=0.052, blank=0.159
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0502, 'right_ratio': 0.0519, 'blank_ratio': 0.1589}

## 7. Output files and checksums

- E:\Taskbeacon\T000012-sst\references\task_plot_spec.yaml: sha256=22ae9c190d20df2f566fcb510683f362476b4dd451a4702cfa4abf6af3fc74da
- E:\Taskbeacon\T000012-sst\references\task_plot_spec.json: sha256=d56ec1320084a5bffd3456d9da94d77b148aa6fe619990cbb8818dc5f7c034f5
- E:\Taskbeacon\T000012-sst\references\task_plot_source_excerpt.md: sha256=fb6019260f29b2665db7fc0c4561d76ecf8ce0a9ba2f527316fc55e6b0039e4c
- E:\Taskbeacon\T000012-sst\task_flow.png: sha256=56c16d39ae4cc48900d3401a2212ced0390a3252afc84e4ec06a80dfc3bde3fe

## 8. Inferred/uncertain items

- collapsed equivalent condition logic into representative timeline: go_left, go_right
- collapsed equivalent condition logic into representative timeline: stop_left, stop_right
- unparsed if-tests defaulted to condition-agnostic applicability: not resp
