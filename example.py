import os

from thycotic.secrets.vault import (
    PasswordGrantAuthorizer,
    SecretsVault,
    SecretsVaultAccessError,
    SecretsVaultError,
    VaultSecret,
)


BASE_URL = os.getenv("DSV_BASE_URL")
CLIENT_ID = os.getenv("DSV_CLIENT_ID")
CLIENT_SECRET = os.getenv("DSV_CLIENT_SECRET")


def main():

    try:
        authorizer = PasswordGrantAuthorizer(BASE_URL, CLIENT_ID, CLIENT_SECRET)
        vault = SecretsVault(BASE_URL, authorizer)
        secret = VaultSecret(**vault.get_secret("/test/sdk/simple"))

        print(f"""
        username: {secret.data['username']}
        password: {secret.data['password']}
        """)

    except SecretsVaultAccessError as e:
        print(e.message)
    except SecretsVaultError as e:
        print(e.response.text)


if __name__ == "__main__":
    main()
