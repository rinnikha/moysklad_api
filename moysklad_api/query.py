"""
Query building utilities for the MoySklad API.
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime


class Filter:
    """Helper class for building MoySklad API filters."""

    def __init__(self):
        """Initialize a new filter builder."""
        self._filters = []

    def add(self, field: str, operator: str, value: Any) -> 'Filter':
        """
        Add a filter condition.

        Args:
            field: Field name to filter on
            operator: Comparison operator
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        self._filters.append((field, operator, value))
        return self

    def eq(self, field: str, value: Any) -> 'Filter':
        """
        Equals filter.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, "=", value)

    def neq(self, field: str, value: Any) -> 'Filter':
        """
        Not equals filter.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, "!=", value)

    def gt(self, field: str, value: Any) -> 'Filter':
        """
        Greater than filter.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, ">", value)

    def lt(self, field: str, value: Any) -> 'Filter':
        """
        Less than filter.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, "<", value)

    def gte(self, field: str, value: Any) -> 'Filter':
        """
        Greater than or equals filter.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, ">=", value)

    def lte(self, field: str, value: Any) -> 'Filter':
        """
        Less than or equals filter.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, "<=", value)

    def like(self, field: str, value: str) -> 'Filter':
        """
        Like filter for string partial matching.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, "~", value)

    def starts_with(self, field: str, value: str) -> 'Filter':
        """
        Starts with filter for string prefix matching.

        Args:
            field: Field name to filter on
            value: Value to compare against

        Returns:
            Self for method chaining
        """
        return self.add(field, "~=", value)

    def to_params(self) -> Dict[str, str]:
        """
        Convert filters to URL parameters.

        Returns:
            Dictionary of URL parameters
        """
        filter_fields = []

        for i, (field, operator, value) in enumerate(self._filters):
            # Handle special cases for value formatting
            if isinstance(value, datetime):
                formatted_value = value.isoformat()
            elif isinstance(value, bool):
                formatted_value = str(value).lower()
            elif isinstance(value, (list, tuple)):
                formatted_value = ",".join(map(str, value))
            else:
                formatted_value = str(value)

            filter_fields.append(f"{field}{operator}{formatted_value}")

        return {"filter": ";".join(filter_fields)}


class OrderBy:
    """Helper class for building MoySklad API order by clauses."""

    ASC = "asc"
    DESC = "desc"

    def __init__(self):
        """Initialize a new order by builder."""
        self._order_by = []

    def add(self, field: str, direction: str = ASC) -> 'OrderBy':
        """
        Add an order by clause.

        Args:
            field: Field name to order by
            direction: Sort direction (asc or desc)

        Returns:
            Self for method chaining
        """
        self._order_by.append((field, direction))
        return self

    def to_params(self) -> Dict[str, str]:
        """
        Convert order by clauses to URL parameters.

        Returns:
            Dictionary of URL parameters
        """
        params = {}
        value = ";".join(f"{field},{direction}" for field, direction in self._order_by)
        if value:
            params["order"] = value
        return params


class QueryBuilder:
    """Builder for MoySklad API queries with filtering, sorting, and pagination."""

    def __init__(self):
        """Initialize a new query builder."""
        self._filter = Filter()
        self._order_by = OrderBy()
        self._expand = []
        self._limit = None
        self._offset = None
        self._search = None

    def filter(self) -> Filter:
        """
        Get the filter builder.

        Returns:
            Filter instance for building filter conditions
        """
        return self._filter

    def order_by(self) -> OrderBy:
        """
        Get the order by builder.

        Returns:
            OrderBy instance for building sort conditions
        """
        return self._order_by

    def limit(self, limit: int) -> 'QueryBuilder':
        """
        Set the limit for pagination.

        Args:
            limit: Maximum number of items to return

        Returns:
            Self for method chaining
        """
        self._limit = limit
        return self

    def offset(self, offset: int) -> 'QueryBuilder':
        """
        Set the offset for pagination.

        Args:
            offset: Number of items to skip

        Returns:
            Self for method chaining
        """
        self._offset = offset
        return self

    def expand(self, *fields: str) -> 'QueryBuilder':
        """
        Add fields to expand in the response.

        Args:
            fields: Field names to expand

        Returns:
            Self for method chaining
        """
        self._expand.extend(fields)
        return self

    def search(self, query: str) -> 'QueryBuilder':
        """
        Set the search query.

        Args:
            query: Search query string

        Returns:
            Self for method chaining
        """
        self._search = query
        return self

    def to_params(self) -> Dict[str, str]:
        """
        Convert the query to URL parameters.

        Returns:
            Dictionary of URL parameters
        """
        params = {}

        # Add filters
        params.update(self._filter.to_params())

        # Add order by
        params.update(self._order_by.to_params())

        # Add expand
        if self._expand:
            params["expand"] = ",".join(self._expand)

        # Add limit and offset
        if self._limit is not None:
            params["limit"] = str(self._limit)

        if self._offset is not None:
            params["offset"] = str(self._offset)

        # Add search
        if self._search is not None:
            params["search"] = self._search

        return params