from eradication_stan.api import api

import io
from fastapi.testclient import TestClient

client = TestClient(api)


def test_api_write_eradication_bayesian_model_results():
    data_path = "tests/data/data.json"
    initial_parameters_path = "tests/data/init.json"

    with open(data_path, "rb") as f:
        file_like_data = io.BytesIO(f.read())

    with open(initial_parameters_path, "rb") as f:
        file_like_init = io.BytesIO(f.read())

    request = {
        "url": "/write_eradication_bayesian_model_results",
        "files": {
            "data_path": (f"{data_path}", file_like_data, "application/json"),
            "initial_parameters_path": (
                f"{initial_parameters_path}",
                file_like_init,
                "application/json",
            ),
        },
    }

    response = client.post(**request)
    assert response.status_code == 200
    content = response.json()
    assert "r" in content[0]
