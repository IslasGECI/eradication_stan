import pandas as pd
from pathlib import Path
import subprocess


def run_predictions(model_path, data_path, initial_parameters, output_path):

    command = [
        f"/workdir/{model_path}",
        "sample",
        "data",
        f"file={data_path}",
        f"init={initial_parameters}",
        "output",
        f"file={output_path}",
    ]
    result = subprocess.run(command)
    predictions = pd.read_csv(output_path, comment="#")
    Path(str(output_path)).unlink(missing_ok=True)
    return predictions
