""" The Thycotic DevOps Secrets Vault (DSV) SDK API facilitates access to DSV
using bearer token authentication.

Example::

    vault = SecretsVault(tenant, username, password, tld="com")
    # to get the secret as a ``dict``
    secret = vault.get_secret("/path/to/secret")
    # or, to use the dataclass
    secret = VaultSecret(**vault.get_secret("/path/to/secret"))"""

import json
import re
import requests

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class VaultSecret:
    id: str
    path: str
    attributes: str
    description: str
    data: dict
    created: datetime
    last_modified: datetime
    created_by: str
    last_modified_by: str
    version: float

    DATETIME_FORMAT_PARAMETER = "datetime_format"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    # Based on https://gist.github.com/jaytaylor/3660565
    @staticmethod
    def snake_case(camel_cased):
        """ Transform to snake case

        Transforms the keys of the given map from camelCase to snake_case.
        """
        return [
            (
                re.compile("([a-z0-9])([A-Z])")
                .sub(r"\1_\2", re.compile(r"(.)([A-Z][a-z]+)").sub(r"\1_\2", k))
                .lower(),
                v,
            )
            for (k, v) in camel_cased.items()
        ]

    def __init__(self, **kwargs):
        # The REST API returns attributes with camelCase names which we replace
        # with snake_case per Python conventions
        datetime_format = self.DEFAULT_DATETIME_FORMAT
        if self.DATETIME_FORMAT_PARAMETER in kwargs:
            datetime_format = kwargs[self.DATETIME_FORMAT_PARAMETER]
        for k, v in self.snake_case(kwargs):
            # @dataclass does not marshal timestamps into datetimes automatically
            if k in ["created", "last_modified"]:
                v = datetime.strptime(v, datetime_format)
            setattr(self, k, v)


class SecretsVaultError(Exception):
    """ An Exception that embeds the server response """

    response: None

    def __init__(self, message, response=None, *args, **kwargs):
        self.message = message
        self.response = response
        super().__init__(*args, **kwargs)


class SecretsVaultAccessError(SecretsVaultError):
    """ An Exception that represents a 403 """


class SecretsVault:
    """A class that uses bearer token authentication to access the DSV API.

    It Uses :attr:`tenant`, :attr:`tld` with :attr:`DEFAULT_URL_TEMPLATE`,
    to create request URLs.

    It uses :attr:`client_id` and :attr:`client_secret`
    to get an access_token with which to make calls to the DSV REST API"""

    DEFAULT_TLD = "com"
    DEFAULT_URL_TEMPLATE = "https://{}.secretsvaultcloud.{}/v1"
    SECRET_PATH_URI = "secrets"
    TOKEN_PATH_URI = "token"

    @staticmethod
    def process(response):
        """ Process the response raising an error if the call was unsuccessful

        :param response: the response from the server
        :type response: :class:`~requests.Response`
        :return: the response if the call was successful
        :rtype: :class:`~requests.Response`
        :raises: :class:`SecretsVaultAccessError` when the caller does not have
                access to the secret
        :raises: :class:`SecretsAccessError` when the server responses with any
                other error"""

        if response.status_code >= 200 and response.status_code < 300:
            return response
        if response.status_code >= 400 and response.status_code < 500:
            raise SecretsVaultAccessError(
                json.loads(response.content)["message"], response
            )
        raise SecretsVaultError(response)

    @classmethod
    def _get_access_grant(cls, token_url, client_id, client_secret):
        """Gets an Access Grant by calling the DSV REST API ``token`` endpoint

        :raise :class:`SecretsVaultError` when the server returns anything other
               than a valid Access Grant"""

        response = requests.post(
            token_url,
            json={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
        )

        try:
            return json.loads(cls.process(response).content)
        except json.JSONDecodeError:
            raise SecretsVaultError(response)

    def __init__(
        self,
        tenant,
        client_id,
        client_secret,
        tld=DEFAULT_TLD,
        url_template=DEFAULT_URL_TEMPLATE,
    ):
        """
        :param tenant: The DSV tenant i.e. `tenant`.secretsvaultcloud.`tld`
        :type tenant: str
        :param client_id: The DSV Client Credential
        :type client_id: str
        :param client_secret: The secret corresponding to `client_id`
        :type client_secret: str
        :param tld: The top-level domain e.g. "com" or "eu" (see `tenant`)
        :type tld: str
        :param url_template: The template to format with `tenant` and `tld`
        :type url_template: str"""

        self.base_url = url_template.format(tenant, tld.strip("."))
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"{self.base_url}/{self.TOKEN_PATH_URI.lstrip('/')}"
        self.secret_url = f"{self.base_url}/{self.SECRET_PATH_URI.lstrip('/')}"

    def _refresh_access_grant(self, seconds_of_drift=300):
        """Refreshes the Access Grant if it has expired or will in the next
        `seconds_of_drift` seconds.

        :raise :class:`SecretsVaultError` when the server returns anything other
               than a valid Access Grant"""

        if (
            hasattr(self, "access_grant")
            and self.access_grant_refreshed
            + timedelta(seconds=self.access_grant["expires_in"] + seconds_of_drift)
            > datetime.now()
        ):
            return
        else:
            self.access_grant = self._get_access_grant(
                self.token_url, self.client_id, self.client_secret
            )
            self.access_grant_refreshed = datetime.now()

    def _add_authorization_header(self, existing_headers={}):
        """Adds an HTTP `Authorization` header containing the `Bearer` token

        :param existing_headers: a ``dict`` containing the existing headers
        :return: a ``dict`` containing the `existing_headers` and the
                `Authorization` header"""

        return {
            "Authorization": f"Bearer {self.access_grant['accessToken']}",
            **existing_headers,
        }

    def get_secret_json(self, secret_path):
        """Gets a secret from DSV

        :param secret_path: the path to the secret
        :type secret_path: str
        :return: a JSON formatted string representation of the secret
        :rtype: ``str``
        :raise: :class:`SecretsVaultAccessError` when the caller does not have
                permission to access the secret
        :raise: :class:`SecretsVaultError` when the REST API call fails for
                any other reason"""

        self._refresh_access_grant()

        return self.process(
            requests.get(
                f"{self.secret_url}/{secret_path}",
                headers=self._add_authorization_header(),
            )
        ).text

    def get_secret(self, secret_path):
        """Gets a secret

        :param secret_path: the path to the secret
        :type secret_path: str
        :return: a ``dict`` representation of the secret
        :rtype: ``dict``
        :raise: :class:`SecretsVaultAccessError` when the caller does not have
                permission to access the secret
        :raise: :class:`SecretsVaultError` when the REST API call fails for
                any other reason"""
        response = self.get_secret_json(secret_path)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise SecretsVaultError(response)
