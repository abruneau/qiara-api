import pytest
import schemathesis
from auth import get_session_id

with open("openapi.json") as f:
    schema = schemathesis.openapi.from_file(f)


@pytest.fixture(scope="session")
def session_id():
    return get_session_id()


@pytest.fixture(scope="session")
def auth_headers(session_id):
    return {"x-hlcore-session-id": session_id}
