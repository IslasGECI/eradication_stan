<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Eradication Stan
[![codecov](https://codecov.io/gh/IslasGECI/eradication_stan/graph/badge.svg?token=RY807ST1T1)](https://codecov.io/gh/IslasGECI/eradication_stan)
![example branch
parameter](https://github.com/IslasGECI/eradication_stan/actions/workflows/actions.yml/badge.svg)
![licencia](https://img.shields.io/github/license/IslasGECI/eradication_stan)
![languages](https://img.shields.io/github/languages/top/IslasGECI/eradication_stan)
![commits](https://img.shields.io/github/commit-activity/y/IslasGECI/eradication_stan)
![PyPI - Version](https://img.shields.io/pypi/v/eradication_stan)

Know when a cat-eradication campaign is working. 🐍
Python wrapper used for [Stan software](https://mc-stan.org/) used for cat eradication project. 🐍

## What it does

Eradication Stan turns counts of captured cats and the effort put into trapping or camera surveys into an estimate of how the cat population is changing. It reports the likely starting population, growth rate and detection rate, and flags whether each period's effort is enough to keep the population shrinking.

## Usage

Send your observations file and your starting-guesses file together to the service. It replies with a list of result rows you can open in a spreadsheet or analysis tool. You can analyse trap counts alone, or trap counts together with camera detections.

## Before you start

- Docker with Docker Compose is the easiest option: the image already contains everything the calculations need.
- Without Docker, install the Python package and its dependencies first.

## Run the project

### Docker (recommended)

```sh
docker compose up --build -d islasgeci
docker compose exec islasgeci uvicorn eradication_stan.api:api --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000/docs` to send files from your browser.

### Native

```sh
pip install eradication_stan
uvicorn eradication_stan.api:api --reload
```

The calculation engine must be installed locally; the Docker image already includes it.
