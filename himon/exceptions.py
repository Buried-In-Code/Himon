"""The Exceptions module.

This module provides the following classes:

- ServiceError
- AuthenticationError
- RateLimitError
"""

__all__ = ["AuthenticationError", "RateLimitError", "ServiceError"]


class ServiceError(Exception):
    """Class for any API errors."""


class AuthenticationError(ServiceError):
    """Class for any authentication errors."""


class RateLimitError(Exception):
    """Class for any API Rate Limit errors."""
