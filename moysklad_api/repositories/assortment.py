"""
Assortment-related repositories for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Tuple, Union

from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.assortment import Assortment, Service, Bundle
from ..entities.products import Product, Variant
from ..entities.base import Meta
from ..query import QueryBuilder


class AssortmentRepository(EntityRepository[Assortment]):
    """Repository for Assortment entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize assortment repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/assortment", Assortment)

    def get_metadata(self) -> Dict:
        """
        Get assortment metadata.

        Returns:
            Metadata dictionary
        """
        return self.api_client.get("entity/assortment/metadata")

    def get_settings(self) -> Dict:
        """
        Get assortment settings.

        Returns:
            Settings dictionary
        """
        return self.api_client.get("entity/assortment/settings")

    def get_stock(self, assortment_id: str) -> Dict:
        """
        Get stock info for an assortment item.

        Args:
            assortment_id: Assortment item ID

        Returns:
            Stock information
        """
        return self.api_client.get(f"entity/assortment/{assortment_id}/stock")

    def get_by_product_folder(self, folder_href: str, with_subfolders: bool = False, query_builder: Optional[QueryBuilder] = None) -> Tuple[
        List[Assortment], Meta]:
        """
        Get assortment items by product folder.

        Args:
            folder_href: Product folder meta href
            with_subfolders: If true, include subfolders products
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of assortment items, metadata)
        """
        query = query_builder or self.query()
        query.filter().eq("productFolder", folder_href).eq("withSubFolders", with_subfolders)

        return self.find_all(query)

    def get_by_barcode(self, barcode: str) -> List[Assortment]:
        """
        Find assortment items by barcode.

        Args:
            barcode: Barcode string

        Returns:
            List of matching assortment items
        """
        query = self.query()
        query.filter().eq("barcode", barcode)

        items, _ = self.find_all(query)
        return items

    def search_by_name(self, search_text: str) -> Tuple[List[Assortment], Meta]:
        """
        Search assortment items by name.

        Args:
            search_text: Search text

        Returns:
            Tuple of (list of matching assortment items, metadata)
        """
        query = self.query()
        query.search(search_text)

        return self.find_all(query)

    def get_by_type(self, type_name: str, query_builder: Optional[QueryBuilder] = None) -> Tuple[
        List[Assortment], Meta]:
        """
        Get assortment items by type.

        Args:
            type_name: Type name (product, variant, service, bundle)
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of assortment items, metadata)
        """
        query = query_builder or self.query()
        query.filter().eq("type", type_name)

        return self.find_all(query)

    def get_products(self, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Assortment], Meta]:
        """
        Get only products from assortment.

        Args:
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of products, metadata)
        """
        return self.get_by_type("product", query_builder)

    def get_variants(self, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Assortment], Meta]:
        """
        Get only variants from assortment.

        Args:
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of variants, metadata)
        """
        return self.get_by_type("variant", query_builder)

    def get_services(self, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Assortment], Meta]:
        """
        Get only services from assortment.

        Args:
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of services, metadata)
        """
        return self.get_by_type("service", query_builder)

    def get_bundles(self, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Assortment], Meta]:
        """
        Get only bundles from assortment.

        Args:
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of bundles, metadata)
        """
        return self.get_by_type("bundle", query_builder)


class ServiceRepository(EntityRepository[Service]):
    """Repository for Service entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize service repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/service", Service)


class BundleRepository(EntityRepository[Bundle]):
    """Repository for Bundle entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize bundle repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/bundle", Bundle)

    def get_components(self, bundle_id: str) -> List[Dict]:
        """
        Get components of a bundle.

        Args:
            bundle_id: Bundle ID

        Returns:
            List of component data
        """
        response = self.api_client.get(f"{self.entity_name}/{bundle_id}/components")
        return response.get("rows", [])

    def add_component(self, bundle_id: str, component_data: Dict) -> Dict:
        """
        Add a component to a bundle.

        Args:
            bundle_id: Bundle ID
            component_data: Component data

        Returns:
            Created component data
        """
        return self.api_client.post(f"{self.entity_name}/{bundle_id}/components", data=component_data)

    def update_component(self, bundle_id: str, component_id: str, component_data: Dict) -> Dict:
        """
        Update a component in a bundle.

        Args:
            bundle_id: Bundle ID
            component_id: Component ID
            component_data: Component data

        Returns:
            Updated component data
        """
        return self.api_client.put(f"{self.entity_name}/{bundle_id}/components/{component_id}", data=component_data)

    def delete_component(self, bundle_id: str, component_id: str) -> None:
        """
        Delete a component from a bundle.

        Args:
            bundle_id: Bundle ID
            component_id: Component ID
        """
        self.api_client.delete(f"{self.entity_name}/{bundle_id}/components/{component_id}")