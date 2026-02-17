<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Dummy Transformations
[![codecov](https://codecov.io/gh/IslasGECI/eradication_stan/graph/badge.svg?token=RY807ST1T1)](https://codecov.io/gh/IslasGECI/eradication_stan)
![example branch
parameter](https://github.com/IslasGECI/eradication_stan/actions/workflows/actions.yml/badge.svg)
![licencia](https://img.shields.io/github/license/IslasGECI/eradication_stan)
![languages](https://img.shields.io/github/languages/top/IslasGECI/eradication_stan)
![commits](https://img.shields.io/github/commit-activity/y/IslasGECI/eradication_stan)
![PyPI - Version](https://img.shields.io/pypi/v/eradication_stan)

Para usar este repo como plantilla debemos hacer lo siguiente:

1. Presiona el botón verde que dice _Use this template_
1. Selecciona como dueño a la organización IslasGECI
1. Agrega el nombre del nuevo módulo de python
1. Presiona el botón _Create repository from template_
1. Reemplaza `eradication_stan` por el nombre del nuevo módulo en:
    - `Makefile`
    - `pyproject.toml`
    - `tests\test_transformations.py`
1. Renombra el archivo `eradication_stan\transformations.py` al nombre del primer archivo del
   nuevo módulo
1. Cambia la descripción del archivo `eradication_stan\__init__.py`
1. Renombra el directorio `eradication_stan` al nombre del nuevo módulo
1. Cambia el `codecov_token` del archivo `Makefile`

Los archivos del nuevo módulo los agregarás en la carpeta que antes se llamaba
`eradication_stan` y las pruebas en la carpeta `tests`.
