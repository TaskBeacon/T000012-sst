# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `go_left` | `go_response_window` | `go_left` | White left-pointing arrow; press left key (`F`). | `LOGAN1984` | Go process requires speeded discrimination response to imperative stimulus. | `psychopy_builtin` | `n/a` | Drawn via PsychoPy `shape` vertices. |
| `go_right` | `go_response_window` | `go_right` | White right-pointing arrow; press right key (`J`). | `LOGAN1984` | Go process requires speeded discrimination response to imperative stimulus. | `psychopy_builtin` | `n/a` | Symmetric with left condition for response mapping balance. |
| `stop_left` | `pre_stop_go_window` + `stop_signal_window` | `go_left` then `stop_left` | White left arrow starts go process, then red left arrow indicates stop signal. | `BAND2003` | Stop signal interrupts ongoing go process after SSD delay in horse-race model. | `psychopy_builtin` | `n/a` | SSD is adaptive and logged per trial (`ssd_s`). |
| `stop_right` | `pre_stop_go_window` + `stop_signal_window` | `go_right` then `stop_right` | White right arrow starts go process, then red right arrow indicates stop signal. | `BAND2003` | Stop signal interrupts ongoing go process after SSD delay in horse-race model. | `psychopy_builtin` | `n/a` | Failure defined by any response before/after stop onset. |
| `all_conditions` | `fixation` | `fixation` | Central white fixation cross before go onset. | `KOK2004` | ERP workflows include pre-target fixation for baseline and onset alignment. | `psychopy_builtin` | `n/a` | Sampled duration from `[0.8, 1.0]` seconds. |
| `go_miss_feedback` | `no_response_feedback` | `no_response_feedback` | Text prompt asking participant to respond when arrow appears. | `VERBRUGGEN2019` | SST quality guidance emphasizes clear instructions and miss handling. | `psychopy_builtin` | `n/a` | Participant-facing text is config-defined for localization. |
| `block_transition` | `block` | `block_break` | Break screen with go hit-rate and stop success-rate summary. | `VERBRUGGEN2019` | Reporting recommendations include monitoring go and stop performance. | `psychopy_builtin` | `n/a` | Metrics are calculated from trial data at block end. |
| `task_start_end` | `instruction_text` / `goodbye` | `instruction_text`, `good_bye` | Chinese instructions and end screen with continue key guidance. | `VERBRUGGEN2019` | Clear participant instruction is required for valid SST behavior. | `psychopy_builtin` | `assets/instruction_text_voice.mp3` | Human mode can add generated instruction voice playback. |
