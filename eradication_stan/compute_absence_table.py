import json
import pandas as pd

from cat_data_tools import transform_effort_captures_to_dict
from eradication_stan.run_predictions import run_predictions
from eradication_stan.build_model import build_model


def compute_absence_table(traps_effort_captures_df, months_to_iterate):
    table = pd.DataFrame(
        columns=["Fecha", "Esfuerzo", "population_size_percentile_95", "extinnct_probability"]
    )
    for i in range(months_to_iterate):
        new_row = compute_absence_row(traps_effort_captures_df)
        table.loc[len(table)] = new_row
    return table


def compute_absence_row(traps_effort_captures_df):
    posterior = compute_posterior_distribution(traps_effort_captures_df)
    population_size_columns = [column for column in posterior.columns if column.startswith("N.")]
    population_size_percentile_95 = posterior[population_size_columns[-1]].quantile(0.95)
    extinct_probability = sum(posterior["is_extinct"]) / len(posterior)
    new_row = {
        "Fecha": traps_effort_captures_df.Fecha.iloc[-1],
        "Esfuerzo": traps_effort_captures_df.Esfuerzo.iloc[-1],
        "population_size_percentile_95": population_size_percentile_95,
        "extinct_probability": extinct_probability,
    }
    return new_row


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
