from requests import HTTPError


class AutomizorVaultError(RuntimeError):
    """Exception raised for errors encountered while interacting with the Vault."""


class SecretNotFoundError(HTTPError):
    """Exception raised when an secret is not found."""
