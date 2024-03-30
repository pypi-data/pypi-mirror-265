import os
from dataclasses import asdict

import requests

from automizor.utils import get_headers
from ._container import SecretContainer
from ._exceptions import AutomizorVaultError


class Vault:
    """
    `Vault` is a secure storage class within the `Automizor Platform` for managing
    secrets such as API keys, passwords, and other sensitive information. It offers
    functionality to securely retrieve and update secrets through direct interaction
    with the `Automizor API`.

    Configuration for accessing and manipulating these secrets is driven by environment
    variables, which are essential for specifying the API's host and token for
    authentication purposes.

    Environment variables requisite for operation include:
    - ``AUTOMIZOR_API_HOST``: The host URL for the `Automizor API`.
    - ``AUTOMIZOR_API_TOKEN``: The token for authenticate against the `Automizor API`.

    Example usage:

    .. code-block:: python

        from automizor import vault

        # Create a new secret
        vault.create_secret(name="MySecret", value={"username": "admin", "password": "*****"})

        # Retrieve a secret by its name
        secret = vault.get_secret("MySecret")
        print(secret.get("username"))  # Output: "admin"
        print(secret.get("password"))  # Output: "*****"

        # Update a existing secret
        secret = vault.get_secret("MySecret")
        secret.update({"username": "user"})
        vault.set_secret(secret)
    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")

        self.session = requests.Session()
        self.session.headers.update(get_headers(self._api_token))

    def create_secret(self, secret: SecretContainer) -> SecretContainer:
        """
        Creates a new secret. Stores the secret in the `Automizor API`.
        If the secret already exists, it will be updated.

        Args:
            secret: The secret to create.

        Returns:
            The created secret.

        Raises:
            AutomizorVaultError: If creating the secret fails.
        """

        try:
            return self._write_vault_secret(secret)
        except AutomizorVaultError:
            return self._create_vault_secret(secret)

    def get_secret(self, name) -> SecretContainer:
        """
        Retrieves a secret by its name. Fetches from the `Automizor API`.

        Args:
            name: The name of the secret to retrieve.

        Returns:
            The retrieved secret.

        Raises:
            AutomizorVaultError: If retrieving the secret fails.
        """

        return self._read_vault_secret(name)

    def set_secret(self, secret: SecretContainer) -> SecretContainer:
        """
        Updates an existing secret. Updates to the `Automizor API`.

        Args:
            secret: The secret to update.

        Returns:
            The updated secret.

        Raises:
            AutomizorVaultError: If updating the secret fails.
        """

        return self._write_vault_secret(secret)

    def _create_vault_secret(self, secret: SecretContainer) -> SecretContainer:
        url = f"https://{self._api_host}/api/v1/vault/secret/"
        try:
            response = self.session.post(
                url, timeout=10, json=asdict(secret), verify=False
            )
            response.raise_for_status()
            return SecretContainer(**response.json())
        except Exception as exc:
            try:
                msg = exc.response.json()
            except (AttributeError, ValueError):
                msg = str(exc)
            raise AutomizorVaultError(f"Failed to create secret: {msg or exc}") from exc

    def _read_vault_secret(self, name: str) -> SecretContainer:
        url = f"https://{self._api_host}/api/v1/vault/secret/{name}/"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return SecretContainer(**response.json())
        except Exception as exc:
            try:
                msg = exc.response.json()
            except (AttributeError, ValueError):
                msg = str(exc)
            raise AutomizorVaultError(f"Failed to get secret: {msg}") from exc

    def _write_vault_secret(self, secret: SecretContainer) -> SecretContainer:
        url = f"https://{self._api_host}/api/v1/vault/secret/{secret.name}/"
        try:
            response = self.session.put(url, timeout=10, json=asdict(secret))
            response.raise_for_status()
            return SecretContainer(**response.json())
        except Exception as exc:
            try:
                msg = exc.response.json()
            except (AttributeError, ValueError):
                msg = str(exc)
            raise AutomizorVaultError(f"Failed to set secret: {msg}") from exc
