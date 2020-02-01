import json

from thycotic.secrets.dataclasses import VaultSecret
from thycotic.secrets.vault import (
    SecretsVault,
    SecretsVaultAccessError,
    SecretsVaultError,
)

if __name__ == "__main__":
    with open("test_vault.json") as f:
        vault = SecretsVault(**json.load(f))
    try:
        secret = VaultSecret(**vault.get_secret("/test/secret"))
        print(
            f"""username: {secret.data['username']}
password: {secret.data['password']}"""
        )
    except SecretsVaultAccessError as e:
        print(e.message)
    except SecretsVaultError as e:
        print(e.response.text)
