# The Thycotic DevOps Secrets Vault Python SDK

The [Thycotic](https://thycotic.com/)
[DevOps Secrets Vault](https://thycotic.com/products/devops-secrets-vault-password-management/)
(DSV) Python SDK contains classes that interact with the DSV REST API.

## Install

```shell
python -m pip install python-dsv-sdk
```

## Settings

The SDK API requires a `tenant`, `client_id`, `client_secret` and optional `tld`.

The API uses the `tenant` to create request URLs and it uses the `client_id` and
`client_secret` to obtain an OAuth2 access_token with which to call the DSV REST
API.

The optional top-level domain (TLD) defaults to `com`.

## Use

Simply instantiate `SecretsVault`:

```python
from thycotic.secrets.vault import SecretsVault

vault = SecretsVault("my_tenant", "my_client_id", "my_client_secret")
```

Then pass a `path` to `get_secret()` which will return the secret as a JSON
encoded string. The SDK API also contains a `VaultSecret` `@dataclass` containing
a the Secret's attributes. The `data` attribute is a Python Dictionary.

```python
from thycotic.secrets.dataclasses import Secret

secret = VaultSecret(**vault.get_secret("/test/secret"))

print(f"username: {secret.data['username']}\npassword: {secret.data['password']}")
```

## Create a Build Environment (optional)

The SDK requires [Python 3.6](https://www.python.org/downloads/) or higher,
and the [Requests](https://2.python-requests.org/en/master/) library.

First, ensure Python 3.6 is in `$PATH` then run:

```shell
git clone https://github.com/thycotic/python-dsv-sdk
cd python-dsv-sdk
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Both `example.py` and the unit tests pull the settings from a JSON file.

```python
with open('vault_config.json') as f:
    config = json.load(f)
```

They also assume that the specified `client_id` and `client_secret` can read
`/test/secret`, and that the secret.data contains `username` and
`password` fields.

Create `vault_config.json`:

```json
{
    "client_id": "359f8c9f-d555-40ff-a036-ce95432e708b",
    "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "tenant": "mytenant"
}
```

Finally, run `pytest` then build the package:

```shell
pytest
python setup.py bdist
```
