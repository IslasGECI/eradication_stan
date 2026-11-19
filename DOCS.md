# Public interface

### POST /write_eradication_bayesian_model_results/

Runs the cat-eradication analysis on capture and survey-effort records and returns the sampled results.

Parameters
- `data_path`: uploaded JSON file holding `T`, `capturas` and `esfuerzo`.
- `initial_parameters_path`: uploaded JSON file holding starting values `N0`, `r` and `q`.

Returns
- JSON array of result records, including `N0`, `r`, `q`, `is_extinct`, `E_critical`, `is_progress`, `is_progress_from_births` and `n_birth`.

### POST /compute_eradication_bayesian_model_results/

Runs the cat-eradication analysis on trap survey records, optionally with camera detections, and returns the sampled results.

Parameters
- `data_path`: uploaded JSON file holding `T`, `captures` and `traps_effort`; `detections` and `cameras_effort` are also required when `model_type` is `traps-and-cameras`.
- `initial_parameters_path`: uploaded JSON file holding starting values `N0`, `r` and `traps_q`; `cameras_q` is also required when `model_type` is `traps-and-cameras`.
- `model_type`: form field selecting the analysis: `traps` or `traps-and-cameras`.

Returns
- JSON array of result records, including `N0`, `r`, `traps_q`, `is_extinct`, `E_critical`, `is_progress`, `is_progress_from_births` and `n_birth`; `cameras_q` is included for `traps-and-cameras`.
