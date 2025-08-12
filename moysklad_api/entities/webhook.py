"""
Webhook entity models for the MoySklad API.
"""

from dataclasses import dataclass
from typing import Dict, Optional, ClassVar

from .base import Meta, MetaEntity


@dataclass
class Webhook(MetaEntity):
    """Product variant entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/webhook"

    action: Optional[str] = None
    authorApplication: Optional[Meta] = None
    diffType: Optional[str] = None
    enabled: Optional[bool] = None
    entityType: Optional[str] = None
    method: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> "Webhook":
        """
        Create webhook entity from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new Webhook instance
        """
        if not data:
            return None

        return cls(**data)


@dataclass
class WebhookStock(MetaEntity):
    """Product variant entity in MoySklad."""

    entity_name: ClassVar[str] = "entity/webhookstock"

    enabled: Optional[bool] = None
    reportType: Optional[str] = None
    stockType: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> "WebhookStock":
        """
        Create webhook stock entity from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new WebhookStock instance
        """
        if not data:
            return None

        return cls(**data)
