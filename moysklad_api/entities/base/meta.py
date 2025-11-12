"""
Metadata structures for MoySklad entities.
"""

from dataclasses import dataclass
from typing import Dict, Optional


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
    def from_dict(cls, data: Dict) -> Optional["Meta"]:
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

