"""
Organization-related repositories for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Tuple

from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.organization import Organization, Employee, Group, Store
from ..entities.base import Meta
from ..query import QueryBuilder


class OrganizationRepository(EntityRepository[Organization]):
    """Repository for Organization entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize organization repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/organization", Organization)

    def get_accounts(self, organization_id: str) -> Dict:
        """
        Get accounts for an organization.

        Args:
            organization_id: Organization ID

        Returns:
            Accounts data
        """
        return self.api_client.get(f"{self.entity_name}/{organization_id}/accounts")

    def add_account(self, organization_id: str, account_data: Dict) -> Dict:
        """
        Add account to an organization.

        Args:
            organization_id: Organization ID
            account_data: Account data

        Returns:
            Created account data
        """
        return self.api_client.post(f"{self.entity_name}/{organization_id}/accounts", data=account_data)


class EmployeeRepository(EntityRepository[Employee]):
    """Repository for Employee entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize employee repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/employee", Employee)

    def get_current(self) -> Employee:
        """
        Get current employee (authenticated user).

        Returns:
            Current employee entity
        """
        response = self.api_client.get("context/employee")
        return Employee.from_dict(response)


class StoreRepository(EntityRepository[Store]):
    """Repository for Store entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize store repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/store", Store)

    def get_stock(self, store_id: str, query_builder: Optional[QueryBuilder] = None) -> Dict:
        """
        Get stock for a store.

        Args:
            store_id: Store ID
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Stock data
        """
        params = query_builder.to_params() if query_builder else {}
        return self.api_client.get(f"{self.entity_name}/{store_id}/stock", params=params)