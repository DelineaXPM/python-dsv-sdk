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
        "tenant": os.getenv("DSV_TENANT"),
    }


@pytest.fixture
def authorizer(env_vars):
    return PasswordGrantAuthorizer(
        env_vars['client_id'],
        env_vars["client_secret"],
        env_vars["tenant"],
    )

@pytest.fixture()
def vault(authorizer):
    return SecretsVault(authorizer)
