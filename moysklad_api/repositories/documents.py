"""
Document-related repositories for the MoySklad API.
"""
from http.client import responses
from typing import Dict, List, Any, Optional, Tuple

from build.lib.moysklad_api.entities import Counterparty
from .base import EntityRepository
from ..api_client import ApiClient
from ..entities.documents import (
    CustomerOrder,
    InvoiceOut,
    Demand,
    Supply,
    CashIn,
    CashOut,
    PaymentIn,
    PaymentOut, Position, PurchaseOrder
)
from ..entities.base import Meta, ListEntity
from ..query import QueryBuilder


class CustomerOrderRepository(EntityRepository[CustomerOrder]):
    """Repository for CustomerOrder entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize customer order repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/customerorder", CustomerOrder)

    def get_metadata(self) -> Dict:
        """
        Get customer order metadata.

        Returns:
            Metadata dictionary
        """
        return self.api_client.get(f"{self.entity_name}/metadata")

    def get_by_agent(self, agent_id: str, query_builder: Optional[QueryBuilder] = None) -> Tuple[
        List[CustomerOrder], Meta]:
        """
        Get orders by agent (counterparty).

        Args:
            agent_id: Agent (counterparty) ID
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of orders, metadata)
        """
        query = query_builder or self.query()
        query.filter().eq("agent.id", agent_id)

        return self.find_all(query)

    def get_positions(self, order_id: str, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Position], Meta]:
        """
        Get order positions.

        Args:
            order_id: Order ID
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Positions data
        """

        params = query_builder if query_builder else self.query()
        params.expand("assortment")

        response = self.api_client.get(f"{self.entity_name}/{order_id}/positions", params=params.to_params())

        list_positions = ListEntity.from_dict(response, Position)

        return list_positions.rows, list_positions.meta

    def get_agent(self, order_id: str, expand=False) -> Counterparty:
        """
        Get order agent.

        Args:
            order_id: Order ID
            expand: Expand bool

        Returns:
            Counterparty meta, if expand is true, then full Counterparty data
        """
        params = self.query()

        if expand:
            params.expand("agent")

        response = self.api_client.get(f"{self.entity_name}/{order_id}", params=params.to_params())

        return Counterparty.from_dict(response['agent'])

    def create_position(self, order_id: str, position_data: Position) -> Dict:
        """
        Create order position.

        Args:
            order_id: Order ID
            position_data: Position data

        Returns:
            Created position data
        """

        data = position_data.to_dict()
        response = self.api_client.post(f"{self.entity_name}/{order_id}/positions", data=data)

        return Position.from_dict(response[0])

    def update_position(self, order_id: str, position_id: str, position_data: Dict) -> Dict:
        """
        Update order position.

        Args:
            order_id: Order ID
            position_id: Position ID
            position_data: Position data

        Returns:
            Updated position data
        """
        return self.api_client.put(f"{self.entity_name}/{order_id}/positions/{position_id}", data=position_data)

    def delete_position(self, order_id: str, position_id: str) -> None:
        """
        Delete order position.

        Args:
            order_id: Order ID
            position_id: Position ID
        """
        self.api_client.delete(f"{self.entity_name}/{order_id}/positions/{position_id}")



class PurchaseOrderRepository(EntityRepository[PurchaseOrder]):
    """Repository for PurchaseOrder entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize purchase order repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/purchaseorder", PurchaseOrder)

    def get_metadata(self) -> Dict:
        """
        Get purchase order metadata.

        Returns:
            Metadata dictionary
        """
        return self.api_client.get(f"{self.entity_name}/metadata")

    def get_by_agent(self, agent_id: str, query_builder: Optional[QueryBuilder] = None) -> Tuple[
        List[PurchaseOrder], Meta]:
        """
        Get orders by agent (counterparty).

        Args:
            agent_id: Agent (counterparty) ID
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Tuple of (list of orders, metadata)
        """
        query = query_builder or self.query()
        query.filter().eq("agent.id", agent_id)

        return self.find_all(query)

    def get_positions(self, order_id: str, query_builder: Optional[QueryBuilder] = None) -> Tuple[List[Position], Meta]:
        """
        Get order positions.

        Args:
            order_id: Order ID
            query_builder: Query builder for filtering, sorting, etc.

        Returns:
            Positions data
        """
        params = query_builder.to_params() if query_builder else {}
        response = self.api_client.get(f"{self.entity_name}/{order_id}/positions", params=params)

        list_positions = ListEntity.from_dict(response, Position)

        return list_positions.rows, list_positions.meta

    def create_position(self, order_id: str, position_data: Position) -> Dict:
        """
        Create order position.

        Args:
            order_id: Order ID
            position_data: Position data

        Returns:
            Created position data
        """

        data = position_data.to_dict()
        response = self.api_client.post(f"{self.entity_name}/{order_id}/positions", data=data)

        return Position.from_dict(response[0])

    def update_position(self, order_id: str, position_id: str, position_data: Dict) -> Dict:
        """
        Update order position.

        Args:
            order_id: Order ID
            position_id: Position ID
            position_data: Position data

        Returns:
            Updated position data
        """
        return self.api_client.put(f"{self.entity_name}/{order_id}/positions/{position_id}", data=position_data)

    def delete_position(self, order_id: str, position_id: str) -> None:
        """
        Delete order position.

        Args:
            order_id: Order ID
            position_id: Position ID
        """
        self.api_client.delete(f"{self.entity_name}/{order_id}/positions/{position_id}")


class InvoiceOutRepository(EntityRepository[InvoiceOut]):
    """Repository for InvoiceOut entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize invoiceout repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/invoiceout", InvoiceOut)

    def get_by_customer_order(self, order_href: str) -> List[InvoiceOut]:
        """
        Get invoices by customer order href.

        Args:
            order_href: Customer order href

        Returns:
            List of invoices
        """
        query = self.query()
        query.filter().eq("customerOrder", order_href)

        invoices, _ = self.find_all(query)
        return invoices


class DemandRepository(EntityRepository[Demand]):
    """Repository for Demand entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize demand repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/demand", Demand)

    def get_by_customer_order(self, order_id: str) -> List[Demand]:
        """
        Get demands by customer order.

        Args:
            order_id: Customer order ID

        Returns:
            List of demands
        """
        query = self.query()
        query.filter().eq("customerOrder.id", order_id)

        demands, _ = self.find_all(query)
        return demands


class SupplyRepository(EntityRepository[Supply]):
    """Repository for Supply entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize supply repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/supply", Supply)


class CashInRepository(EntityRepository[CashIn]):
    """Repository for CashIn entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize cash-in repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/cashin", CashIn)


class CashOutRepository(EntityRepository[CashOut]):
    """Repository for CashOut entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize cash-out repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/cashout", CashOut)


class PaymentInRepository(EntityRepository[PaymentIn]):
    """Repository for PaymentIn entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize payment-in repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/paymentin", PaymentIn)

    def get_by_customer_order(self, order_id: str) -> List[PaymentIn]:
        """
        Get payment-ins by customer order.

        Args:
            order_id: Customer order ID

        Returns:
            List of payment-ins
        """
        query = self.query()
        query.filter().eq("operations.customerorder.id", order_id)

        payments, _ = self.find_all(query)
        return payments


class PaymentOutRepository(EntityRepository[PaymentOut]):
    """Repository for PaymentOut entities."""

    def __init__(self, api_client: ApiClient):
        """
        Initialize payment-out repository.

        Args:
            api_client: API client instance
        """
        super().__init__(api_client, "entity/paymentout", PaymentOut)