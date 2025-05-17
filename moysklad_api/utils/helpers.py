"""
Helper functions for the MoySklad API.
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, Union

MS_FORMAT = "%Y-%m-%d %H:%M"


def ms_datetime_to_string(date: Union[datetime, str]) -> str:
    if date is None:
        return None

        # If it's already a datetime object
    if isinstance(date, datetime):
        # Adjust timezone by subtracting 2 hours
        adjusted_date = date - timedelta(hours=2)
        return adjusted_date.strftime(MS_FORMAT)
    return str(date)

def ms_string_to_datetime(date_str: Optional[str]) -> Optional[datetime]:
    if date_str is None or not date_str:
        return None

    try:
        # Parse the string to datetime
        dt = datetime.strptime(date_str, MS_FORMAT)

        # Adjust timezone by adding 2 hours (inverse of the subtraction in ms_datetime_to_string)
        adjusted_dt = dt + timedelta(hours=2)
        return adjusted_dt
    except ValueError:
        # Handle parsing errors - could raise an exception or return None depending on your needs
        return None

def format_date(date: Union[datetime, str]) -> str:
    """
    Format date for MoySklad API.

    Args:
        date: Date to format (datetime or ISO string)

    Returns:
        Formatted date string
    """
    if isinstance(date, str):
        # If already a string, try to parse it first
        date = parse_date(date)

    # Ensure UTC timezone
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    # Format in ISO 8601
    return date.isoformat()


def parse_date(date_str: str) -> datetime:
    """
    Parse date from MoySklad API.

    Args:
        date_str: Date string from API

    Returns:
        Parsed datetime object
    """
    # Try different formats
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",  # With milliseconds and timezone
        "%Y-%m-%dT%H:%M:%S%z",     # Without milliseconds, with timezone
        "%Y-%m-%dT%H:%M:%S.%f",    # With milliseconds, without timezone
        "%Y-%m-%dT%H:%M:%S",       # Without milliseconds and timezone
        "%Y-%m-%d",                # Date only
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            # If no timezone specified, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_str}")


def uuid_to_id(uuid_str: str) -> str:
    """
    Convert UUID to MoySklad ID format.

    Args:
        uuid_str: UUID string

    Returns:
        MoySklad ID format
    """
    # Remove hyphens
    return uuid_str.replace("-", "")


def id_to_uuid(id_str: str) -> str:
    """
    Convert MoySklad ID to UUID format.

    Args:
        id_str: MoySklad ID (without hyphens)

    Returns:
        UUID format (with hyphens)
    """
    # Convert to standard UUID format with hyphens
    return str(uuid.UUID(id_str))


def ensure_id_format(id_str: str) -> str:
    """
    Ensure ID is in the correct format (without hyphens).

    Args:
        id_str: ID string (with or without hyphens)

    Returns:
        ID in correct format (without hyphens)
    """
    # If the ID contains hyphens, convert to UUID format without hyphens
    if "-" in id_str:
        return uuid_to_id(id_str)
    return id_str