from eradication_stan.api import api
from fastapi.testclient import TestClient
from geci_test_tools import assert_exist, if_exist_remove

client = TestClient(api)


def test_api_write_eradication_bayesian_model_results():
    data_path = "tests/data/data.json"
    initial_parameters_path = "tests/data/init.json"
    output_path = "tests/eradication_results.csv"

    if_exist_remove(output_path)
    request = f"/write_eradication_bayesian_model_results/?data_path={data_path}&initial_parameters={initial_parameters_path}&output_path={output_path}"

    response = client.get(request)
    assert response.status_code == 200

    assert_exist(output_path)
