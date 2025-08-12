"""
Product-related repositories for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Tuple

from moysklad_api.entities.webhook import Webhook, WebhookStock

from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.products import (
    Product,
)
from ..entities.base import Meta, ListEntity
from ..query import QueryBuilder


class WebhookRepository(EntityRepository[Webhook]):
    """Repository for Webhook entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize webhook repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/webhook", Webhook)


class WebhookStockRepository(EntityRepository[WebhookStock]):
    """Repository for WebhookStock entities."""

    def __init__(self, api_client: ApiClient):
        """Initialize webhook stock repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/webhookstock", WebhookStock)
