"""
Metadata-related entity models for the MoySklad API.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, ClassVar, Union

from .base import Meta, MetaEntity


@dataclass
class AttributeDefinition:
    """Custom attribute definition entity in MoySklad."""
    name: str
    type: str
    required: bool
    meta: Meta  # Moving meta from the parent class
    description: Optional[str] = None
    customEntityMeta: Optional[Dict] = None
    id: Optional[str] = None
    accountId: Optional[str] = None
    updated: Optional[str] = None

    # Possible types:
    # string, long, time, file, double, boolean, text, link
    # date, customentity, dictionary

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)


@dataclass
class CustomEntity(MetaEntity):
    """Custom entity in MoySklad."""
    entity_name: ClassVar[str] = "entity/customentity"

    code: Optional[str] = None
    externalCode: Optional[str] = None
    description: Optional[str] = None
    vat: Optional[int] = None
    effectiveVat: Optional[int] = None
    owner: Optional[Dict] = None
    shared: Optional[bool] = None
    group: Optional[Dict] = None
    updated: Optional[str] = None


@dataclass
class Metadata:
    """Metadata for entity types in MoySklad."""
    meta: Meta
    attributes: Optional[List[AttributeDefinition]] = None
    states: Optional[List[Dict]] = None
    createShared: Optional[bool] = None

    def __post_init__(self):
        """Post-initialization hook."""
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

        if self.attributes:
            self.attributes = [
                attr if isinstance(attr, AttributeDefinition) else AttributeDefinition(**attr)
                for attr in self.attributes
            ]

    @classmethod
    def from_dict(cls, data: Dict) -> 'Metadata':
        """
        Create metadata from API response.

        Args:
            data: Dictionary data from API

        Returns:
            A new Metadata instance
        """
        if not data:
            return None

        attributes = data.get("attributes", [])
        processed_attributes = []

        for attr in attributes:
            processed_attributes.append(AttributeDefinition(**attr))

        return cls(
            meta=Meta(**data.get("meta", {})),
            attributes=processed_attributes,
            states=data.get("states"),
            createShared=data.get("createShared")
        )