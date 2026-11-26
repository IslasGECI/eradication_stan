from eradication_stan.api import api

import io
from fastapi.testclient import TestClient

import geci_test_tools as gtt

client = TestClient(api)


def test_api_write_eradication_bayesian_model_results():
    real_data_path = "tests/data/data.json"
    initial_parameters_path = "tests/data/init.json"

    file_like_data = load_file_on_buffer(real_data_path)
    file_like_init = load_file_on_buffer(initial_parameters_path)

    remote_data_path = "data.json"
    remote_initial_parameters_path = "init.json"

    request = {
        "url": "/write_eradication_bayesian_model_results",
        "files": {
            "data_path": (remote_data_path, file_like_data, "application/json"),
            "initial_parameters_path": (
                remote_initial_parameters_path,
                file_like_init,
                "application/json",
            ),
        },
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "r" in content[0]
    assert "N0" in content[0]
    assert "q" in content[0]
    gtt.assert_not_exist(remote_data_path)
    gtt.assert_not_exist(remote_initial_parameters_path)
    gtt.if_exist_remove("cat_eradication")


def test_api_compute_eradication_bayesian_model_results():
    real_data_path = "tests/data/cameras_and_traps_effort_and_captures.json"
    initial_parameters_path = "tests/data/init_with_cameras.json"

    file_like_data = load_file_on_buffer(real_data_path)
    file_like_init = load_file_on_buffer(initial_parameters_path)

    remote_data_path = "data.json"
    remote_initial_parameters_path = "init.json"
    model_type = "traps"

    request = {
        "url": "/compute_eradication_bayesian_model_results",
        "files": {
            "data_path": (remote_data_path, file_like_data, "application/json"),
            "initial_parameters_path": (
                remote_initial_parameters_path,
                file_like_init,
                "application/json",
            ),
        },
        "data": {"model_type": model_type},
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "traps_q" in content[0]
    gtt.assert_not_exist(remote_data_path)
    gtt.assert_not_exist(remote_initial_parameters_path)
    gtt.if_exist_remove("cat_eradication_traps")

    model_type = "traps-and-cameras"

    request = {
        "url": "/compute_eradication_bayesian_model_results",
        "files": {
            "data_path": (remote_data_path, file_like_data, "application/json"),
            "initial_parameters_path": (
                remote_initial_parameters_path,
                file_like_init,
                "application/json",
            ),
        },
        "data": {"model_type": model_type},
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "traps_q" in content[0]
    assert "cameras_q" in content[0]
    gtt.assert_not_exist(remote_data_path)
    gtt.assert_not_exist(remote_initial_parameters_path)
    obtained_compiled_file = "/workdir/cat_eradication_traps_and_cameras"
    gtt.assert_exist(obtained_compiled_file)
    gtt.if_exist_remove(obtained_compiled_file)


def test_api_compute_absence_probaility_table():
    effort_captures_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    initial_parameters_path = "tests/data/init_with_cameras.json"

    file_like_effort_captures = load_file_on_buffer(effort_captures_path)
    file_like_init = load_file_on_buffer(initial_parameters_path)

    remote_data_path = "data.csv"
    remote_initial_parameters_path = "init.json"
    months_to_iterate = 10

    request = {
        "url": "/compute_absence_probaility_table",
        "files": {
            "data_path": (remote_data_path, file_like_effort_captures, "text/csv"),
            "initial_parameters_path": (
                remote_initial_parameters_path,
                file_like_init,
                "application/json",
            ),
        },
        "data": {"months_to_iterate": months_to_iterate},
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "population_size_percentile_95" in content[0]
    assert "extinct_probability" in content[0]
    gtt.assert_not_exist(remote_data_path)
    gtt.assert_not_exist(remote_initial_parameters_path)
    gtt.if_exist_remove("cat_eradication_traps")


def load_file_on_buffer(path):
    with open(path, "rb") as f:
        file_like_data = io.BytesIO(f.read())
    return file_like_data
