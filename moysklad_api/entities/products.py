"""
Product-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, ClassVar
from decimal import Decimal

from .base import Meta, MetaEntity
from ..constants import PaymentItemType, TrackingType


@dataclass
class Barcode(MetaEntity):
    """Barcode entity in MoySklad."""

    ean13: Optional[str] = None
    ean8: Optional[str] = None
    code128: Optional[str] = None
    gtin: Optional[str] = None
    upc: Optional[str] = None


@dataclass
class Image(MetaEntity):
    """Image entity in MoySklad."""

    filename: Optional[str] = None
    miniature: Optional[Dict] = None
    tiny: Optional[Dict] = None
    title: Optional[str] = None


@dataclass
class ProductFolder(MetaEntity):
    """Product folder entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/productfolder"

    pathName: Optional[str] = None
    code: Optional[str] = None
    externalCode: Optional[str] = None
    archived: Optional[bool] = None
    vat: Optional[int] = None
    vatEnabled: Optional[bool] = None
    effectiveVat: Optional[int] = None
    effectiveVatEnabled: Optional[bool] = None
    useParentVat: Optional[bool] = None
    taxSystem: Optional[str] = None
    shared: Optional[bool] = None
    owner: Optional[Dict] = None
    group: Optional[Dict] = None
    productFolder: Optional[Dict] = None
    description: Optional[str] = None

    created: Optional[datetime] = None
    updated: Optional[datetime] = None


@dataclass
class Currency(MetaEntity):
    """Currency entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/currency"

    code: Optional[str] = None
    default: Optional[Decimal] = None
    fullName: Optional[str] = None
    indirect: Optional[bool] = None
    isoCode: Optional[str] = None
    majorUnit: Optional[Dict] = None
    minorUnit: Optional[Dict] = None
    margin: Optional[Decimal] = None
    multiplicity: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    rateUpdateType: Optional[str] = None
    system: Optional[bool] = None
    archived: Optional[bool] = None

@dataclass
class Price:
    """Price entity in MoySklad."""

    value: Decimal
    currency: Optional[Currency] = None
    priceType: Optional[Dict] = None

    def __post_init__(self):
        """Convert string to Decimal if needed."""
        if isinstance(self.currency, dict):
            self.currency = Currency(**self.currency)

        if isinstance(self.value, (str, int, float)):
            self.value = Decimal(str(self.value))

@dataclass
class PriceType(MetaEntity):
    """Price type entity in MoySklad."""

    entity_name: ClassVar[str] = "context/companysettings/pricetype"

    externalCode: Optional[str] = None


@dataclass
class Uom(MetaEntity):
    """Unit of measurement entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/uom"

    code: Optional[str] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[Dict] = None
    group: Optional[Dict] = None
    shared: Optional[bool] = None


@dataclass
class Product(MetaEntity):
    """Product entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/product"

    code: Optional[str] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    vat: Optional[int] = None
    syncId: Optional[str] = None
    effectiveVat: Optional[int] = None
    productFolder: Optional[Dict] = None
    uom: Optional[Dict] = None
    images: Optional[Dict] = None
    minPrice: Optional[Dict] = None
    buyPrice: Optional[Dict] = None
    salePrices: Optional[List[Dict]] = None
    supplier: Optional[Dict] = None
    country: Optional[Dict] = None
    article: Optional[str] = None
    weighed: Optional[bool] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    vatEnabled: Optional[bool] = None
    pathName: Optional[str] = None
    barcodes: Optional[List[Dict]] = None
    variantsCount: Optional[int] = None
    isSerialTrackable: Optional[bool] = None
    trackingType: Optional[str] = None
    paymentItemType: Optional[str] = None
    discountProhibited: Optional[bool] = None
    shared: Optional[bool] = None
    archived: Optional[bool] = None
    owner: Optional[Dict] = None
    group: Optional[Dict] = None
    files: Optional[Dict] = None
    effectiveVatEnabled: Optional[bool] = None
    useParentVat: Optional[bool] = None
    taxSystem: Optional[str] = None
    packs: Optional[List[Dict]] = None

    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization hook."""
        super().__post_init__()

        # Convert string enum values to actual enum values if needed
        if isinstance(self.trackingType, str):
            try:
                self.trackingType = TrackingType(self.trackingType)
            except ValueError:
                pass

        if isinstance(self.paymentItemType, str):
            try:
                self.paymentItemType = PaymentItemType(self.paymentItemType)
            except ValueError:
                pass


@dataclass
class Variant(MetaEntity):
    """Product variant entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/variant"

    code: Optional[str] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    vat: Optional[int] = None
    effectiveVat: Optional[int] = None
    discountProhibited: Optional[bool] = None
    minPrice: Optional[Dict] = None
    buyPrice: Optional[Dict] = None
    salePrices: Optional[List[Dict]] = None
    barcodes: Optional[List[Dict]] = None
    product: Optional[Dict] = None
    characteristics: Optional[List[Dict]] = None
    images: Optional[Dict] = None
    archived: Optional[bool] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    isSerialTrackable: Optional[bool] = None
    trackingType: Optional[str] = None
