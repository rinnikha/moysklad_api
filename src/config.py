"""
Configuration classes for the MoySklad API client.
"""


class MoySkladConfig:
    """Configuration for the MoySklad API client."""

    def __init__(
            self,
            token: str = None,
            base_url: str = "https://api.moysklad.ru/api/remap/1.2",
            retry_count: int = 3,
            retry_delay: int = 1,
            timeout: int = 60,
            debug: bool = False
    ):
        """
        Initialize MoySklad API configuration.

        Args:
            token: MoySklad API token.
            base_url: MoySklad API base URL
            retry_count: Number of retry attempts for failed requests
            retry_delay: Delay between retry attempts in seconds
            timeout: Request timeout in seconds
            debug: Enable debug logging
        """
        self.token = token
        self.base_url = base_url
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.debug = debug