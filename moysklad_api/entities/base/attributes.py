"""
Attribute models and helpers for MoySklad entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional, TYPE_CHECKING, Union

from .meta import Meta

if TYPE_CHECKING:
    from .entity import MetaEntity


@dataclass
class Attribute:
    """Attribute data of the entity."""

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
        Create an attribute from a dictionary.

        Args:
            data: Dictionary data from API

        Returns:
            A new attribute instance
        """

        if not data:
            return None
        return cls(**data)


class AttributeCollection(list):
    """
    Helper collection for working with entity attributes.

    Provides convenient helpers while still behaving like a regular list,
    so it remains compatible with the API client's expectations.
    """

    def __init__(
        self,
        iterable: Optional[Iterable[Union[Attribute, Dict]]] = None,
        *,
        owner: Optional["MetaEntity"] = None,
    ):
        iterable = iterable or []
        super().__init__(self._ensure_attribute(item) for item in iterable)
        self._owner: Optional["MetaEntity"] = owner

    def bind(self, owner: "MetaEntity") -> "AttributeCollection":
        """Bind the collection to an owning entity."""
        self._owner = owner
        return self

    # Mutating list API -------------------------------------------------
    def append(self, item: Union[Attribute, Dict]) -> None:  # type: ignore[override]
        super().append(self._ensure_attribute(item))

    def extend(self, other: Iterable[Union[Attribute, Dict]]) -> None:  # type: ignore[override]
        super().extend(self._ensure_attribute(item) for item in other)

    def insert(self, index: int, item: Union[Attribute, Dict]) -> None:  # type: ignore[override]
        super().insert(index, self._ensure_attribute(item))

    # Helpers -----------------------------------------------------------
    def add(
        self,
        attribute_id: str,
        value: object,
        *,
        meta: Optional[Meta] = None,
        **extra_fields,
    ) -> Attribute:
        """
        Append a new attribute with the provided value.

        Args:
            attribute_id: Identifier of the attribute metadata.
            value: Value to assign to the attribute.
            meta: Optional explicit metadata. Generated automatically if omitted.
            extra_fields: Any additional Attribute fields to set.
        """
        attribute_meta = meta or self._build_meta(attribute_id)
        attribute = Attribute(
            id=attribute_id,
            meta=attribute_meta,
            value=value,
            **extra_fields,
        )
        super().append(attribute)
        return attribute

    def get(self, attribute_id: str) -> Optional[Attribute]:
        """Return the attribute matching the provided id, if present."""
        for attribute in self:
            if attribute.id == attribute_id:
                return attribute
        return None

    def get_value(self, attribute_id: str, default: Optional[object] = None) -> Optional[object]:
        """Convenience wrapper to get attribute value directly."""
        attribute = self.get(attribute_id)
        return attribute.value if attribute else default

    def update(self, attribute_id: str, value: object, **extra_fields) -> Attribute:
        """
        Update an existing attribute or create a new one when missing.
        """
        attribute = self.get(attribute_id)
        if attribute:
            attribute.value = value
            for key, attr_value in extra_fields.items():
                setattr(attribute, key, attr_value)
            if attribute.meta is None:
                attribute.meta = self._build_meta(attribute_id)
            return attribute

        return self.add(attribute_id, value, **extra_fields)

    def remove_by_id(self, attribute_id: str) -> Optional[Attribute]:
        """Remove the attribute with the given id and return it."""
        attribute = self.get(attribute_id)
        if attribute:
            super().remove(attribute)
        return attribute

    # Internal utilities ------------------------------------------------
    def _ensure_attribute(self, item: Union[Attribute, Dict]) -> Attribute:
        if isinstance(item, Attribute):
            return item
        if isinstance(item, dict):
            attribute = Attribute.from_dict(item)
            if attribute is None:
                raise ValueError("Attribute dictionary must not be empty.")
            return attribute
        raise TypeError(f"AttributeCollection supports Attribute or dict instances, got {type(item)!r}")

    def _build_meta(self, attribute_id: str) -> Optional[Meta]:
        if not self._owner:
            return None
        href = self._owner.get_attribute_href(attribute_id)
        if not href:
            return None
        return Meta(
            href=href,
            type="attributemetadata",
            mediaType="application/json",
        )
