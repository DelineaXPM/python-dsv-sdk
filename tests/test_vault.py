import pytest
from thycotic.secrets.vault import (
    AccessTokenAuthorizer,
    SecretsVault,
    SecretsVaultAccessError,
    VaultSecret,
)


def test_token_url(authorizer, env_vars):
    """Tests the token_url endpoint is built correctly"""
    assert authorizer.token_url == f"{env_vars['base_url'].rstrip('/')}/v1/token"


def test_get_secret(vault):
    """Fetches a test secret"""
    assert len(VaultSecret(**vault.get_secret("/test/sdk/simple")).id) == 36


def test_get_nonexistent_secret(vault):
    """Fetches an invalid secret"""
    with pytest.raises(SecretsVaultAccessError):
        vault.get_secret("/nonexistent")


def test_get_secret_path_has_no_leading_slash(vault):
    """Test that the secret path can bu built correctly with or without the
    leading slash
    """
    assert len(VaultSecret(**vault.get_secret("test/sdk/simple")).id) == 36


def test_access_token_authorizer(authorizer, env_vars):
    """Tests that an existing access token can be used to retrieve a secret"""
    token = authorizer.get_access_token()
    vault = SecretsVault(env_vars["base_url"], AccessTokenAuthorizer(token))
    assert len(VaultSecret(**vault.get_secret("test/sdk/simple")).id) == 36
