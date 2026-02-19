from eradication_stan.api import api

import io
from fastapi.testclient import TestClient

client = TestClient(api)


def test_api_write_eradication_bayesian_model_results():
    real_data_path = "tests/data/data.json"
    initial_parameters_path = "tests/data/init.json"

    with open(real_data_path, "rb") as f:
        file_like_data = io.BytesIO(f.read())

    with open(initial_parameters_path, "rb") as f:
        file_like_init = io.BytesIO(f.read())

    remote_data_path = "data.json"
    remote_initial_parameters_path = "init.json"

    request = {
        "url": "/write_eradication_bayesian_model_results",
        "files": {
            "data_path": (remote_data_path, file_like_data, "application/json"),
            "initial_parameters_path": (
                f"{remote_initial_parameters_path}",
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
