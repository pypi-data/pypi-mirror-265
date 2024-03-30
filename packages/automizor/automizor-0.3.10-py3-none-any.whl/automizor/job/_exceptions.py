from requests import HTTPError


class AutomizorJobError(RuntimeError):
    """Exception raised for errors encountered while interacting with the Job."""


class ContextNotFoundError(HTTPError):
    """Exception raised when an job is not found."""
