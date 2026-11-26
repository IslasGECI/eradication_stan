import json
import numpy as np
import pandas as pd

from cat_data_tools import transform_effort_captures_to_dict
from eradication_stan.run_predictions import run_predictions
from eradication_stan.build_model import build_model


def compute_absence_table(traps_effort_captures_df, months_to_iterate, initial_parameters_filename):
    traps_effort_captures_df_copy = traps_effort_captures_df.copy()

    posterior = compute_posterior_distribution(
        traps_effort_captures_df, initial_parameters_filename
    )
    population_size_columns = [column for column in posterior.columns if column.startswith("N.")]
    first_part_table = {
        "Fecha": pd.to_datetime(traps_effort_captures_df.Fecha),
        "Esfuerzo": traps_effort_captures_df.Esfuerzo,
        "Capturas": traps_effort_captures_df.Capturas,
        "population_size_percentile_95": [
            posterior[column].quantile(0.95) for column in population_size_columns
        ],
        "extinct_probability": [
            sum(posterior[column] < 1) / len(posterior) for column in population_size_columns
        ],
    }
    first_part_dataframe = pd.DataFrame.from_dict(first_part_table)

    median_effort = traps_effort_captures_df_copy["Esfuerzo"].median()
    table = pd.DataFrame(
        columns=[
            "Fecha",
            "Esfuerzo",
            "Capturas",
            "population_size_percentile_95",
            "extinct_probability",
        ]
    )
    first_absence_row = compute_absence_row(
        traps_effort_captures_df_copy, initial_parameters_filename
    )
    effort = traps_effort_captures_df_copy["Esfuerzo"].quantile(0.75)
    traps_effort_captures_df_copy["Fecha"] = pd.to_datetime(traps_effort_captures_df_copy["Fecha"])
    next_month = traps_effort_captures_df_copy["Fecha"].max() + pd.DateOffset(months=1)
    new_row = {
        "Fecha": next_month,
        "Esfuerzo": int(effort),
        "Capturas": np.floor(first_absence_row["population_size_percentile_95"]),
    }
    traps_effort_captures_df_copy.loc[len(traps_effort_captures_df_copy)] = new_row

    for _ in range(months_to_iterate):
        new_row = compute_absence_row(traps_effort_captures_df_copy, initial_parameters_filename)
        table.loc[len(table)] = new_row

        traps_effort_captures_df_copy["Fecha"] = pd.to_datetime(
            traps_effort_captures_df_copy["Fecha"]
        )
        next_month = traps_effort_captures_df_copy["Fecha"].max() + pd.DateOffset(months=1)
        new_row = {
            "Fecha": next_month,
            "Esfuerzo": median_effort,
            "Capturas": 0,
        }
        traps_effort_captures_df_copy.loc[len(traps_effort_captures_df_copy)] = new_row
    return pd.concat([first_part_dataframe, table])


def compute_absence_row(traps_effort_captures_df, initial_parameters_filename):
    posterior = compute_posterior_distribution(
        traps_effort_captures_df, initial_parameters_filename
    )
    population_size_columns = [column for column in posterior.columns if column.startswith("N.")]
    population_size_percentile_95 = posterior[population_size_columns[-1]].quantile(0.95)
    extinct_probability = sum(posterior["is_extinct"]) / len(posterior)
    new_row = {
        "Fecha": pd.to_datetime(traps_effort_captures_df.Fecha.iloc[-1]),
        "Esfuerzo": traps_effort_captures_df.Esfuerzo.iloc[-1],
        "Capturas": traps_effort_captures_df.Capturas.iloc[-1],
        "population_size_percentile_95": population_size_percentile_95,
        "extinct_probability": extinct_probability,
    }
    return new_row


def compute_posterior_distribution(traps_effort_captures_df, initial_parameters_filename):
    effort_captures_dict = transform_effort_captures_to_dict(traps_effort_captures_df)
    internal_json_path = "internal_effort_captures_to_stan.json"
    write_json(effort_captures_dict, internal_json_path)

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
