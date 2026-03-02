# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `conditions` | `task.conditions` | `['go_left', 'go_right', 'stop_left', 'stop_right']` | `LOGAN1984` | Go/stop discrimination with left-right choice response is central to response inhibition design. | `adapted` | Condition tokens include direction to support stimulus-side analyses. |
| `stop_ratio` | `src/utils.generate_sst_conditions(stop_ratio)` | `0.25` | `BAND2003` | Simulations discuss mixed go/stop schedules with stop trials as a minority class. | `inferred` | Implemented via custom condition generator for sequence constraints. |
| `total_blocks` | `task.total_blocks` | `3` (human), `1` (qa/sim) | `VERBRUGGEN2019` | SST guidance emphasizes enough trials for stable inhibition estimates. | `adapted` | QA/sim profiles are reduced for smoke testing only. |
| `trial_per_block` | `task.trial_per_block` | `70` (human), `24` (qa/sim) | `VERBRUGGEN2019` | Reliable SSRT estimates require repeated go and stop events. | `inferred` | Total trial count balances runtime and signal quality for this implementation. |
| `fixation_duration` | `timing.fixation_duration` | `[0.8, 1.0]` s | `KOK2004` | Pre-stimulus fixation period is used before go onset in EEG SST workflows. | `adapted` | Implemented as sampled interval per trial. |
| `go_duration` | `timing.go_duration` | `1.0` s | `BAND2003` | Go response window is finite to classify misses consistently. | `adapted` | Applied to both go-only and stop-trial go phases. |
| `ssd_initial` | `controller.initial_ssd` | `0.25` s | `BAND2003` | Staircase methods initialize SSD at an intermediate delay value. | `adapted` | Updated online with 1-up/1-down rule. |
| `ssd_bounds` | `controller.min_ssd`, `controller.max_ssd` | `0.05` to `0.5` s | `VERBRUGGEN2019` | Practical SST implementations constrain SSD to avoid degenerate floor/ceiling states. | `inferred` | Boundaries set in controller config and enforced each update. |
| `ssd_step` | `controller.step` | `0.05` s | `BAND2003` | Staircase increment/decrement with fixed step supports convergence near 50% stop success. | `direct` | Shared SSD pool by default (`condition_specific: false`). |
| `trigger_go_onset` | `triggers.map.go_onset` | `10` | `KOK2004` | EEG analyses align go-locked components to go onset markers. | `direct` | Sent on both go-only and stop trials at go onset. |
| `trigger_stop_onset` | `triggers.map.stop_onset` | `22` | `KOK2004` | Successful vs failed stopping analyses require stop-signal onset markers. | `direct` | Emitted at red stop-signal onset. |
| `trigger_go_response` | `triggers.map.go_response` | `11` | `KOK2004` | Response-locked analyses need explicit response event codes. | `direct` | Used for go-response capture window. |
| `trigger_pre_stop_response` | `triggers.map.pre_stop_response` | `23` | `KOK2004` | Early responses before stop onset are behaviorally distinct in SST. | `adapted` | Captures responses during pre-stop go window. |
| `trigger_on_stop_response` | `triggers.map.on_stop_response` | `24` | `KOK2004` | Responses after stop onset classify failed stopping. | `direct` | Emitted in stop-signal window on keypress. |
