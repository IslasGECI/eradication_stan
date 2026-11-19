# AGENTS

## Public interface

The public interface is the FastAPI app exported as `api` from `eradication_stan` (`eradication_stan/__init__.py`); its elements are the HTTP routes registered on that app. Internal callables and Stan sources are not part of it.

## Environment and paths

- Python >=3.9; `flit_core` builds the `eradication_stan` distribution. Runtime requirements: `fastapi`, `httpx`, `pandas`, `python-multipart`; dev extra: `pandas-stubs`, `geci-test-tools`.
- `Dockerfile` installs tooling, clones CmdStan recursively into `/opt/cmdstan`, runs `make build` there, then `make install` from `/workdir`.
- `api.py` and `run_predictions.py` hardcode `/workdir` paths; `build_model.py` runs `make <stan_basename>` with `cwd="/opt/cmdstan"`.
- Compiled Stan executables land beside their sources: `cat_eradication`, `cat_eradication_traps` and `cat_eradication_traps_and_cameras` in `/workdir`; `tests/data/cat_eradication_for_tests` is tracked with mode `100755`.

## Verification

- `make init` = `init_git` + `setup` + `tests`; `init_git` sets the global git safe.directory for `/workdir` and the GECI author identity.
- `make setup` = `clean install_dev`; `install_dev` = `pip install --editable ".[dev]"`; `install` = `pip install --editable .`.
- `make check` = `black --check --line-length 100` on `eradication_stan` and `tests`, `flake8 --max-line-length 100` on both, `mypy` on both. `.flake8` ignores E203, E266, E501; selects B,C,E,F,W,T4,B9; max-complexity 18.
- `make tests` = `pytest --verbose tests`; `make coverage` = `setup install_dev` then `pytest --cov=eradication_stan --cov-report=xml` plus `coverage report --show-missing`; `make mutants` = `setup install_dev` then `mutmut run` (`paths_to_mutate = eradication_stan/`, `pytest_add_cli_args_test_selection = tests/`).
- `make clean` removes `.*_cache`, module egg-info, both `__pycache__` trees, `mutants`, `coverage.xml` and the `cat_eradication` binary; it does not remove `cat_eradication_traps`.
- `make format` = black at line length 100 on module and tests; `make all` = `check coverage mutants`.
- `red`, `green` and `refactor` format, run pytest, then commit on success or restore test/module files on failure, and finish with `chmod g+w -R .`.

## CI and release

- `.github/workflows/actions.yml` runs on push to `develop`; job order is `build-image` → `test-module` → `build-n-publish` → `cleanup-artifacts`.
- `test-module` runs `make check`, `make coverage` and `make mutants` in the built image (the last two mount `$PWD:/workdir`), uploads Codecov with token and slug, force-pushes tag `latest`, and pushes `latest` plus `${GITHUB_SHA:0:4}` to Docker Hub.
- `build-n-publish` holds `permissions: id-token: write` and publishes with `pypa/gh-action-pypi-publish@release/v1` and `skip-existing: true`.

## Conventions

- Package version lives in `eradication_stan/__init__.py` as `__version__`; version tags use `vX.Y.Z`.
- Makefile targets encode commit messages with emoji prefixes: `🛑🧪 Fail tests`, `✅ Pass tests`, `♻️ Refactor`.
- Routes write uploaded files into the working directory under the uploaded filename, delete them after sampling, and use `api_predictions.csv` as the temporary output.
