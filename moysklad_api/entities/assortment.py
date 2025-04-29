"""
Assortment-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, ClassVar, Union
from decimal import Decimal

from .base import Meta, MetaEntity
from ..constants import PaymentItemType, TrackingType


@dataclass
class Assortment(MetaEntity):
    """
    Assortment entity in MoySklad.

    Assortment is a generic entity type that can represent products, variants, services,
    bundles (kits), or other items that can be part of inventory.
    """
    entity_name: ClassVar[str] = "entity/assortment"

    # Common fields for all assortment types
    code: Optional[str] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    vat: Optional[int] = None
    shared: Optional[bool] = None
    pathName: Optional[str] = None
    effectiveVat: Optional[int] = None
    productFolder: Optional[Dict] = None
    uom: Optional[Dict] = None
    minPrice: Optional[Dict] = None
    buyPrice: Optional[Dict] = None
    salePrices: Optional[List[Dict]] = None
    supplier: Optional[Dict] = None
    attributes: Optional[List[Dict]] = None
    images: Optional[Dict] = None
    barcodes: Optional[List[Dict]] = None
    paymentItemType: Optional[str] = None
    discountProhibited: Optional[bool] = None
    owner: Optional[Dict] = None
    article: Optional[str] = None
    weighed: Optional[bool] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    variantsCount: Optional[int] = None
    effectiveVatEnabled: Optional[bool] = None
    stock: Optional[Decimal] = None
    reserve: Optional[Decimal] = None
    inTransit: Optional[Decimal] = None
    quantity: Optional[Decimal] = None
    packs: Optional[List[Dict]] = None
    vatEnabled: Optional[bool] = None
    useParentVat: Optional[bool] = None
    isSerialTrackable: Optional[bool] = None
    trackingType: Optional[str] = None
    group: Optional[Dict] = None
    files: Optional[Dict] = None

    # Fields specific to certain types
    alcoholic: Optional[Dict] = None
    archived: Optional[bool] = None
    country: Optional[Dict] = None
    components: Optional[List[Dict]] = None  # For bundles/kits
    characteristics: Optional[List[Dict]] = None  # For variants
    product: Optional[Dict] = None  # For variants, references parent product

    # Type information
    productType: Optional[str] = None  # product, variant, service, bundle

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

    @property
    def is_product(self) -> bool:
        """Check if this assortment item is a product."""
        return self.productType == "product"

    @property
    def is_variant(self) -> bool:
        """Check if this assortment item is a variant."""
        return self.productType == "variant"

    @property
    def is_service(self) -> bool:
        """Check if this assortment item is a service."""
        return self.productType == "service"

    @property
    def is_bundle(self) -> bool:
        """Check if this assortment item is a bundle/kit."""
        return self.productType == "bundle"


@dataclass
class AssortmentSettings:
    """Settings for assortment in MoySklad."""
    meta: Meta
    priceTypes: List[Dict]
    barcodeRules: Optional[Dict] = None

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)


@dataclass
class Service(MetaEntity):
    """Service entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/service"

    code: Optional[str] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    vat: Optional[int] = None
    effectiveVat: Optional[int] = None
    buyPrice: Optional[Dict] = None
    discountProhibited: Optional[bool] = False
    minPrice: Optional[Dict] = None
    salePrices: Optional[List[Dict]] = None
    uom: Optional[Dict] = None
    owner: Optional[Dict] = None
    shared: Optional[bool] = None
    group: Optional[Dict] = None
    pathName: Optional[str] = None
    productFolder: Optional[Dict] = None
    syncId: Optional[str] = None
    taxSystem: Optional[str] = None
    useParentVat: Optional[bool] = None
    vatEnabled: Optional[bool] = None
    files: Optional[List[Dict]] = None
    effectiveVatEnabled: Optional[bool] = None
    barcodes: Optional[List[Dict]] = None
    attributes: Optional[List[Dict]] = None
    paymentItemType: Optional[str] = None
    archived: Optional[bool] = None

    def __post_init__(self):
        """Post-initialization hook."""
        super().__post_init__()

        if isinstance(self.paymentItemType, str):
            try:
                self.paymentItemType = PaymentItemType(self.paymentItemType)
            except ValueError:
                pass


@dataclass
class Bundle(MetaEntity):
    """Bundle (kit) entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/bundle"

    components: Optional[List[Dict]] = None
    code: Optional[str] = None
    country: Optional[Dict] = None
    group: Optional[Dict] = None
    overhead: Optional[Dict] = None
    owner: Optional[Dict] = None
    partialDisposal: Optional[bool] = None
    pathName: Optional[str] = None
    productFolder: Optional[Dict] = None
    shared: Optional[bool] = None
    syncId: Optional[str] = None
    taxSystem: Optional[str] = None
    tnved: Optional[str] = None
    trackingType: Optional[str] = None
    uom: Optional[Dict] = None
    effectiveVatEnabled: Optional[bool] = None
    useParentVat: Optional[bool] = None
    vatEnabled: Optional[bool] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    files: Optional[List[Dict]] = None
    vat: Optional[int] = None
    effectiveVat: Optional[int] = None
    discountProhibited: Optional[bool] = None
    minPrice: Optional[Dict] = None
    salePrices: Optional[List[Dict]] = None
    article: Optional[str] = None
    attributes: Optional[List[Dict]] = None
    images: Optional[Dict] = None
    barcodes: Optional[List[Dict]] = None
    paymentItemType: Optional[str] = None
    archived: Optional[bool] = None
    weight: Optional[float] = None
    volume: Optional[float] = None

    def __post_init__(self):
        """Post-initialization hook."""
        super().__post_init__()

        if self.components is None:
            raise ValueError("Components are required for bundles")

        if isinstance(self.paymentItemType, str):
            try:
                self.paymentItemType = PaymentItemType(self.paymentItemType)
            except ValueError:
                pass