"""
Document-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from datetime import datetime
from numbers import Number
from typing import Dict, List, Any, Optional, ClassVar
from decimal import Decimal

from .base import Meta, MetaEntity
from ..constants import DocumentStatus


@dataclass
class Position(MetaEntity):
    """Document position entity in MoySklad."""
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    vat: Optional[int] = None
    vatEnabled: Optional[bool] = None
    assortment: Optional[Dict] = None
    shipped: Optional[Decimal] = None
    reserve: Optional[Decimal] = None

    def __post_init__(self):
        """Convert string to Decimal if needed."""
        super().__post_init__()

        if isinstance(self.quantity, (str, int, float)):
            self.quantity = Decimal(str(self.quantity))

        if isinstance(self.price, (str, int, float)):
            self.price = Decimal(str(self.price))

        if isinstance(self.discount, (str, int, float)):
            self.discount = Decimal(str(self.discount))

@dataclass
class State(MetaEntity):
    """Document state entity in MoySklad."""
    color: Optional[Number] = None
    stateType: Optional[str] = None
    entityType: Optional[str] = None

    @staticmethod
    def get_href(entity_id: str, entity_type: str) -> str:
        return f'https://api.moysklad.ru/api/remap/1.2/entity/{entity_type}/metadata/states/{entity_id}'


@dataclass
class BaseDocument(MetaEntity):
    """Base document entity in MoySklad."""
    owner: Optional[Dict] = None
    shared: Optional[bool] = None
    group: Optional[Dict] = None
    description: Optional[str] = None
    externalCode: Optional[str] = None
    moment: Optional[datetime] = None
    applicable: Optional[bool] = None
    rate: Optional[Dict] = None
    sum: Optional[Decimal] = None
    syncId: Optional[str] = None
    project: Optional[Dict] = None
    state: Optional[Dict] = None
    deleted: Optional[bool] = None
    files: Optional[Dict] = None
    printed: Optional[bool] = None
    published: Optional[bool] = None

    def __post_init__(self):
        """Post-initialization hook."""
        super().__post_init__()


@dataclass
class CustomerOrder(BaseDocument):
    """Customer Order entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/customerorder"

    store: Optional[Dict] = None
    agent: Optional[Dict] = None
    shipmentAddress: Optional[Dict] = None
    shipmentAddressFull: Optional[Dict] = None
    shippedSum: Optional[Decimal] = None
    demands: Optional[List[Dict]] = None
    contract: Optional[Dict] = None
    salesChannel: Optional[Dict] = None
    syncId: Optional[str] = None
    taxSystem: Optional[str] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[Decimal] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    positions: Optional[Dict] = None
    deliveryPlannedMoment: Optional[datetime] = None
    payedSum: Optional[int] = None
    invoicesOut: Optional[List[Dict]] = None
    invoicedSum: Optional[int] = None
    reservedSum: Optional[int] = None

@dataclass
class PurchaseOrder(BaseDocument):
    """Customer Order entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/customerorder"

    store: Optional[Dict] = None
    agent: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    shippedSum: Optional[Decimal] = None
    supplies: Optional[List[Dict]] = None
    internalOrder: Optional[Dict] = None
    customerOrders: Optional[List[Dict]] = None
    contract: Optional[Dict] = None
    payments: Optional[List[Dict]] = None
    salesChannel: Optional[Dict] = None
    syncId: Optional[str] = None
    taxSystem: Optional[str] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[Decimal] = None
    waitSum: Optional[Decimal] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    positions: Optional[Dict] = None
    deliveryPlannedMoment: Optional[datetime] = None
    payedSum: Optional[int] = None
    invoicesOut: Optional[List[Dict]] = None
    invoicedSum: Optional[int] = None
    reservedSum: Optional[int] = None


@dataclass
class PurchaseReturn(BaseDocument):
    """Purchase Return entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/purchasereturn"

    code: Optional[str] = None
    store: Optional[Dict] = None
    agent: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    contract: Optional[Dict] = None
    payments: Optional[List[Dict]] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[Decimal] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    positions: Optional[Dict] = None
    supply: Optional[Dict] = None
    payedSum: Optional[int] = None
    factureIn: Optional[Dict] = None
    factureOut: Optional[Dict] = None


