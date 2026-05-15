import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

client = TestClient(app_module.app)

@pytest.fixture
def client_fixture():
    return client

@pytest.fixture(autouse=True)
def restore_activities():
    snapshot = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(snapshot)
