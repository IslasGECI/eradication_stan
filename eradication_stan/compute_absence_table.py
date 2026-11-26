import json

from cat_data_tools import transform_effort_captures_to_dict
from eradication_stan.run_predictions import run_predictions
from eradication_stan.build_model import build_model


def compute_posterior_distribution(traps_effort_captures_df):
    effort_captures_dict = transform_effort_captures_to_dict(traps_effort_captures_df)
    internal_json_path = "internal_effort_captures_to_stan.json"
    write_json(effort_captures_dict, internal_json_path)

    initial_parameters_filename = "tests/data/init.json"

    output_path = "internal_distribution.csv"
    model_file = "cat_eradication"

    stan_file = f"/workdir/{model_file}.stan"
    build_model(stan_file)
    predictions = run_predictions(
        model_path=model_file,
        data_path=internal_json_path,
        initial_parameters=initial_parameters_filename,
        output_path=output_path,
    )
    return predictions


def write_json(data, file_path):
    json_str = json.dumps(data, indent=4)
    with open(file_path, "w") as f:
        f.write(json_str)
