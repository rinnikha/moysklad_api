"""
Stock-related repositories for the MoySklad API.
"""

from typing import List

from ..api_client import ApiClient
from ..entities.stock import StockFromReport, StockFromWebhookReport


class StockReportRepository:
    """Repository for Product entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize product repository.

        Args:
            api_client: API client instance
        """
        self.api_client = api_client

    def get_stock_from_webhook_report(
        self, report_href: str, storeId: str = None
    ) -> List[StockFromWebhookReport]:
        """ """

        response = self.api_client.get_via_url(report_href)

        stock_list = [StockFromWebhookReport.from_dict(row) for row in response]

        if storeId:
            stock_list = [stock for stock in stock_list if stock.storeId == storeId]

        return stock_list

    def get_stock_report(
        self, store_href: str, type: str, product_hrefs: List[str] = None
    ) -> List[StockFromReport]:
        """
        Get stock info for a store.

        Args:
            store_href: Store href for filtering
            type: type of products "all", "positiveOnly", "negativeOnly", "empty", "nonEmpty", "underMinimum"

        Returns:
            List of Stock entities
        """

        products_filter = "".join(f";product={href}" for href in (product_hrefs or []))
        url = f"report/stock/all?filter=store={store_href};stockMode={type}{products_filter}"
        resp = self.api_client.get(url)

        all_rows: List[dict] = resp.get("rows", [])

        meta = resp.get("meta") or {}
        next_href = meta.get("nextHref")

        while next_href:
            resp = self.api_client.get_via_url(next_href)
            all_rows.extend(resp.get("rows", []))

            meta = resp.get("meta") or {}
            next_href = meta.get("nextHref")

        return [StockFromReport.from_dict(row) for row in all_rows]
