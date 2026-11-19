from eradication_stan.build_model import build_model
from eradication_stan.run_predictions import run_predictions

from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path

api = FastAPI()


@api.post("/write_eradication_bayesian_model_results")
async def api_write_eradication_bayesian_model_results(
    data_path: UploadFile = File(...), initial_parameters_path: UploadFile = File(...)
):
    stan_file = "/workdir/cat_eradication.stan"
    build_model(stan_file)

    await write_internal_file(data_path)
    await write_internal_file(initial_parameters_path)

    data_filename = data_path.filename
    initial_parameters_filename = initial_parameters_path.filename
    model_path = "cat_eradication"
    output_path = "api_predictions.csv"
    predictions = run_predictions(
        model_path=model_path,
        data_path=data_filename,
        initial_parameters=initial_parameters_filename,
        output_path=output_path,
    )

    Path(str(data_filename)).unlink(missing_ok=True)
    Path(str(initial_parameters_filename)).unlink(missing_ok=True)

    return predictions.to_dict(orient="records")


@api.post("/compute_eradication_bayesian_model_results")
async def api_compute_eradication_bayesian_model_results(
    data_path: UploadFile = File(...),
    initial_parameters_path: UploadFile = File(...),
    model_type: str = Form(...),
):
    models = {
        "traps": "cat_eradication_traps",
        "traps-and-cameras": "cat_eradication_traps_and_cameras",
    }
    model_file = models[model_type]
    await select_model(model_file)
    await write_internal_file(data_path)
    await write_internal_file(initial_parameters_path)

    data_filename = data_path.filename
    initial_parameters_filename = initial_parameters_path.filename
    output_path = "api_predictions.csv"
    predictions = run_predictions(
        model_path=model_file,
        data_path=data_filename,
        initial_parameters=initial_parameters_filename,
        output_path=output_path,
    )

    Path(str(data_filename)).unlink(missing_ok=True)
    Path(str(initial_parameters_filename)).unlink(missing_ok=True)

    return predictions.to_dict(orient="records")


async def select_model(model_file):
    stan_file = f"/workdir/{model_file}.stan"
    build_model(stan_file)


async def write_internal_file(data_path):
    content = await data_path.read()
    with open(data_path.filename, "wb") as f:
        f.write(content)
