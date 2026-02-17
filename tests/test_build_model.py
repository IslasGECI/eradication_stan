from eradication_stan.build_model import build_model

import geci_test_tools as gtt


def test_build_model():
    obtained_file = "cat_eradication"
    stan_file = f"{obtained_file}.stan"

    gtt.if_exist_remove(obtained_file)

    build_model(stan_file)

    gtt.assert_exist(obtained_file)
