# The Thycotic DevOps Secrets Vault Python SDK

![PyPI Version](https://img.shields.io/pypi/v/python-dsv-sdk)
![License](https://img.shields.io/github/license/thycotic/python-dsv-sdk)
![Python Versions](https://img.shields.io/pypi/pyversions/python-dsv-sdk)

The [Thycotic](https://thycotic.com/)
[DevOps Secrets Vault](https://thycotic.com/products/devops-secrets-vault-password-management/)
(DSV) Python SDK contains classes that interact with the DSV REST API.

## Install

```shell
python -m pip install python-dsv-sdk
```

## Usage

There are two ways in which you can authorize the `SecretsVault` class to fetch secrets.

- Password Authorization (with `PasswordGrantAuthorizer`)
- Access Token Authorization (with `AccessTokenAuthorizer`)

### Authorizers

#### Password Authorization

If using a traditional `client_id` and a `client_secret` to authenticate in to your DevOps Secrets Vault, you can pass the `PasswordGrantAuthorizer` into the `SecretsVault` class at instantiation. The `PasswordGrantAuthorizer` requires a `base_url`, `username`, and `password`. It _optionally_ takes a `token_path_uri`, but defaults to `/v1/token`.

```python
from thycotic.secrets.vault import PasswordGrantAuthorizer

authorizer = PasswordGrantAuthorizer("https://mytenant.secretsvaultcloud.com/", "my_client_id", "my_client_secret")
```

#### Access Token Authorization

If you already have a valid `access_token`, you can pass directly via the `AccessTokenAuthorizer`.

```python
from thycotic.secrets.vault import AccessTokenAuthorizer

authorizer = AccessTokenAuthorizer("YgJ1slfZs8ng9bKsRsB-tic0Kh8I...")
```

### Secrets Vault

Instantiate `SecretsVault` by passing your `base_url` and `Authorizer` as arguments:

```python
from thycotic.secrets.vault import SecretsVault

vault = SecretsVault("https://mytenant.secretsvaultcloud.com/", authorizer)
```

Secrets can be fetched using the `get_secret` method, which takes the `secret_path` of the secret and returns a `json` object. Alternatively, you can use pass the json to `VaultSecret` which returns a `dataclass` object representation of the secret:

```python
from thycotic.secrets.vault import VaultSecret

secret = VaultSecret(**vault.get_secret("/test/secret"))

print(f"username: {secret.data['username']}\npassword: {secret.data['password']}")
```

## Create a Build Environment (optional)

The SDK requires [Python 3.6](https://www.python.org/downloads/) or higher.

First, ensure Python 3.6 is in `$PATH` then run:

```shell
# Clone the repo
git clone https://github.com/thycotic/python-dsv-sdk
cd python-dsv-sdk

# Create a virtual environment
python -m venv venv
. venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

```

Valid credentials are required to run the unit tests. The credentials should be stored in environment variables or in a `.env` file:

```shell
export DSV_CLIENT_ID="e7f6be68-0acb-4020-9c55-c7b161620199"
export DSV_CLIENT_SECRET="0lYBbBbaXtkMd3WYydhfhuy0rHNFet_jq7QA4ZfEjxU"
export DSV_BASE_URL="https://my.secretsvaultcloud.com/"
```

The tests assume that the client associated with the specified `CLIENT_ID` can read the secret with the path `/test/sdk/simple`.

> Note: The secret path can be changed manually in `test_server.py` to a secret path that the client can access.

To run the tests with `tox`:

```shell
tox
```

To build the package, use [Flit](https://flit.readthedocs.io/en/latest/):

```shell
flit build
```
