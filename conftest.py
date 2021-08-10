import os
import pytest
from dotenv import load_dotenv
from thycotic.secrets.vault import PasswordGrantAuthorizer, SecretsVault


load_dotenv()


@pytest.fixture
def env_vars():
    return {
        "client_id": os.getenv("DSV_CLIENT_ID"),
        "client_secret": os.getenv("DSV_CLIENT_SECRET"),
        "base_url": os.getenv("DSV_BASE_URL"),
    }


@pytest.fixture
def authorizer(env_vars):
    return PasswordGrantAuthorizer(
        env_vars["base_url"],
        env_vars["client_id"],
        env_vars["client_secret"],
    )


@pytest.fixture()
def vault(authorizer, env_vars):
    return SecretsVault(env_vars["base_url"], authorizer)
