"""
Product-related repositories for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Tuple

from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.stock import Stock
from ..entities.base import Meta, ListEntity
from ..query import QueryBuilder


class StockReportRepository:
    """Repository for Product entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize product repository.

        Args:
            api_client: API client instance
        """
        self.api_client = api_client

    def get_stock_report(self, store_href) -> List[Stock]:
        """
        Get stock info for a store.

        Args:
            store_href: Store href for filtering

        Returns:
            List of Stock entities
        """

        response = self.api_client.get(f"report/stock/all?filter=store={store_href}")
        rows = response.get("rows", [])
        return [Stock.from_dict(row) for row in rows]
