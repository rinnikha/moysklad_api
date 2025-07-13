"""
MoySklad API Client - A comprehensive Python client for the MoySklad JSON API v1.2
"""

__version__ = "0.1.0"

from .client import MoySklad
from .config import MoySkladConfig
from .exceptions import (
    MoySkladException,
    AuthenticationException,
    RateLimitException,
    NotFoundException,
    ValidationException
)
from .query import QueryBuilder, Filter, OrderBy

# Import convenience modules for easy access
from .entities.base import MetaEntity, Meta