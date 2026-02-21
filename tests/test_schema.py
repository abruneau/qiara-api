import pytest
from auth import BASE_URL
from conftest import schema
from schemathesis.checks import not_a_server_error


@(
    schema.include(path="/home/history", method="POST")
    .include(path="/home/nodes")
    .include(path="/home/endpoints_read")
    .include(path="/home/open_stream")
    .include(path="/home/stream/live.jpeg")
    .include(path="/home/recording/720p")
    .parametrize()
)
def test_api(case):
    if case.method.upper() not in ("GET", "POST", "PUT", "DELETE"):
        pytest.skip(f"Skipping coverage-generated method {case.method}")
    response = case.call(base_url=BASE_URL)
    case.validate_response(response, checks=[not_a_server_error])
