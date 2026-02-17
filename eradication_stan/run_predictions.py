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
    return result.returncode
