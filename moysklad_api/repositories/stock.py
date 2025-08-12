"""
Product-related repositories for the MoySklad API.
"""

from typing import List

from ..api_client import ApiClient
from ..entities.stock import StockFromReport


class StockReportRepository:
    """Repository for Product entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize product repository.

        Args:
            api_client: API client instance
        """
        self.api_client = api_client

    def get_stock_report(self, store_href: str, type: str) -> List[StockFromReport]:
        """
        Get stock info for a store.

        Args:
            store_href: Store href for filtering
            type: type of products "all", "positiveOnly", "negativeOnly", "empty", "nonEmpty", "underMinimum"

        Returns:
            List of Stock entities
        """

        response = self.api_client.get(
            f"report/stock/all?filter=store={store_href};stockMode={type}"
        )
        rows = response.get("rows", [])
        return [StockFromReport.from_dict(row) for row in rows]
