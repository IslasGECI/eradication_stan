from eradication_stan.run_predictions import run_predictions

import geci_test_tools as gtt


def test_run_predictions():

    output_path = "predictions.csv"
    gtt.if_exist_remove(output_path)
    run_predictions(
        model_path="tests/data/cat_eradication_for_tests",
        data_path="tests/data/data.json",
        initial_parameters="tests/data/init.json",
        output_path=output_path,
    )
    gtt.assert_exist(output_path)
    gtt.if_exist_remove(output_path)
