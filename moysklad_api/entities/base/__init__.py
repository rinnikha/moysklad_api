"""
Core base structures for MoySklad entities.
"""

from .meta import Meta
from .attributes import Attribute, AttributeCollection
from .entity import MetaEntity, ListEntity

__all__ = ["Meta", "MetaEntity", "ListEntity", "Attribute", "AttributeCollection"]

