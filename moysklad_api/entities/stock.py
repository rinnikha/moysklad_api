"""
Stock-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, ClassVar
from decimal import Decimal

from .base import Meta, MetaEntity


@dataclass
class Stock:
    """Stock entity in MoySklad."""

    meta: Optional[Meta] = None
    stock: Optional[Decimal] = None
    reserve: Optional[Decimal] = None
    inTransit: Optional[Decimal] = None
    quantity: Optional[Decimal] = None
    name: Optional[str] = None
    code: Optional[str] = None
    article: Optional[str] = None
    externalCode: Optional[str] = None
    assortment: Optional[Dict] = None
    folder: Optional[Dict] = None

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

        # Convert string to Decimal if needed
        for attr in ["stock", "reserve", "inTransit", "quantity"]:
            value = getattr(self, attr)
            if value is not None and not isinstance(value, Decimal):
                setattr(self, attr, Decimal(str(value)))

    @classmethod
    def from_dict(cls, data: Dict) -> "Stock":
        """
        Create stock entity from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new Stock instance
        """
        if not data:
            return None

        return cls(**data)


@dataclass
class StockFromReport:
    """Stock from report in MoySklad."""

    meta: Optional[Meta] = None
    code: Optional[str] = None
    reserve: Optional[Decimal] = None
    inTransit: Optional[Decimal] = None
    quantity: Optional[Decimal] = None
    name: Optional[str] = None
    code: Optional[str] = None
    article: Optional[str] = None
    externalCode: Optional[str] = None
    image: Optional[Meta] = None
    assortment: Optional[Dict] = None
    folder: Optional[Dict] = None
    price: Optional[float] = None
    salePrice: Optional[float] = None
    stock: Optional[float] = None
    stockDays: Optional[int] = None
    uom: Optional[Dict] = None

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

        # Convert string to Decimal if needed
        for attr in ["stock", "reserve", "inTransit", "quantity"]:
            value = getattr(self, attr)
            if value is not None and not isinstance(value, Decimal):
                setattr(self, attr, Decimal(str(value)))

    @classmethod
    def from_dict(cls, data: Dict) -> "Stock":
        """
        Create stock entity from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new Stock instance
        """
        if not data:
            return None

        return cls(**data)


@dataclass
class StockByOperation:
    """Stock by operation entity in MoySklad."""

    meta: Optional[Meta] = None
    stock: Optional[Decimal] = None
    operation: Optional[Dict] = None
    assortment: Optional[Dict] = None

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

        # Convert string to Decimal if needed
        if self.stock is not None and not isinstance(self.stock, Decimal):
            self.stock = Decimal(str(self.stock))

    @classmethod
    def from_dict(cls, data: Dict) -> "StockByOperation":
        """
        Create stock by operation entity from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new StockByOperation instance
        """
        if not data:
            return None

        return cls(**data)


@dataclass
class StockByStore:
    """Stock by store entity in MoySklad."""

    meta: Optional[Meta] = None
    stock: Optional[Decimal] = None
    reserve: Optional[Decimal] = None
    inTransit: Optional[Decimal] = None
    store: Optional[Dict] = None
    assortment: Optional[Dict] = None

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

        # Convert string to Decimal if needed
        for attr in ["stock", "reserve", "inTransit"]:
            value = getattr(self, attr)
            if value is not None and not isinstance(value, Decimal):
                setattr(self, attr, Decimal(str(value)))

    @classmethod
    def from_dict(cls, data: Dict) -> "StockByStore":
        """
        Create stock by store entity from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new StockByStore instance
        """
        if not data:
            return None

        return cls(**data)
