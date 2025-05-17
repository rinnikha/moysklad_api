"""
Base entity classes for the MoySklad API.
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Any, Optional, ClassVar, Type, TypeVar, Generic
from decimal import Decimal
import json

def _convert_for_json(obj):
    """Convert special types to JSON-serializable formats."""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()  # Converts to ISO 8601 format string
    elif isinstance(obj, dict):
        return {k: _convert_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_for_json(item) for item in item]
    return obj


@dataclass
class Meta:
    """Represents MoySklad entity metadata."""
    href: str
    metadataHref: Optional[str] = None
    type: Optional[str] = None
    mediaType: Optional[str] = None
    uuidHref: Optional[str] = None
    downloadHref: Optional[str] = None
    nextHref: Optional[str] = None
    previousHref: Optional[str] = None
    size: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    @classmethod
    def create_default(cls, href: str = "") -> 'Meta':
        """
        Create a default Meta object with minimal required fields.

        Args:
            href: The href URL (can be empty for new entities)

        Returns:
            A new Meta instance
        """
        return cls(href=href)


@dataclass
class MetaEntity:
    """Base class for all MoySklad entities with metadata."""
    meta: Optional[Meta] = None
    id: Optional[str] = None
    accountId: Optional[str] = None
    attributes: Optional[List[Dict]] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    name: Optional[str] = None

    # Class variable to store entity type name
    entity_name: ClassVar[str] = ""

    def __post_init__(self):
        """
        Post-initialization hook to convert dict to Meta object
        if needed.
        """
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

    def to_dict(self) -> Dict:
        """
        Convert entity to a dictionary for API requests.

        Returns:
            Dict representation of the entity
        """
        # Convert to dict using dataclasses.asdict
        data = asdict(self)

        # Remove None values
        filtered_data = {k: v for k, v in data.items() if v is not None}

        # Convert special types (Decimal, datetime) for JSON serialization
        return _convert_for_json(filtered_data)


    @classmethod
    def from_dict(cls, data: Dict) -> 'MetaEntity':
        """
        Create an entity from a dictionary.

        Args:
            data: Dictionary data from API

        Returns:
            A new entity instance
        """

        if not data:
            return None
        return cls(**data)


T = TypeVar('T', bound=MetaEntity)


@dataclass
class ListEntity(Generic[T]):
    """Represents a list of entities from the MoySklad API."""
    meta: Meta
    rows: List[T]
    context: Optional[Dict] = None

    def __post_init__(self):
        """
        Post-initialization hook to convert dict to Meta object
        if needed.
        """
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)

    @classmethod
    def from_dict(cls, data: Dict, entity_class: Type[T]) -> 'ListEntity[T]':
        """
        Create a list entity from API response.

        Args:
            data: Dictionary data from API
            entity_class: The entity class to use for rows

        Returns:
            A new ListEntity instance
        """
        if not data:
            return None

        # Convert row data to entity objects
        rows = [entity_class.from_dict(row) for row in data.get("rows", [])]

        return cls(
            meta=Meta(**data.get("meta", {})),
            rows=rows,
            context=data.get("context")
        )