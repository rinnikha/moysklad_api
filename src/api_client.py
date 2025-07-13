"""
Low-level API client for the MoySklad API.
"""

import time
import logging
import requests
from typing import Dict, Optional, Any
from .config import MoySkladConfig
from .exceptions import (
    MoySkladException,
    AuthenticationException,
    RateLimitException,
    NotFoundException,
    ValidationException
)


class ApiClient:
    """Low-level client for making requests to the MoySklad API."""

    def __init__(self, config: MoySkladConfig):
        """
        Initialize the API client.

        Args:
            config: MoySklad API configuration
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.token}",
            "Accept-Encoding": "gzip"
        })

        # Set up logging
        self.logger = logging.getLogger("moysklad_api")
        if config.debug:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            self.logger.setLevel(logging.WARNING)

    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle the API response and raise appropriate exceptions.

        Args:
            response: HTTP response from the API

        Returns:
            Parsed JSON response

        Raises:
            AuthenticationException: When authentication fails
            NotFoundException: When resource is not found
            RateLimitException: When rate limit is exceeded
            ValidationException: When request validation fails
            MoySkladException: For other API errors
        """

        if self.config.debug:
            self.logger.debug(f"Response status: {response.status_code}")
            self.logger.debug(f"Response headers: {response.headers}")
            try:
                self.logger.debug(f"Response body: {response.json()}")
            except:
                self.logger.debug(f"Response body: {response.text}")

        if 200 <= response.status_code < 300:
            if not response.content:
                return {}
            return response.json()

        error_message = "Unknown error"
        error_data = {}

        try:
            error_data = response.json()
            if "errors" in error_data and error_data["errors"]:
                error_message = "; ".join(err.get("error", "") for err in error_data["errors"])
            elif "error" in error_data:
                error_message = error_data["error"]
        except:
            error_message = response.text or "Unknown error"

        if response.status_code == 401:
            raise AuthenticationException(response.status_code, error_message, error_data)
        elif response.status_code == 404:
            raise NotFoundException(response.status_code, error_message, error_data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitException(retry_after, response.status_code, error_message, error_data)
        elif 400 <= response.status_code < 500:
            raise ValidationException(response.status_code, error_message, error_data)
        else:
            raise MoySkladException(response.status_code, error_message, error_data)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make a request to the MoySklad API with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional parameters to pass to requests

        Returns:
            Parsed JSON response

        Raises:
            MoySkladException: When all retries fail
        """

        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"

        self.logger.debug(f"Making {method} request to {url}")
        if "json" in kwargs and self.config.debug:
            self.logger.debug(f"Request body: {kwargs['json']}")
        if "params" in kwargs and self.config.debug:
            self.logger.debug(f"Request params: {kwargs['params']}")

        kwargs["timeout"] = kwargs.get("timeout", self.config.timeout)

        for attempt in range(self.config.retry_count):
            try:
                response = self.session.request(method, url, **kwargs)
                return self._handle_response(response)
            except RateLimitException as e:
                if attempt == self.config.retry_count - 1:
                    raise

                wait_time = e.retry_after or self.config.retry_delay
                self.logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds before retry.")
                time.sleep(wait_time)
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt == self.config.retry_count - 1:
                    raise MoySkladException(0, str(e))

                wait_time = self.config.retry_delay * (2 ** attempt)  # Exponential backoff
                self.logger.warning(f"Connection error: {str(e)}. Retrying in {wait_time} seconds.")
                time.sleep(wait_time)

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a GET request to the MoySklad API.

        Args:
            endpoint: API endpoint path
            params: URL parameters

        Returns:
            Parsed JSON response
        """
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Make a POST request to the MoySklad API.

        Args:
            endpoint: API endpoint path
            data: Request body data
            params: URL parameters

        Returns:
            Parsed JSON response
        """
        return self._make_request("POST", endpoint, json=data, params=params)

    def put(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """
        Make a PUT request to the MoySklad API.

        Args:
            endpoint: API endpoint path
            data: Request body data
            params: URL parameters

        Returns:
            Parsed JSON response
        """
        return self._make_request("PUT", endpoint, json=data, params=params)

    def delete(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a DELETE request to the MoySklad API.

        Args:
            endpoint: API endpoint path
            params: URL parameters

        Returns:
            Parsed JSON response
        """
        return self._make_request("DELETE", endpoint, params=params)