# Backlog

- [ ] Explore the benefits of return JSONResponse on each endpoint
## Features
- [ ] Agregar columna "population_size_percentile_50" a la tabla que sale de `compute_absence_table()`
## Bugs

- [ ] Fix `build_model()` error handling: `except result.CalledProcessError` in `eradication_stan/build_model.py:12` references `result` before assignment, and `subprocess.run` has no `check=True`, so failures are never raised there. Introduced in `d220697`.

## Limitations

- [ ] Remove hardcoded `/workdir` and `/opt/cmdstan` paths from `api.py`, `run_predictions.py` and `build_model.py` so the package works when installed outside the container. Evidence: `00c633e`, `8a5b5c6`, `02fd299`, `6b74c1d`.
