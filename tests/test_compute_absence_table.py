import pandas as pd

from eradication_stan.compute_absence_table import compute_posterior_distribution


def test_compute_posterior_distribution():
    traps_effort_captures_df = pd.read_csv(
        "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    )
    obtained = compute_posterior_distribution(traps_effort_captures_df)
    expected_rows = 1000
    assert len(obtained) == expected_rows
    expected_population_columns = 13
    obtained_population_columns = len(
        [column for column in obtained.columns if column.startswith("N.")]
    )
    assert obtained_population_columns == expected_population_columns
