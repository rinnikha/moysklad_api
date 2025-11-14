"""
Entity base classes for MoySklad.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
from datetime import datetime
from decimal import Decimal
import inspect
import types
import sys
from functools import lru_cache
from typing import Any, ClassVar, Dict, Generic, List, Optional, Type, TypeVar, Union, get_args, get_origin, get_type_hints
from urllib.parse import urlparse

from ...utils.helpers import ms_datetime_to_string
from .attributes import Attribute, AttributeCollection
from .meta import Meta

_UNION_TYPES = (Union,)
if hasattr(types, "UnionType"):
    _UNION_TYPES = _UNION_TYPES + (types.UnionType,)  # type: ignore[assignment]


def _convert_for_json(obj):
    """Convert special types to JSON-serializable formats and remove None values."""
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return ms_datetime_to_string(obj)  # Converts to ISO 8601 format string
    if is_dataclass(obj):
        return _convert_for_json(asdict(obj))
    if isinstance(obj, dict):
        # Filter out None values in dictionaries at any nesting level
        return {k: _convert_for_json(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, (list, tuple)):
        # Process each item in the sequence
        return [_convert_for_json(item) for item in obj]
    if isinstance(obj, AttributeCollection):
        return [_convert_for_json(item) for item in list(obj)]
    return obj


def _get_resolved_type_hints(cls: Type) -> Dict[str, Any]:
    """Return cached typing hints for the provided class."""
    module_dict = sys.modules[cls.__module__].__dict__
    base_module_dict = sys.modules[MetaEntity.__module__].__dict__
    combined_globals = {**base_module_dict, **module_dict}
    return get_type_hints(cls, globalns=combined_globals, localns=combined_globals)


_get_resolved_type_hints = lru_cache(maxsize=None)(_get_resolved_type_hints)


@dataclass
class MetaEntity:
    """Base class for all MoySklad entities with metadata."""

    meta: Optional[Meta] = None
    id: Optional[str] = None
    accountId: Optional[str] = None
    attributes: Optional[AttributeCollection] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    name: Optional[str] = None

    # Class variable to store entity type name
    entity_name: ClassVar[str] = ""

    def __post_init__(self):
        """Post-initialization hook to materialize nested entities based on type hints."""
        type_hints = _get_resolved_type_hints(type(self))
        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue

            annotation = type_hints.get(field.name, field.type)
            converted = self._convert_field_value(annotation, value)
            setattr(self, field.name, converted)

        self._bind_attribute_collection()

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
                    # Filter out unknown fields for other dataclasses too
                    known_fields = {f.name for f in fields(annotation)}
                    filtered_value = {k: v for k, v in value.items() if k in known_fields}
                    return annotation(**filtered_value)
                return value

        return value

    def _bind_attribute_collection(self) -> None:
        if self.attributes is None:
            return
        if isinstance(self.attributes, AttributeCollection):
            self.attributes.bind(self)
            return
        # If attributes were provided as a plain list, convert them
        self.attributes = AttributeCollection(self.attributes, owner=self)

    def _get_attribute_collection(self) -> AttributeCollection:
        if self.attributes is None:
            self.attributes = AttributeCollection(owner=self)
        elif not isinstance(self.attributes, AttributeCollection):
            self.attributes = AttributeCollection(self.attributes, owner=self)
        else:
            self.attributes.bind(self)
        return self.attributes

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

    def add_attribute(self, attribute_id: str, value: object, **extra_fields) -> Optional[Attribute]:
        """Add attribute with meta and value to entity."""
        if not self.entity_name:
            return None

        collection = self._get_attribute_collection()
        return collection.add(attribute_id, value, **extra_fields)

    def create_or_update_attribute(self, attribute_id: str, value: object, **extra_fields) -> Optional[Attribute]:
        """Update an existing attribute or create one if it does not exist."""
        if not self.entity_name:
            return None

        collection = self._get_attribute_collection()
        return collection.update(attribute_id, value, **extra_fields)

    def remove_attribute(self, attribute_id: str) -> Optional[Attribute]:
        """Remove attribute by identifier."""
        if not self.attributes:
            return None
        self._bind_attribute_collection()
        return self.attributes.remove_by_id(attribute_id)

    def get_attribute_value(self, attribute_id: str):
        """Get value of attribute."""
        if not self.attributes:
            return None
        self._bind_attribute_collection()
        return self.attributes.get_value(attribute_id)

    @classmethod
    def get_href(cls, entity_id: str) -> Optional[str]:
        return f"https://api.moysklad.ru/api/remap/1.2/{cls.entity_name}/{entity_id}"

    @classmethod
    def get_attribute_href(cls, attribute_id: str) -> Optional[str]:
        return f"https://api.moysklad.ru/api/remap/1.2/{cls.entity_name}/metadata/attributes/{attribute_id}"

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

        # Filter out unknown fields to handle future API additions gracefully
        known_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}

        return cls(**filtered_data)


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
