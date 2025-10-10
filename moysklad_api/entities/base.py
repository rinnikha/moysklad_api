"""
Base entity classes for the MoySklad API.
"""

from dataclasses import dataclass, asdict, fields, is_dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional, ClassVar, Type, TypeVar, Generic
from typing import Union, get_args, get_origin
from decimal import Decimal
from urllib.parse import urlparse
import inspect
import json
import types

from ..utils.helpers import ms_datetime_to_string

_UNION_TYPES = (Union,)
if hasattr(types, "UnionType"):
    _UNION_TYPES = _UNION_TYPES + (types.UnionType,)


def _convert_for_json(obj):
    """Convert special types to JSON-serializable formats and remove None values."""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, datetime):
        return ms_datetime_to_string(obj)  # Converts to ISO 8601 format string
    elif isinstance(obj, dict):
        # Filter out None values in dictionaries at any nesting level
        return {k: _convert_for_json(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        # Process each item in the list
        return [_convert_for_json(item) for item in obj]
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
    def create_default(cls, href: str = "") -> "Meta":
        """
        Create a default Meta object with minimal required fields.

        Args:
            href: The href URL (can be empty for new entities)

        Returns:
            A new Meta instance
        """
        return cls(href=href)

    @classmethod
    def from_dict(cls, data: Dict) -> "Meta":
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

@dataclass
class Attribute:
    """Attribute data of the entity"""

    meta: Optional[Meta] = None
    id: Optional[str] = None
    name: Optional[str] = None
    required: Optional[bool] = None
    customEntityMeta: Optional[Meta] = None
    file: Optional[Dict] = None
    show: Optional[bool] = None
    type: Optional[str] = None
    value: Optional[object] = None

    def __post_init__(self):
        if isinstance(self.meta, dict):
            self.meta = Meta(**self.meta)
        if isinstance(self.customEntityMeta, dict):
            self.customEntityMeta = Meta(**self.customEntityMeta)

    @classmethod
    def from_dict(cls, data: Dict) -> Optional["Attribute"]:
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


@dataclass
class MetaEntity:
    """Base class for all MoySklad entities with metadata."""

    meta: Optional[Meta] = None
    id: Optional[str] = None
    accountId: Optional[str] = None
    attributes: Optional[List[Attribute]] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    name: Optional[str] = None

    # Class variable to store entity type name
    entity_name: ClassVar[str] = ""

    def __post_init__(self):
        """Post-initialization hook to materialize nested entities based on type hints."""
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue

            converted = self._convert_field_value(field.type, value)
            setattr(self, field.name, converted)

    @classmethod
    def _convert_field_value(cls, annotation, value):
        """Convert field value into entity/dataclass instances when applicable."""
        if value is None:
            return None

        origin = get_origin(annotation)

        # Handle Optional/Union types (including PEP 604 unions)
        if origin in _UNION_TYPES:
            non_none_args = [arg for arg in get_args(annotation) if arg is not type(None)]
            if len(non_none_args) == 1:
                return cls._convert_field_value(non_none_args[0], value)
            return value

        # Handle collections (currently list/tuple are most common in API payloads)
        if origin in (list, tuple):
            if not isinstance(value, (list, tuple)):
                return value
            item_args = get_args(annotation)
            item_type = item_args[0] if item_args else Any
            converted_items = [
                cls._convert_field_value(item_type, item) for item in value
            ]
            return tuple(converted_items) if isinstance(value, tuple) else converted_items

        # Leave dictionaries as-is; caller can keep typing as Dict when raw payload expected
        if origin in (dict, Dict):
            return value

        if inspect.isclass(annotation):
            # Convert nested MetaEntity subclasses using their own from_dict logic
            if issubclass(annotation, MetaEntity):
                if isinstance(value, annotation):
                    return value
                if isinstance(value, dict):
                    return annotation.from_dict(value)
                return value

            # Convert other dataclasses (Meta, Attribute, Rate, etc.)
            if is_dataclass(annotation):
                if isinstance(value, annotation):
                    return value
                if isinstance(value, dict):
                    return annotation(**value)
                return value

        return value

    def get_id(self) -> Optional[str]:
        if self.id:
            return self.id

        if self.meta and self.meta.href:
            path_parts = [part for part in urlparse(self.meta.href).path.split("/") if part]

            if self.entity_name:
                entity_parts = [part for part in self.entity_name.split("/") if part]

                for index in range(len(path_parts) - len(entity_parts) + 1):
                    if path_parts[index : index + len(entity_parts)] == entity_parts:
                        candidate_index = index + len(entity_parts)
                        if candidate_index < len(path_parts):
                            return path_parts[candidate_index]

            if path_parts:
                return path_parts[-1]

        return None

    def get_href(self) -> Optional[str]:
        if self.id and self.entity_name:
            return f"https://api.moysklad.ru/api/remap/1.2/{self.entity_name}/{self.id}"
        return None

    def get_attribute_value(self, attribute_id: str):
        """Get value of attribute

        Args:
            attribute_id (str): Id of attribute

        Returns:
            object: value of attribute
        """
        if not self.attributes:
            return None

        for attribute in self.attributes:
            if attribute.id == attribute_id:
                return attribute.value
        return None

    @classmethod
    def get_href(cls, entity_id: str) -> Optional[str]:
        return f"https://api.moysklad.ru/api/remap/1.2/entity/{cls.entity_name}/{entity_id}"

    @classmethod
    def get_attribute_href(cls, attribute_id: str) -> Optional[str]:
        return f"https://api.moysklad.ru/api/remap/1.2/entity/{cls.entity_name}/metadata/attributes/{attribute_id}"

    def to_dict(self) -> Dict:
        """
        Convert entity to a dictionary for API requests.

        Returns:
            Dict representation of the entity
        """
        # Convert to dict using dataclasses.asdict
        data = asdict(self)

        # Convert special types (Decimal, datetime) for JSON serialization
        return _convert_for_json(data)

    @classmethod
    def from_dict(cls, data: Dict) -> "MetaEntity":
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


T = TypeVar("T", bound=MetaEntity)


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
    def from_dict(cls, data: Dict, entity_class: Type[T]) -> "ListEntity[T]":
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
            meta=Meta(**data.get("meta", {})), rows=rows, context=data.get("context")
        )
