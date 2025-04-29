"""
Data conversion utilities for the MoySklad API.
"""

from typing import Dict, Any, Optional, Type, TypeVar, List, Union
from dataclasses import asdict, is_dataclass

from ..entities.base import MetaEntity, Meta

T = TypeVar('T', bound=MetaEntity)


def to_dict(obj: Any) -> Dict:
    """
    Convert object to dictionary for API.

    Args:
        obj: Object to convert

    Returns:
        Dictionary representation
    """
    if is_dataclass(obj):
        # Convert dataclass to dict
        data = asdict(obj)
        # Remove None values
        return {k: v for k, v in data.items() if v is not None}
    elif hasattr(obj, "to_dict"):
        # Use to_dict method if available
        return obj.to_dict()
    elif isinstance(obj, dict):
        # Already a dict
        return obj
    else:
        # Try to convert to dict using __dict__
        return {k: v for k, v in obj.__dict__.items() if not k.startswith('_') and v is not None}


def from_dict(data: Dict, cls: Type[T]) -> T:
    """
    Convert dictionary to object.

    Args:
        data: Dictionary data
        cls: Target class

    Returns:
        Instance of target class
    """
    if not data:
        return None

    if hasattr(cls, "from_dict"):
        # Use from_dict class method if available
        return cls.from_dict(data)
    else:
        # Create instance directly
        return cls(**data)


def entity_to_ref(entity: Union[MetaEntity, Dict, str]) -> Dict:
    """
    Convert entity to reference object for API.

    Args:
        entity: Entity instance, dictionary with meta, or entity ID

    Returns:
        Reference dictionary with meta
    """
    if isinstance(entity, str):
        # Entity ID provided
        return {
            "meta": {
                "href": entity,
                "type": "unknown"
            }
        }
    elif isinstance(entity, dict) and "meta" in entity:
        # Dictionary with meta provided
        return {"meta": entity["meta"]}
    elif isinstance(entity, MetaEntity):
        # Entity instance provided
        return {"meta": to_dict(entity.meta)}
    else:
        raise ValueError(f"Unable to create reference from: {entity}")


def list_to_dict(items: List[Any], key_field: str = "id") -> Dict[str, Any]:
    """
    Convert list of objects to dictionary by key field.

    Args:
        items: List of objects
        key_field: Field to use as dictionary key

    Returns:
        Dictionary of objects indexed by key field
    """
    result = {}

    for item in items:
        if isinstance(item, dict):
            key = item.get(key_field)
        else:
            key = getattr(item, key_field, None)

        if key:
            result[key] = item

    return result