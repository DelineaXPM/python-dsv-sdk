import pytest
from thycotic.secrets.vault import (
    SecretsVault,
    SecretsVaultAccessError,
    SecretsVaultError,
    VaultSecret,
)


def vault(json):
    return SecretsVault(**json)


def test_token_url(vault_json):
    assert (
        vault(vault_json).token_url
        == f"https://{vault_json['tenant']}.secretsvaultcloud.com/v1/token"
    )


def test_api_url(vault_json):
    assert (
        vault(vault_json).secret_url
        == f"https://{vault_json['tenant']}.secretsvaultcloud.com/v1/secrets"
    )


def test_get_secret(vault_json):
    assert len(VaultSecret(**vault(vault_json).get_secret("/test/secret")).id) == 36


def test_get_nonexistent_secret(vault_json):
    with pytest.raises(SecretsVaultAccessError):
        vault(vault_json).get_secret("/nonexistent")
