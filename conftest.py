import json
import pytest


@pytest.fixture
def vault_json():
    with open("test_vault.json") as f:
        return json.load(f)
