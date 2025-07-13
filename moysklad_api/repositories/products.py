"""
Product-related repositories for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Tuple

from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.products import Product, ProductFolder, Variant, Uom, PriceType, Currency
from ..entities.base import Meta, ListEntity
from ..query import QueryBuilder


class ProductRepository(EntityRepository[Product]):
    """Repository for Product entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize product repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/product", Product)

    def get_stock(self, product_id: str) -> Dict:
        """
        Get stock info for a product.

        Args:
            product_id: Product ID

        Returns:
            Stock information
        """
        return self.api_client.get(f"{self.entity_name}/{product_id}/stock")

    def get_by_barcode(self, barcode: str) -> Product:
        """
        Find product by barcode.

        Args:
            barcode: Barcode string

        Returns:
            Product instance or None if not found
        """
        query = self.query()
        query.filter().eq("barcodes", barcode)

        products, _ = self.find_all(query)
        return products[0] if products else None

    def update_prices(self, product_id: str, prices: List[Dict]) -> Product:
        """
        Update product prices.

        Args:
            product_id: Product ID
            prices: List of price objects

        Returns:
            Updated product
        """
        data = {"salePrices": prices}
        response = self.api_client.put(f"{self.entity_name}/{product_id}", data=data)
        return Product.from_dict(response)


class ProductFolderRepository(EntityRepository[ProductFolder]):
    """Repository for ProductFolder entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize product folder repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/productfolder", ProductFolder)

    def get_products(self, folder_id: str, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Product], Meta]:
        """
        Get products in a folder.

        Args:
            folder_id: Folder ID
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of products, metadata)
        """
        product_repo = ProductRepository(self.api_client)

        query = query_builder or product_repo.query()
        query.filter().eq("productFolder.id", folder_id)

        return product_repo.find_all(query)


class VariantRepository(EntityRepository[Variant]):
    """Repository for Variant entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize variant repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/variant", Variant)

    def get_by_product(self, product_id: str) -> List[Variant]:
        """
        Get variants for a product.

        Args:
            product_id: Product ID

        Returns:
            List of variant instances
        """
        query = self.query()
        query.filter().eq("product.id", product_id)

        variants, _ = self.find_all(query)
        return variants


class UomRepository(EntityRepository[Uom]):
    """Repository for Uom (unit of measurement) entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize UOM repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/uom", Uom)

class CurrencyRepository(EntityRepository[Currency]):
    """Repository for Currency entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize currency repository.

        Args:
             api_client: API client instance
        """
        super().__init__(api_client, "entity/currency", Currency)

    def get_default(self) -> Currency:
        """
        Get default currency.
        """
        query = self.query()
        query.filter().eq("default", True).eq("archived", False)
        response = self.api_client.get(self.entity_name, params=query.to_params())

        return Currency.from_dict(response["rows"][0])


class PriceTypeRepository(EntityRepository[PriceType]):
    """Repository for PriceType entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize PriceType repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "context/companysettings/pricetype", PriceType)

    def get_default(self):
        response = self.api_client.get(f"{self.entity_name}/default")

        entity = PriceType.from_dict(response)

        return entity