@dataclass
class SalesReturn(BaseDocument):
    """Sales Return entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/salesreturn"

    store: Optional[Dict] = None
    agent: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    contract: Optional[Dict] = None
    payments: Optional[List[Dict]] = None
    demand: Optional[List[Dict]] = None
    losses: Optional[List[Dict]] = None
    salesChannel: Optional[Dict] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[Decimal] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    positions: Optional[Dict] = None
    payedSum: Optional[int] = None
    factureOut: Optional[Dict] = None

@dataclass
class InvoiceOut(BaseDocument):
    """Invoice entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/invoiceout"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    positions: Optional[Dict] = None
    paymentPlannedMoment: Optional[datetime] = None
    payments: Optional[List[Dict]] = None
    demands: Optional[List[Dict]] = None
    customerOrder: Optional[Dict] = None
    contract: Optional[Dict] = None
    payedSum: Optional[int] = None
    salesChannel: Optional[Dict] = None
    shippedSum: Optional[Decimal] = None
    store: Optional[Dict] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[Decimal] = None


@dataclass
class Demand(BaseDocument):
    """Demand entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/demand"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    store: Optional[Dict] = None
    positions: Optional[Dict] = None
    customerOrder: Optional[Dict] = None
    invoicesOut: Optional[List[Dict]] = None
    payedSum: Optional[int] = None
    shipmentAddress: Optional[str] = None
    shipmentAddressFull: Optional[Dict] = None


@dataclass
class Supply(BaseDocument):
    """Supply entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/supply"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    store: Optional[Dict] = None
    positions: Optional[Dict] = None
    payedSum: Optional[int] = None
    invoicesIn: Optional[List[Dict]] = None
    incomingNumber: Optional[str] = None
    incomingDate: Optional[str] = None


@dataclass
class CashIn(BaseDocument):
    """Cash In entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/cashin"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    contract: Optional[Dict] = None
    paymentPurpose: Optional[str] = None
    operations: Optional[List[Dict]] = None
    factureIn: Optional[Dict] = None
    vatSum: Optional[int] = None
    retailShift: Optional[Dict] = None


@dataclass
class CashOut(BaseDocument):
    """Cash Out entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/cashout"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    contract: Optional[Dict] = None
    paymentPurpose: Optional[str] = None
    expenseItem: Optional[Dict] = None
    operations: Optional[List[Dict]] = None
    factureOut: Optional[Dict] = None
    vatSum: Optional[int] = None
    retailShift: Optional[Dict] = None


@dataclass
class PaymentIn(BaseDocument):
    """Payment In entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/paymentin"

    agent: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    contract: Optional[Dict] = None
    paymentPurpose: Optional[str] = None
    salesChannel: Optional[Dict] = None
    operations: Optional[List[Dict]] = None
    factureOut: Optional[Dict] = None
    vatSum: Optional[int] = None
    incomingNumber: Optional[str] = None
    incomingDate: Optional[str] = None


@dataclass
class PaymentOut(BaseDocument):
    """Payment Out entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/paymentout"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    contract: Optional[Dict] = None
    paymentPurpose: Optional[str] = None
    expenseItem: Optional[Dict] = None
    operations: Optional[List[Dict]] = None
    factureOut: Optional[Dict] = None
    vatSum: Optional[int] = None


@dataclass
class CounterpartyAdjustment(BaseDocument):
    """Counterparty adjustment entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/counterpartyadjustment"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None


@dataclass
class RetailDemand(BaseDocument):
    """Retail Demand entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/retaildemand"

    agent: Optional[Dict] = None
    organization: Optional[Dict] = None
    store: Optional[Dict] = None
    positions: Optional[Dict] = None
    retailStore: Optional[Dict] = None
    retailShift: Optional[Dict] = None
    cashSum: Optional[int] = None
    noCashSum: Optional[int] = None
    vatSum: Optional[int] = None
    fiscal: Optional[bool] = None

