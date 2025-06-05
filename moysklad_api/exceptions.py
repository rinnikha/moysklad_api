"""
Custom exceptions for the MoySklad API client.
"""

from typing import Dict, Optional


class MoySkladException(Exception):
    """Base exception for MoySklad API errors."""

    def __init__(self, status_code: int, error_message: str, response_body: Optional[Dict] = None):
        """
        Initialize MoySklad API exception.

        Args:
            status_code: HTTP status code of the response
            error_message: Error message from the API
            response_body: Full response body (if available)
        """
        self.status_code = status_code
        self.error_message = error_message
        self.response_body = response_body
        super().__init__(f"MoySklad API Error: {status_code} - {error_message}")


class RateLimitException(MoySkladException):
    """Exception raised when API rate limit is exceeded."""

    def __init__(self, retry_after: int, *args, **kwargs):
        """
        Initialize rate limit exception.

        Args:
            retry_after: Recommended wait time in seconds before retrying
        """
        self.retry_after = retry_after
        super().__init__(*args, **kwargs)


class AuthenticationException(MoySkladException):
    """Exception raised when authentication fails."""
    pass


class NotFoundException(MoySkladException):
    """Exception raised when a resource is not found."""
    pass


class ValidationException(MoySkladException):
    """Exception raised when validation fails."""
    pass