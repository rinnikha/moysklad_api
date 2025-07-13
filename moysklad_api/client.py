"""
Main client class for the MoySklad API.
"""

from typing import Dict, Any, Optional, Type, List

from .api_client import ApiClient
from .config import MoySkladConfig
from .entities.base import MetaEntity
from .repositories.base import EntityRepository

# Import repositories
from .repositories.products import (
    ProductRepository,
    ProductFolderRepository,
    VariantRepository,
    UomRepository,
    PriceTypeRepository, CurrencyRepository
)
from .repositories.documents import (
    CustomerOrderRepository,
    InvoiceOutRepository,
    DemandRepository,
    SupplyRepository,
    CashInRepository,
    CashOutRepository,
    PaymentInRepository,
    PaymentOutRepository, PurchaseOrderRepository
)
from .repositories.counterparty import CounterpartyRepository
from .repositories.organization import (
    OrganizationRepository,
    EmployeeRepository,
    StoreRepository
)
from .repositories.assortment import (
    AssortmentRepository,
    ServiceRepository,
    BundleRepository
)



class MoySklad:
    """Main MoySklad API client."""

    def __init__(self, token: str, **kwargs):
        """
        Initialize MoySklad API client.

        Args:
            token (str): MoySklad API token.
            **kwargs: Additional configuration options
        """
        self.config = MoySkladConfig(token, **kwargs)
        self.api_client = ApiClient(self.config)

        # Initialize repositories
        self._init_repositories()

    def _init_repositories(self):
        """Initialize standard repositories."""
        # Products
        self.products = ProductRepository(self.api_client)
        self.product_folders = ProductFolderRepository(self.api_client)
        self.currencies = CurrencyRepository(self.api_client)
        self.price_types = PriceTypeRepository(self.api_client)
        self.variants = VariantRepository(self.api_client)
        self.uoms = UomRepository(self.api_client)

        # Assortment
        self.assortment = AssortmentRepository(self.api_client)
        self.services = ServiceRepository(self.api_client)
        self.bundles = BundleRepository(self.api_client)

        # Documents
        self.customer_orders = CustomerOrderRepository(self.api_client)
        self.purchase_orders = PurchaseOrderRepository(self.api_client)
        self.invoiceouts = InvoiceOutRepository(self.api_client)
        self.demands = DemandRepository(self.api_client)
        self.supplies = SupplyRepository(self.api_client)
        self.cash_ins = CashInRepository(self.api_client)
        self.cash_outs = CashOutRepository(self.api_client)
        self.payment_ins = PaymentInRepository(self.api_client)
        self.payment_outs = PaymentOutRepository(self.api_client)

        # Counterparties
        self.counterparties = CounterpartyRepository(self.api_client)

        # Organization
        self.organizations = OrganizationRepository(self.api_client)
        self.employees = EmployeeRepository(self.api_client)
        self.stores = StoreRepository(self.api_client)

    def create_repository(self, entity_name: str, entity_class: Type[MetaEntity]) -> EntityRepository:
        """
        Create a custom repository for an entity type.

        Args:
            entity_name: Entity API endpoint name
            entity_class: Entity class

        Returns:
            Repository instance
        """
        return EntityRepository(self.api_client, entity_name, entity_class)

    def get_contexts(self) -> Dict:
        """
        Get user contexts.

        Returns:
            Context information
        """
        return self.api_client.get("context")

    def get_metadata(self, entity_name: str) -> Dict:
        """
        Get metadata for an entity type.

        Args:
            entity_name: Entity API endpoint name

        Returns:
            Metadata information
        """
        return self.api_client.get(f"{entity_name}/metadata")

    def get_audit(self, params: Optional[Dict] = None) -> Dict:
        """
        Get audit data.

        Args:
            params: Query parameters

        Returns:
            Audit information
        """
        return self.api_client.get("audit", params=params)

    def get_audit_events(self, audit_id: str, params: Optional[Dict] = None) -> Dict:
        """
        Get audit events by id.

        Args:
            audit_id: Audit ID
            params: Query parameters

        Returns:
            Audit events
        """
        return self.api_client.get(f"audit/{audit_id}/events", params=params)

    def search(self, query: str) -> Dict:
        """
        Perform a global search.

        Args:
            query: Search query

        Returns:
            Search results
        """
        return self.api_client.get("entity/search", params={"search": query})

    def get_custom_entities(self) -> List[Dict]:
        """
        Get a list of custom entities.

        Returns:
            List of custom entities
        """
        response = self.api_client.get("entity/customentity")
        return response.get("rows", [])

    def get_custom_entity(self, entity_id: str) -> Dict:
        """
        Get a custom entity by ID.

        Args:
            entity_id: Custom entity ID

        Returns:
            Custom entity information
        """
        return self.api_client.get(f"entity/customentity/{entity_id}")