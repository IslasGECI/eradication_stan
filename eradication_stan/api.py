from eradication_stan.build_model import build_model
from eradication_stan.run_predictions import run_predictions

from fastapi import FastAPI, UploadFile, File
import pandas as pd
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
    run_predictions(
        model_path=model_path,
        data_path=data_filename,
        initial_parameters=initial_parameters_filename,
        output_path=output_path,
    )

    Path(data_filename).unlink(missing_ok=True)
    Path(initial_parameters_filename).unlink(missing_ok=True)

    predictions = pd.read_csv(output_path, comment="#")
    return predictions.to_dict(orient="records")


async def write_internal_file(data_path):
    content = await data_path.read()
    with open(data_path.filename, "wb") as f:
        f.write(content)
