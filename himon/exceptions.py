"""The Exceptions module.

This module provides the following classes:

- ServiceError
- AuthenticationError
"""

__all__ = ["AuthenticationError", "ServiceError"]


class ServiceError(Exception):
    """Class for any API errors."""


class AuthenticationError(ServiceError):
    """Class for any authentication errors."""
