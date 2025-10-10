"""
Document-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urlparse
from numbers import Number
from typing import Dict, List, Any, Optional, ClassVar
from decimal import Decimal

from moysklad_api.entities.organization import Organization
from moysklad_api.entities.products import Currency

from .base import Meta, MetaEntity
from ..constants import DocumentStatus


@dataclass
class Position(MetaEntity):
    """Document position entity in MoySklad."""

    cost: Optional[float] = None
    country: Optional[Meta] = None
    gtd: Optional[Dict] = None
    quantity: Optional[float] = None
    pack: Optional[Dict] = None
    price: Optional[Decimal] = None
    slot: Optional[Meta] = None
    things: Optional[List[str]] = None
    trackingCodes: Optional[List[Dict]] = None
    trackingCodes_1162: Optional[List[Dict]] = None
    overhead: Optional[float] = None
    discount: Optional[Decimal] = None
    declaration: Optional[List[Dict]] = None
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


@dataclass
class Rate:
    """Document rate object with currency and rate"""
    currency: Optional[Currency] = None
    value: Optional[float] = 1

    def __post_init__(self):
        if isinstance(self.currency, dict):
            self.currency = Currency(**self.currency)



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
    rate: Optional[Rate] = None
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

        if isinstance(self.rate, dict):
            self.rate = Rate(**self.rate)

    def extract_id_from_href(self, href: str):
        path = urlparse(href).path
        parts = path.strip("/").split("/")

        if self.entity_name in parts:
            idx = parts.index(self.entity_name)
            if idx + 1 < len(parts):
                return parts[idx + 1]
        return None




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
    payments: Optional[List[Dict]] = None
    invoicesOut: Optional[List[Dict]] = None
    invoicedSum: Optional[int] = None
    reservedSum: Optional[int] = None


@dataclass
class PurchaseOrder(BaseDocument):
    """Customer Order entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/purchaseorder"

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
    agentAccount: Optional[Dict] = None
    code: Optional[str] = None
    contract: Optional[Dict] = None
    customerOrder: Optional[Dict] = None
    factureOut: Optional[Dict] = None
    returns: Optional[Dict] = None
    organization: Optional[Dict] = None
    organizationAccount: Optional[Dict] = None
    overhead: Optional[Dict] = None
    salesChannel: Optional[Dict] = None
    store: Optional[Dict] = None
    positions: Optional[Dict] = None
    customerOrder: Optional[Dict] = None
    invoicesOut: Optional[List[Dict]] = None
    payedSum: Optional[int] = None
    payments: Optional[Dict] = None
    shipmentAddress: Optional[str] = None
    shipmentAddressFull: Optional[Dict] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[float] = None


@dataclass
class Supply(BaseDocument):
    """Supply entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/supply"

    agent: Optional[Dict] = None
    organization: Optional[Organization] = None
    organizationAccount: Optional[Dict] = None
    overhead: Optional[Dict] = None
    agentAccount: Optional[Dict] = None
    store: Optional[Dict] = None
    factureIn: Optional[Meta] = None
    positions: Optional[Dict] = None
    payedSum: Optional[int] = None
    payments: Optional[List[Meta]] = None
    purchaseOrder: Optional[Meta] = None
    returns: Optional[List[Meta]] = None
    productionTask: Optional[Meta] = None
    invoicesIn: Optional[List[Dict]] = None
    incomingNumber: Optional[str] = None
    incomingDate: Optional[str] = None
    vatEnabled: Optional[bool] = None
    vatIncluded: Optional[bool] = None
    vatSum: Optional[float] = None


@dataclass
class CashIn(BaseDocument):
    """Cash In entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/cashin"

    agent: Optional[MetaEntity] = None
    code: Optional[str] = None
    organization: Optional[Organization] = None
    contract: Optional[Dict] = None
    paymentPurpose: Optional[str] = None
    salesChannel: Optional[Dict] = None
    operations: Optional[List[Dict]] = None
    factureIn: Optional[Dict] = None
    vatSum: Optional[int] = None


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


@dataclass
class Enter(BaseDocument):
    """Product Entere to store in MoySklad."""

    entity_name: ClassVar[str] = "entity/enter"

    organization: Optional[Dict] = None
    overhead: Optional[Dict] = None
    positions: Optional[Dict] = None
    store: Optional[Dict] = None
    inventory: Optional[Dict] = None


@dataclass
class Loss(BaseDocument):
    """Product loss from store in MoySklad"""

    entity_name: ClassVar[str] = "entity/loss"

    organization: Optional[Dict] = None
    overhead: Optional[Dict] = None
    positions: Optional[Dict] = None
    store: Optional[Dict] = None
    salesReturn: Optional[Dict] = None
    inventory: Optional[Dict] = None
