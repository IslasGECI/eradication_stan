import pandas as pd

from eradication_stan.compute_absence_table import (
    compute_absence_table,
    compute_posterior_distribution,
    compute_absence_row,
)

traps_effort_captures_df = pd.read_csv("tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv")
initial_parameters_path = "tests/data/init.json"


def test_compute_absence_table():
    months_to_iterate = 10
    obtained = compute_absence_table(
        traps_effort_captures_df, months_to_iterate, initial_parameters_path
    )
    assert isinstance(obtained, pd.DataFrame)
    expected_shape = (months_to_iterate + len(traps_effort_captures_df), 5)
    assert obtained.shape == expected_shape
    last_date_from_raw_data = pd.to_datetime(traps_effort_captures_df.Fecha.iloc[-1])
    obtained_last_date = pd.to_datetime(obtained.Fecha.iloc[-1])
    assert obtained_last_date > last_date_from_raw_data


def test_compute_posterior_distribution():
    obtained = compute_posterior_distribution(traps_effort_captures_df, initial_parameters_path)
    expected_rows = 1000
    assert len(obtained) == expected_rows
    expected_population_columns = 13
    obtained_population_columns = len(
        [column for column in obtained.columns if column.startswith("N.")]
    )
    assert obtained_population_columns == expected_population_columns


def test_compute_absence_row():
    obtained = compute_absence_row(traps_effort_captures_df, initial_parameters_path)
    expected_columns = set(
        ["Fecha", "Esfuerzo", "Capturas", "population_size_percentile_95", "extinct_probability"]
    )
    assert set(obtained.keys()) == expected_columns
    assert isinstance(obtained, dict)
