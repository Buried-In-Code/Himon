"""
The Exceptions module.

This module provides the following classes:

- ServiceError
- AuthenticationError
"""


class ServiceError(Exception):
    """Class for any API errors."""

    pass


class AuthenticationError(ServiceError):
    """Class for any authentication errors."""

    pass
