# The Delinea DevOps Secrets Vault Python SDK

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![PyPI Version](https://img.shields.io/pypi/v/python-dsv-sdk)
![License](https://img.shields.io/github/license/DelineaXPM/python-dsv-sdk)
![Python Versions](https://img.shields.io/pypi/pyversions/python-dsv-sdk)

The [Delinea](https://delinea.com/)
[DevOps Secrets Vault](https://delinea.com/products/devops-secrets-management-vault)
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
from delinea.secrets.vault import PasswordGrantAuthorizer

authorizer = PasswordGrantAuthorizer("https://mytenant.secretsvaultcloud.com/", "my_client_id", "my_client_secret")
```

#### Access Token Authorization

If you already have a valid `access_token`, you can pass directly via the `AccessTokenAuthorizer`.

```python
from delinea.secrets.vault import AccessTokenAuthorizer

authorizer = AccessTokenAuthorizer("YgJ1slfZs8ng9bKsRsB-tic0Kh8I...")
```

### Secrets Vault

Instantiate `SecretsVault` by passing your `base_url` and `Authorizer` as arguments:

```python
from delinea.secrets.vault import SecretsVault

vault = SecretsVault("https://mytenant.secretsvaultcloud.com/", authorizer)
```

Secrets can be fetched using the `get_secret` method, which takes the `secret_path` of the secret and returns a `json` object. Alternatively, you can use pass the json to `VaultSecret` which returns a `dataclass` object representation of the secret:

```python
from delinea.secrets.vault import VaultSecret

secret = VaultSecret(**vault.get_secret("/test/secret"))

print(f"username: {secret.data['username']}\npassword: {secret.data['password']}")
```

## Using Self-Signed Certificates

When using a self-signed certificate for SSL, the `REQUESTS_CA_BUNDLE` environment variable should be set to the path of the certificate (in `.pem` format). This will negate the need to ignore SSL certificate verification, which makes your application vunerable. Please reference the [`requests` documentation](https://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification) for further details on the `REQUESTS_CA_BUNDLE` environment variable, should you require it.

## Create a Build Environment (optional)

The SDK requires [Python 3.7](https://www.python.org/downloads/) or higher.

Assuming that you have a supported version of Python installed, you can clone
this repository and set up your environment with:

```shell
# Clone the repo
git clone https://github.com/DelineaXPM/python-dsv-sdk
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
export DSV_CLIENT_ID=""
export DSV_CLIENT_SECRET=""
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
