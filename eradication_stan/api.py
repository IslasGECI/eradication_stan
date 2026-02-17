from fastapi import FastAPI, UploadFile, File

api = FastAPI()


@api.post("/write_eradication_bayesian_model_results")
async def api_write_eradication_bayesian_model_results(
    data_path: UploadFile = File(...), initial_parameters_path: UploadFile = File(...)
):
    pass
