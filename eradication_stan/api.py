from eradication_stan.build_model import build_model
from eradication_stan.run_predictions import run_predictions

from fastapi import FastAPI, UploadFile, File
import pandas as pd

api = FastAPI()


@api.post("/write_eradication_bayesian_model_results")
async def api_write_eradication_bayesian_model_results(
    data_path: UploadFile = File(...), initial_parameters_path: UploadFile = File(...)
):
    stan_file = "/workdir/tests/data/cat_eradication.stan"
    build_model(stan_file)
    model_path = "tests/data/cat_eradication"
    output_path = "api_predictions.csv"
    run_predictions(
        model_path=model_path,
        data_path=data_path.filename,
        initial_parameters=initial_parameters_path.filename,
        output_path=output_path,
    )
    predictions = pd.read_csv(output_path, comment="#")
    return predictions.to_dict(orient="records")
